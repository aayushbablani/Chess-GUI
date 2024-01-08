import unittest
from test_Object import TestObjectCase
from Move import Move
from datetime import datetime


class TestMoveCase(TestObjectCase, unittest.TestCase):

    user_pk: int | None = None
    game_pk: int | None = None

    def setUp(self):
        super().setUp()
        with self.db.get_cxn() as cxn:
            with cxn.cursor() as cursor:
                cursor.execute("INSERT INTO users (email) VALUE ('user@domain.tld')")
                cxn.commit()
                self.user_pk = cursor.lastrowid
        with self.db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                cursor.execute("INSERT INTO games (user_pk, date_played) VALUE (?, ?)", (self.user_pk, datetime.now()))
                cxn.commit()
                self.game_pk = cursor.lastrowid

    # Tests that the string representation in correct.
    def test_str_output(self):
        move = Move(self.db, "1", "a2b4", 0)
        self.assertEqual(str(move), "a2b4")

    # Test that the programmer representation is correct.
    def test_repr_output(self):
        move = Move(self.db, 10, "a2b4", 0)
        move._Move__pk = 1
        self.assertEqual(repr(move), f'Move(10, 1, 0, "a2b4")')

    # Tests that moves sort correctly by game, then index.
    def test_lt_sort(self):
        move1 = Move(self.db, 10, "test", 3)
        move2 = Move(self.db, 10, "test", 2)
        move3 = Move(self.db, 1, "test", 2)
        move4 = Move(self.db, 1, "test", 1)

        moves = sorted([move1, move2, move3, move4])
        self.assertIs(moves[0], move4)
        self.assertIs(moves[1], move3)
        self.assertIs(moves[2], move2)
        self.assertIs(moves[3], move1)

    # Test that save throws an exception if values are missing
    # def test_save_game_missing_values(self): ...  # todo: implement me

    # Test that an existing database row is updated.
    def test_save_and_load_game(self):
        move = Move(self.db, self.game_pk, "a1a2", 0)
        move.save()

        move_loaded = Move(self.db)
        move_loaded._Move__pk = move._Move__pk
        move_loaded.load()

        self.assertEqual(move.move, move_loaded.move)
        self.assertEqual(move.move_idx, move_loaded.move_idx)
        self.assertEqual(move.game_pk, move_loaded.game_pk)

    # Test that load will throw an exception if pk is not set.
    def test_load_on_nonexisting(self):
        move = Move(self.db, 1, "a1a2", 0)
        with self.assertRaises(ValueError):
            move.load()

    # Test that remove will remove and entry from the database.
    def test_remove(self):
        move = Move(self.db, game_pk=self.game_pk, move="test", move_idx=1)
        move.save()
        self.assertIsNotNone(move._Move__pk)
        move_pk = move._Move__pk

        move.remove()
        self.assertIsNone(move._Move__pk)

        with self.db.get_cxn() as cxn:
            with cxn.cursor(prepared=True) as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM moves WHERE pk = ?",
                    (move_pk,)
                )
                result_set = cursor.fetchall()
                self.assertEqual(result_set[0][0], 0)

    # Test that calling remove on an object where pk is not set will raise exception.
    def test_remove_on_nonexisting(self):
        move = Move(self.db, 1, "a1a2", 0)
        with self.assertRaises(ValueError):
            move.remove()

    # Test the static method get_game_moves gets correct moves from moves table by game_pk.
    # def test_get_game_moves(self): ...  # todo: implement me

    # Test the static method get_game_moves throws exception if indexes of moves pulled is faulty.
    # def test_get_game_move_bad_order(self): ...

    # Test that selecting from database from the row associated with pk picks up data correctly.
    # def test_select(self): ...  # todo: implement me

    # Tests that running update on the row associated with pk will update correctly.
    # def test_update(self): ...  # todo: implement me

    # Tests that a database row will be created from fields in the object correctly.
    # def test_insert(self): ...  # todo: implement me

    # Tests that a row associated with pk is removed correctly.
    # def test_delete(self): ...  # todo: implement me


if __name__ == '__main__':
    unittest.main()
