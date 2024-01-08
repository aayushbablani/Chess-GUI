import random
import unittest

import mysql.connector

from test_Object import TestObjectCase
from User import User
from Game import Game


class TestUserCase(TestObjectCase, unittest.TestCase):

    # Tests that loading a user from the database that does not exist raises an error, because pk
    # is not set.
    def test_check_load_on_non_existent(self):
        user = User(self.db, "user@domain.tld")
        with self.assertRaises(ValueError):
            user.load()

    # Tests that the output string is as expected.
    def test_str_output(self):
        user = User(db=self.db, email='user@domain.tld')
        self.assertEqual(str(user), 'user@domain.tld')

    # Test the output representation is as expected
    def test_repr_output(self):
        user = User(self.db)
        user.email = 'user@domain.tld'
        user._User__pk = 1010101
        self.assertEqual(repr(user), 'User(1010101, "user@domain.tld")')

    # Tests that when created a game is created by a user and saved it is retrievable.
    def test_add_new_game(self):
        user = User(self.db, "user@domain.tld")
        user.save()
        game = user.new_game()
        self.assertIn(game, user.games)
        game.save()

        loaded_user = User(self.db, "user@domain.tld")
        loaded_user.load()

        self.assertEqual(1, len(loaded_user.games))
        self.assertEqual(game._Game__pk, loaded_user.games[0]._Game__pk)

    def test_lt_sort(self):
        ...  # todo: implement me

    # Tests that when a user with the same email is loaded it will pull the existing entry from
    # The database
    def test_load_on_existing(self):
        user = User(self.db, "user@domain.tld")
        user.save()
        user_loaded = User(self.db, "user@domain.tld")
        user_loaded.load()
        self.assertEqual(user._User__pk, user_loaded._User__pk)

    # Tests that a user that 2 users saved with the same email will represent the same entry in the
    # database.
    def test_check_create_on_existing_user(self):
        user1 = User(self.db, "user@domain.tld")
        user1.save()
        user2 = User(self.db, "user@domain.tld")
        user2.save()
        self.assertEqual(user1._User__pk, user2._User__pk)

    # Test that loading a user without pk set will throw an error
    def test_load_on_nonexistent(self):
        user = User(self.db, "user@domain.tld")
        with self.assertRaises(ValueError):
            user.load()

    # Test that saving a user will retain its games
    def test_save_on_existing(self):
        user = User(self.db, "user@domain.tld")
        user.save()
        game = user.new_game()
        game.save()

        user2 = User(self.db, "user@domain.tld")
        user2.save()  # get pk
        user2.load()  # load the games

        self.assertEqual(user._User__pk, user2._User__pk)

        self.assertEqual(1, len(user2.games))
        self.assertEqual(game._Game__pk, user2.games[0]._Game__pk)

    # Test that saving creating a game before creating a user will throw an exception.
    def test_game_save_not_without_saved_user(self):
        user = User(self.db, "user@domain.tld")
        with self.assertRaises(ValueError):
            user.new_game()

    # Test that when a user is removed, it's object will reflect that no longer having __pk set.
    def test_remove_on_existing(self):
        user = User(self.db, "user@domain.tld")
        user.save()
        self.assertIsNotNone(user._User__pk)
        user.remove()
        self.assertIsNone(user._User__pk)

    # Tests that when a user is removed from the database, the users games are also removed.
    def test_remove_on_existing_with_games(self):
        user = User(self.db, "user@domain.tld")
        user.save()
        games: list[Game] = []

        for i in range(10):
            game: Game = user.new_game()
            game.save()
            self.assertIsNotNone(game._Game__pk)
            games.append(game)

        user.remove()
        self.assertIsNone(user._User__pk)

        for game in games:
            self.assertIsNone(game._Game__pk)

    # This tests that running remove on a user without __pk set will throw an exception.
    def test_remove_on_nonexistent(self):
        user = User(self.db)
        self.assertIsNone(user._User__pk)
        with self.assertRaises(ValueError):
            user.remove()

    # This tests that the correct email is picked up when selecting by pk.
    def test_select_by_pk(self):
        for i in range(1, 100):
            user = User(self.db, f"user{i}@domain.tld")
            user.save()

        user2 = User(self.db)
        user2._User__pk = 1
        user2._User__select_on_pk()

        self.assertEqual(user2.email, "user1@domain.tld")

    # This tests that the correct __pk is picked up when selecting from the database by email.
    def test_select_on_existing_by_email(self):
        user = User(self.db, "user@domain.tld")
        user.save()

        user2 = User(self.db, "user@domain.tld")
        self.assertTrue(user2._User__select_on_email())

        self.assertEqual(user._User__pk, user2._User__pk)

    # This tests that __select_on_email returns false when the email does not exist.
    def test_select_on_nonexistent_by_email(self):
        user = User(self.db, "user@domain.tld")
        self.assertFalse(user._User__select_on_email())

    # This tests that all games saved will be loaded.
    def test_select_of_a_users_games(self):
        user = User(self.db, "user@domain.tld")
        user.save()
        games: list[Game] = []

        # create and save games
        for i in range(10):
            game = user.new_game()
            game.save()
            games.append(game)

        # retrieve games
        user2 = User(self.db, "user@domain.tld")
        user2._User__select_on_email()
        user2._User__select_games()

        # check if games are there
        games_pks = [orig._Game__pk for orig in games]
        for game in user2.games:
            self.assertIn(game._Game__pk, games_pks)

        # create and save more games
        for i in range(10):
            game = user2.new_game()
            game.save()
            games.append(game)

        # retrieve games again
        user3 = User(self.db, "user@domain.tld")
        user3._User__select_games()

        # check if all games are there
        games_pks = [orig._Game__pk for orig in games]
        for game in user3.games:
            self.assertIn(game._Game__pk, games_pks)

    # Test that a user is created
    def test_insert(self):
        user = User(self.db, "user@domain.tld")
        self.assertIsNone(user._User__pk)
        user._User__insert()
        self.assertIsNotNone(user._User__pk)

    # Test that the email of an existing user can be updated
    def test_update(self):
        user = User(self.db, "user@domain.tld")
        user.save()
        self.assertIsNotNone(user._User__pk)

        user.email = "replaced@domain.tld"
        user._User__update()

        user2 = User(self.db, "replaced@domain.tld")
        user2.load()
        self.assertEqual(user._User__pk, user2._User__pk)

    # test that a user can be deleted from the database
    def test_delete(self):
        user = User(self.db, "user@domain.tld")
        user.save()
        self.assertIsNotNone(user._User__pk)

        user._User__delete()
        with self.db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                stmt = "SELECT COUNT(*) FROM users WHERE pk = ?"
                cursor.execute(stmt, (user._User__pk,))
                result_set = cursor.fetchall()
                self.assertEqual(result_set[0][0], 0)


if __name__ == '__main__':
    unittest.main()
