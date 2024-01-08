import unittest
from os import getenv
from DatabaseMock import DatabaseMock


class TestObjectCase(unittest.TestCase):
    db: DatabaseMock

    @classmethod
    def setUpClass(cls):
        cls.db = DatabaseMock(
            {
                'user':              getenv("DB_USER"),
                'password':          getenv("DB_PASS"),
                'database':          getenv("DB_SCHEMA"),
                'host':              getenv("DB_HOST"),
                'port':              getenv("DB_PORT"),
                'raise_on_warnings': True,
            }
        )

        # Do NOT run on production database, will drop all tables.
        if cls.db.is_production():
            print("Rows Exist in Database, might be production.")
            exit(1)

    def setUp(self):
        self.db.clean()

    @classmethod
    def tearDownClass(cls):
        # removes rows from test database if running locally. Tests won't run if rows exist.
        cls.db.clean()


if __name__ == '__main__':
    unittest.main()
