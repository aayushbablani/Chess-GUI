import os

import mysql.connector
from collections import OrderedDict
from os import getenv
from mysql.connector import errorcode

# https://dev.mysql.com/doc/connector-python/en/connector-python-examples.html

# todo: get values from docker, maybe env varaiables
config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASS"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
    'raise_on_warnings': True,
}
db_schema = getenv("DB_SCHEMA")


def get_cxn() -> mysql.connector.connect:
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


## Create the database
def create_database(cursor: mysql.connector.connect().cursor):
    try:
        cursor.execute(f"CREATE DATABASE {db_schema} DEFAULT CHARACTER SET 'utf8mb4'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

# Get SQL Files to create database tables
def get_tables() -> OrderedDict:
    tables = OrderedDict()
    sql_file_names = [
        "./db_tables/createUsers.sql",
        "./db_tables/createGames.sql",
        "./db_tables/createMoves.sql",
    ]
    for file in sql_file_names:
        with open(file, "r") as f:
            tables[file] = f.read()

    return tables

def create_tables():
    with get_cxn() as cxn:
        cursor = cxn.cursor()

        try:
            cursor.execute(f"USE {db_schema}")
        except mysql.connector.Error as err:
            print(f"Database {db_schema} does not exists.")
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                print(f"Database {db_schema} created successfully.")
                cxn.database = db_schema
            else:
                print(err)
                exit(1)

        tables = get_tables()

        for table_name in tables:
            table_description = tables[table_name]
            try:
                print(f"Creating table {table_name}: ", end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        cursor.close()




