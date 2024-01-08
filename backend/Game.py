from datetime import datetime

import mysql.connector

from Move import Move, get_game_moves
from Database import Database


class Game:

    def __init__(self, db: Database, user_pk: int = None, date_played: datetime = datetime.now()):
        self.__pk = None
        self.user_pk = user_pk
        self.__db = db
        self.moves = []
        self.date_played = date_played

    __db: Database
    __pk: int | None  # Primary Key
    user_pk: int | None  # Foreign Key
    moves: list[Move]
    date_played: datetime

    # Returns the string representation of Game instance
    def __str__(self) -> str:
        date_str = self.date_played.strftime("%Y-%m-%d %H:%M:%S")
        return date_str

    # Returns the programmer representation of Game instance
    def __repr__(self) -> str:
        return f'Game({self.user_pk}, {self.__pk}, "{self.date_played.strftime("%Y-%m-%d %H:%M:%S")}")'

    # Helps sort games first ascending by user, then ascending oldest to newest
    def __lt__(self, other):
        if self.user_pk < other.user_pk:
            return True
        elif self.user_pk == other.user_pk:
            return self.date_played < other.date_played
        else:
            return False

    # Saves the game and all moves to the database, either updating existing or creating entry.
    def save(self):
        for i, param in enumerate([self.user_pk, self.date_played]):
            if param is None:
                raise ValueError(f"parameter {i} in {self} not set")

        if self.__pk is None:
            self.__insert()
        else:
            self.__update()

    # Loads moves and date_played.
    def load(self):
        if self.__pk is None:
            raise ValueError("cannot load: object not associated with database row.")

        self.__select()
        self.__select_moves()
        for move in self.moves:
            move.load()

    # Removes game moves and game from database.
    def remove(self):
        if self.__pk is None:
            raise ValueError("cannot remove: object not associated with database row.")

        for move in self.moves:
            move.remove()

        self.__delete()
        self.__pk = None


    # Checks value of move, adds to self.moves, and saves move.
    # Will overwrite in self.moves if index is set. Will otherwise add as latest move.
    # Assumes game has already been saved.
    def add_move(self, move: str, index: int = None) -> Move:
        if self.__pk is None:
            raise ValueError("cannot add move: object not associated with database row.")

        if len(move) != 4:
            raise ValueError("move is wrong size")

        if index is None:
            index = len(self.moves)

        else:
            if index < 0 or index > len(self.moves):
                raise ValueError("invalid index")

        move = Move(self.__db, self.__pk, move, index)
        move.save()
        self.moves.append(move)
        return move

    # Runs select on the database by pk. Assumes database row matching pk exists and pk is set.
    def __select(self):
        with self.__db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                cursor.execute(
                    "SELECT user_pk, date_played FROM games WHERE pk = ?",
                    (self.__pk,)
                )
                result_set = cursor.fetchall()

                if len(result_set) != 1:
                    raise mysql.connector.IntegrityError("wrong number of records.")

                self.user_pk = result_set[0][0]
                self.date_played = result_set[0][1]

    # Creates empty Move objects in self.moves for rows found in database matching pk.
    # Moves must be loaded.
    def __select_moves(self):
        get_game_moves(self.__db, game_pk=self.__pk, moves=self.moves)

    # Updates all fields in database to match object. Assumes pk is set and entry exists
    def __update(self):
        with self.__db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                cursor.execute(
                    "UPDATE games SET user_pk = ?, date_played = ? WHERE pk = ?",
                    (self.user_pk, self.date_played, self.__pk,)
                )
                cxn.commit()

    # Creates entry for object instance in database. Assumes it does not exist in database.
    def __insert(self):
        with self.__db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                cursor.execute(
                    "INSERT INTO games (user_pk, date_played) VALUES (?, ?)",
                    (self.user_pk, self.date_played)
                )
                cxn.commit()
                self.__pk = cursor.lastrowid

    # Runs delete on object in database. Assumes entry matching pk exists and pk is set.
    def __delete(self):
        with self.__db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                cursor.execute(
                    "DELETE FROM games WHERE pk = ?",
                    (self.__pk,)
                )
                cxn.commit()


# Does not fully overwrite games list, only adds games found in database missing.
# This method does not load the games, only creates objects that can be loaded.
def get_users_games(db: Database, user_pk: int, games: list[Game]):
    with db.get_cxn() as cxn:
        with cxn.cursor(prepared=True) as cursor:
            cursor.execute(
                "SELECT pk FROM games WHERE user_pk = ?",
                (user_pk,)
            )
            result_set = cursor.fetchall()

            existing_game_pks = [game._Game__pk for game in games]

            for game_result in result_set:
                if game_result[0] in existing_game_pks:
                    # skip existing games
                    continue

                new_game = Game(db)
                new_game._Game__pk = game_result[0]
                games.append(new_game)