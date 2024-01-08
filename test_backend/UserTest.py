import unittest
from os import getenv
from backend.User import User
from test_backend.DatabaseMock import DatabaseMock


class UserTestCase(unittest.TestCase):
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

    def test_check_load_on_non_existent(self):
        exception_caught = False
        user = User(self.db, "hello@world.com")
        try:
            user.load()
        except ValueError as val_err:
            exception_caught = True
            self.assertEqual(str(val_err), "db row for hello@world.com does not exist.")
        self.assertTrue(exception_caught)

    def test_check_user_create_and_retrieve(self):
        user = User(self.db, "user1@test.com")
        user.save()
        same_user_new_object = User(self.db, "user1@test.com")
        same_user_new_object.load()
        self.assertEqual(user._User__pk, same_user_new_object._User__pk)

    def test_check_create_on_existing_user(self):
        try:
            user1 = User(self.db, "user@test.com")
            user1.save()
            user2 = User(self.db, "user@test.com")
            user2.save()
            self.assertEqual(user1._User__pk, user2._User__pk)
        except Exception as err:
            print(err)


def main():
    unittest.main()

if __name__ == '__main__':
    main()