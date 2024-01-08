import mysql.connector

from Database import Database


class Move:
    def __init__(self, db: Database, game_pk=None, move=None, move_idx=None):
        self.__db = db
        self.__pk = None
        self.game_pk = game_pk
        self.move = move
        self.move_idx = move_idx

    __db: Database
    __pk: int | None
    game_pk: int | None
    move: str | None
    move_idx: int | None

    # Returns the string representation
    def __str__(self):
        return self.move

    # Returns the Programmer representation
    def __repr__(self):
        return f'Move({self.game_pk}, {self.__pk}, {self.move_idx}, "{self.move}")'

    # Helps sort the moves ascending self.game_pk, then by self.move_idx
    def __lt__(self, other):
        if self.game_pk < other.game_pk:
            return True
        elif self.game_pk == other.game_pk:
            if self.move_idx < other.move_idx:
                return True
            else:
                return False
        else:
            return False

    # Saves the game and all moves in the database, either updating existing or creating entry
    def save(self):
        for param in [self.game_pk, self.move, self.move_idx]:
            if param is None:
                raise ValueError(f"parameter in {self} not set")

        if self.__pk is None:
            self.__insert()
        else:
            self.__update()

    # Loads fields from the database entry. The object must exist in the database.
    def load(self):
        if self.__pk is None:
            raise ValueError("cannot load: object not associated with database row")

        self.__select()

    # Deletes the object from the database and sets pk to false indicating it does not exist.
    def remove(self):
        if self.__pk is None:
            raise ValueError("cannot remove: object not associated with database row")

        self.__delete()
        self.__pk = None

    # Runs SELECT on the database by pk. Assumes pk is set and exists in database.
    def __select(self):
        with self.__db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                stmt = "SELECT game_pk, move_idx, move FROM moves WHERE pk = ?"
                cursor.execute(stmt, (self.__pk,))
                result_set = cursor.fetchall()

                if len(result_set) != 1:
                    # There should only be 1 move per primary key
                    raise mysql.connector.IntegrityError

                if len(result_set[0][2]) != 4:
                    # Moves should be exactly 4 characters
                    raise mysql.connector.IntegrityError

                self.game_pk = result_set[0][0]
                self.move_idx = result_set[0][1]
                self.move = result_set[0][2]

    # Runs UPDATE on the database for row matching pk. Assumes pk is set and exists in database.
    def __update(self):
        with self.__db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                cursor.execute(
                    "UPDATE moves SET game_pk = ?, move_idx = ?, move = ? WHERE pk = ?",
                    (self.game_pk, self.move_idx, self.move, self.__pk,)
                )
                cxn.commit()

    # Creates an entry in the database.
    # Assumes it does not exist in database; pk is not set, will overwrite.
    def __insert(self):
        with self.__db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                stmt = "INSERT INTO moves (game_pk, move_idx, move) VALUES (?, ?, ?)"
                cursor.execute(stmt, (self.game_pk, self.move_idx, self.move,))
                cxn.commit()
                self.__pk = cursor.lastrowid

    # Removes entry matching pk from database. Assumes pk is set.
    def __delete(self):
        with self.__db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                cursor.execute(
                    "DELETE FROM moves WHERE pk = ?",
                    (self.__pk,)
                )
                cxn.commit()


def get_game_moves(db: Database, game_pk: int, moves: list[Move]):
    with db.get_cxn() as cxn:
        with cxn.cursor(prepared=True) as cursor:
            cursor.execute(
                "SELECT pk FROM moves WHERE game_pk = ?",
                (game_pk,)
            )
            result_set = cursor.fetchall()

            existing_move_pks = [move._Move__pk for move in moves]

            for move_result in result_set:
                if move_result[0] in existing_move_pks:
                    # skip existing moves
                    continue

                new_move = Move(db, game_pk)
                new_move._Move__pk = move_result[0]
                moves.append(new_move)