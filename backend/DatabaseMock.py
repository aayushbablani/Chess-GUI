import mysql.connector

from Database import Database


class DatabaseMock(Database):

    # drops and recreate tables
    def clean(self):
        with self.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                cursor.execute("DROP TABLE IF EXISTS moves")
                cursor.execute("DROP TABLE IF EXISTS games")
                cursor.execute("DROP TABLE IF EXISTS users")
                cxn.commit()
        self._Database__create_tables(quiet=True)

    # returns true if tables have existing rows, should be an empty database
    def is_production(self) -> bool:
        for table_name in ["users", "games", "moves"]:
            with self.get_cxn() as cxn:
                with cxn.cursor() as cursor:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                        result_set = cursor.fetchall()

                        # If count of any table is not 0. return True
                        if result_set[0][0] != 0:
                            print(f"{table_name} table has rows")
                            return True
                    except mysql.connector.Error as err:
                        print(err)
                        print(err.with_traceback())

        # All tables checked have no rows
        return False
