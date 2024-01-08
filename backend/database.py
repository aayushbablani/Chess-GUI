import time

import mysql.connector
from collections import OrderedDict
from mysql.connector import errorcode
from os.path import dirname, abspath, join


# Object representation of database. Create database and schema when initialized. Then used to
# initiate connections and make calls.
class Database:
    def __init__(self, config: dict[str, str]):
        # Create Database Pool
        try:
            self.__schema = config['database']
            self.__cxnpool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="dbpool",
                pool_size=3,
                # remove schema from config so it can be created.
                **{k: v for k, v in config.items() if k != "database"},
            )
        except mysql.connector.Error as err:
            print(err)
            exit(1)

        # Setup Database
        self.__create_schema()
        self.__cxnpool.set_config(**config)  # reset pool config with schema after it's been created
        self.__create_tables()

    __schema: str
    __cxnpool: mysql.connector.pooling.MySQLConnectionPool

    # Public method used for creating database connections from pool.
    def get_cxn(self, timeout=1, retries=10):
        attempt: int = 0
        while attempt < retries:
            try:
                cxn = self.__cxnpool.get_connection()

                if cxn.is_connected():
                    return cxn
                else:
                    attempt += 1
                    time.sleep(timeout)

            except mysql.connector.Error as err:
                print(err)

        raise mysql.connector.Error("not connected to database.")

    # Private method that the schema in the database.
    # see: https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
    def __create_schema(self, quiet: bool = False):
        with self.get_cxn() as cxn:
            with cxn.cursor() as cursor:
                try:
                    cursor.execute(f"USE {self.__schema}")
                except mysql.connector.Error as err:
                    if not quiet:
                        print(f"Database {self.__schema} does not exists.")
                    if err.errno == errorcode.ER_BAD_DB_ERROR:
                        cursor.execute(
                            f"CREATE DATABASE {self.__schema} DEFAULT CHARACTER SET 'utf8mb4'"
                        )
                        if not quiet:
                            print(f"Database {self.__schema} created successfully.")
                    else:
                        if not quiet:
                            print(f"Failed creating database: {err}")
                        exit(1)

    # Private method that create database tables in the schema if they don't already exist.
    # Assumes schema has been created.
    def __create_tables(self, quiet: bool = False):
        with self.get_cxn() as cxn:
            with cxn.cursor() as cursor:
                try:
                    cursor.execute(f"USE {self.__schema}")
                except mysql.connector.Error as err:
                    print(f"Database {self.__schema} does not exists.")
                    print(err)
                    exit(1)

                # Get table definitions from SQL files
                # Order of creation matters because of foreign keys, using OrderedDict
                tables = OrderedDict()

                tables_dir = join(dirname(abspath(__file__)), "db_tables")

                sql_file_names = {
                    "users": join(tables_dir, "createUsers.sql"),
                    "games": join(tables_dir, "createGames.sql"),
                    "moves": join(tables_dir, "createMoves.sql"),
                }
                for table, file in sql_file_names.items():
                    with open(file, "r") as f:
                        tables[table] = f.read()

                # Create each table if it doesn't exist.
                for table_name in tables:
                    table_description = tables[table_name]
                    try:
                        if not quiet:
                            print(f"Creating table {table_name}: ", end='')
                        cursor.execute(table_description)
                    except mysql.connector.Error as err:
                        if not quiet:
                            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                                print("already exists.")
                            else:
                                print(err.msg)
                    else:
                        if not quiet:
                            print("OK")
