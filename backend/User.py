import mysql.connector
from Game import Game, get_users_games
from Database import Database


# The Users class is an object representation of a row in the database. This class contains methods
# for interacting with the database
class User:
    def __init__(self, db: Database, email: str = None):
        self.__pk = None
        self.email = email
        self.__db = db  # Database must be set
        self.games = []

    __pk: int | None  # Private: Primary Key in Database
    __db: Database  # Private: Database object for getting connections
    email: str | None  # Public: User email
    games: list[Game]  # Public: List of user games

    # Returns programmer representation of object
    def __repr__(self) -> str:
        return f'User({self.__pk}, "{self.email}")'

    # Returns user facing representation of object
    def __str__(self) -> str:
        return f"{self.email}"

    # Returns reference to game and appends it to users games
    def new_game(self) -> Game:
        if self.__pk is None:
            raise ValueError("User is not saved.")

        # Pass database from user
        new_game = Game(self.__db, self.__pk)
        self.games.append(new_game)
        return new_game

    # Load is a public method that pulls data from the database when called.
    # This method assumes either self.__pk is set, or self.email is set to find user.
    def load(self):
        try:
            if self.__pk is not None:
                # if available, lookup by self.__pk
                self.__select_on_pk()
            elif not self.__select_on_email():  # returns true if row found with self.email.
                # User with email does not exist in db.
                raise ValueError(f"db row for {self} does not exist.")  # save() will create row.
            else:
                # User found by email and self.__pk is now set, lookup by pk.
                self.__select_on_pk()

            self.__select_games()
        except ValueError as err:
            raise err

    # Save is a public method to push data in the object to the database.
    # self.__pk set to None indicate object does not exist in DB, will create. Otherwise, will
    # update row with self.__pk.
    def save(self):
        for param in [self.email]:
            if param is None:
                raise ValueError(f"Value in {self} not set")
        try:
            # looks for existing pk with email, if found set's pk and updates instead of insert
            if self.__pk is None and not self.__select_on_email():
                self.__insert()
            else:
                self.__update()

        except ValueError as err:
            raise err

    # Remove is a public method for deleting the related user from the database. It will also delete
    # any associated games from the database.
    def remove(self):
        if self.__pk is None:
            raise ValueError(f"db row for {self} does not exist.")  # save() will create row.

        for game in self.games:
            game.remove()

        self.__delete()

        # Remove the primary key as an indication row no longer exists in the database table.
        self.__pk = None

    # Select is a private method that calls SELECT on the row related with self.__pk
    # This method assumes self.__pk has been set, and the entry exists in the database.
    def __select_on_pk(self):
        with self.__db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                stmt = "SELECT email FROM users WHERE pk = ?"
                cursor.execute(stmt, (self.__pk,))
                result_set = cursor.fetchall()

                # Check Result
                if len(result_set) != 1:  # todo: is 0?
                    raise mysql.connector.IntegrityError(
                        "Should only be one entry per primary key."
                    )

                # Set object values
                self.email = result_set[0][0]

    # Select is a private method that calls SELECT on the row related with self.email and
    # sets self.__pk. A second database call with __select_on_pk is required to get other fields.
    # This avoids having other fields set in multiple places.
    # Return true if user row exists in database, false if row not found.
    def __select_on_email(self) -> bool:
        if self.email is None:
            raise ValueError(f"email for {self} not set.")
        with self.__db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                stmt = "SELECT pk FROM users WHERE email = %s"
                cursor.execute(stmt, (self.email,))
                result_set = cursor.fetchall()

                # Check Result
                if len(result_set) > 1:
                    raise mysql.connector.IntegrityError(
                        "Should only be one entry per email."
                    )

                if len(result_set) == 0:
                    # User with email does not exist.
                    return False

                # User found! set the primary key
                self.__pk = result_set[0][0]
                return True

    # Does not fully overwrite games list, only adds games found in database missing.
    # This method does not load the games, only creates objects that can be loaded.
    def __select_games(self):
        get_users_games(self.__db, self.__pk, self.games)

    # Insert is a private method that calls INSERT on the database creating a new row.
    # This method assumes the entry the object represents does not already exist in the database.
    def __insert(self):
        with self.__db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                stmt = "INSERT INTO users (email) VALUES (%s)"
                cursor.execute(stmt, (self.email,))
                cxn.commit()
                self.__pk = cursor.lastrowid

    # Update is a private method that calls UPDATE on the database pushing new data to the row
    # associated with self.__pk
    # This method assumes self.__pk and associated row exists in database.
    def __update(self):
        with self.__db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                stmt = "UPDATE users SET email = ? WHERE pk = ?"
                cursor.execute(stmt, (self.email, self.__pk))
                cxn.commit()

    # Delete is a private method that calls DELETE on the row in the Database associated with
    # self.__pk
    # This method assumes self.__pk is set and associate row exists in database.
    def __delete(self):
        with self.__db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                stmt = "DELETE FROM users WHERE pk = ?"
                cursor.execute(stmt, (self.__pk,))
                cxn.commit()

