import unittest
from datetime import datetime
from test_Object import TestObjectCase
from Game import Game


class TestGameCase(TestObjectCase, unittest.TestCase):

    user_pk: int | None = None

    def setUp(self):
        super().setUp()
        with self.db.get_cxn() as cxn:
            with cxn.cursor() as cursor:
                cursor.execute("INSERT INTO users (email) VALUE ('user@domain.tld')")
                cxn.commit()
                self.user_pk = cursor.lastrowid

    # Tests that the string representation in correct.
    def test_str_output(self):
        game = Game(self.db, self.user_pk, datetime.strptime(
            "2024-01-01 11:35:10",
            "%Y-%m-%d %H:%M:%S",
        ))
        self.assertEqual("2024-01-01 11:35:10", str(game))

    # Test that the programmer representation is correct.
    def test_repr_output(self):
        game_time = datetime.strptime(
            "2024-01-01 11:35:10",
            "%Y-%m-%d %H:%M:%S",
        )
        game = Game(self.db, self.user_pk, game_time)
        game._Game__pk = 2
        self.assertEqual(f'Game(1, 2, "2024-01-01 11:35:10")', repr(game))

    # Tests that games sort correctly by
    def test_lt_sort(self):
        game1 = Game(
            self.db,
            user_pk=10,
            date_played=datetime.strptime(
                "22/01/24 11:35:10",
                "%d/%m/%y %H:%M:%S",
            )
        )
        game2 = Game(
            self.db,
            user_pk=10,
            date_played=datetime.strptime(
                "23/01/24 11:35:10",
                "%d/%m/%y %H:%M:%S",
            )
        )
        game3 = Game(
            self.db,
            user_pk=2,
            date_played=datetime.strptime(
                "23/01/23 11:35:10",
                "%d/%m/%y %H:%M:%S",
            )
        )
        game4 = Game(
            self.db,
            user_pk=2,
            date_played=datetime.strptime(
                "22/01/23 11:35:10",
                "%d/%m/%y %H:%M:%S",
            )
        )
        game5 = Game(
            self.db,
            user_pk=10,
            date_played=datetime.strptime(
                "23/01/20 11:35:10",
                "%d/%m/%y %H:%M:%S",
            )
        )

        games = sorted([game1, game2, game3, game4, game5])
        self.assertIs(games[0], game4)
        self.assertIs(games[1], game3)
        self.assertIs(games[2], game5)
        self.assertIs(games[3], game1)
        self.assertIs(games[4], game2)

    # Test that save throws an exception if values are missing
    # def test_save_game_missing_values(self): ...  # todo: implement me

    def test_save_and_load_game(self):
        game = Game(self.db, user_pk=self.user_pk)
        game.save()
        move1 = game.add_move("b1b2")
        move2 = game.add_move("b2b3")
        self.assertIsNotNone(game._Game__pk)

        game_loaded = Game(self.db)
        game_loaded._Game__pk = game._Game__pk
        game_loaded.load()
        loaded_game_pks = [move._Move__pk for move in game_loaded.moves]
        self.assertIn(move1._Move__pk, loaded_game_pks)
        self.assertIn(move2._Move__pk, loaded_game_pks)
        move3 = game_loaded.add_move("b3b4")

        game.load()
        loaded_game_pks = [move._Move__pk for move in game_loaded.moves]
        self.assertIn(move3._Move__pk, loaded_game_pks)

    def test_remove_game(self):
        game = Game(self.db, user_pk=self.user_pk)
        game.save()
        self.assertIsNotNone(game._Game__pk)
        move = game.add_move("a1b2")
        game.remove()

        self.assertIsNone(game._Game__pk)
        self.assertIsNone(move._Move__pk)

    # Test that games are sequential
    def test_new_game_on_many_games(self):
        game = Game(self.db, user_pk=self.user_pk)
        game.save()

        for i in range(100):
            game.add_move(f"a{(i%8)+1}a{(i%8)+2}")
            self.assertEqual(game.moves[i].move_idx, i)


        self.assertEqual(game.moves[0].move, "a1a2")
        self.assertEqual(game.moves[99].move, "a4a5")

    # Test exception thrown if games not saved before adding moves
    def test_add_move_without_saved_game(self):
        game = Game(self.db, user_pk=self.user_pk)
        with self.assertRaises(ValueError):
            game.add_move("a1a2")

    # Test exception thrown when adding move with index beyond next move
    def test_add_move_outside_of_range(self):
        game = Game(self.db, user_pk=self.user_pk)
        game.save()

        self.assertEqual(len(game.moves), 0)

        move1 = game.add_move("a1a2")
        self.assertEqual(move1.move_idx, 0)
        move2 = game.add_move("a2a3")
        self.assertEqual(move2.move_idx, 1)

        self.assertEqual(len(game.moves), 2)

        with self.assertRaises(ValueError):
            game.add_move("c7c8", 12)

    # def test_update_game(self): ...  # todo: implement me

    # def test_delete_game(self): ...  # todo: implement me


if __name__ == '__main__':
    unittest.main()
