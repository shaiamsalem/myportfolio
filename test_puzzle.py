import random
import unittest

from puzzle import SOLVED_BOARD, is_solvable, move_tile, new_shuffled_board


class PuzzleTests(unittest.TestCase):
    def test_solved_board_is_solvable(self) -> None:
        self.assertTrue(is_solvable(SOLVED_BOARD))

    def test_single_move_is_solvable(self) -> None:
        one_move_away = move_tile(SOLVED_BOARD, 14)
        self.assertTrue(is_solvable(one_move_away))

    def test_unsolvable_board_is_detected(self) -> None:
        unsolvable = (2, 1) + SOLVED_BOARD[2:]
        self.assertFalse(is_solvable(unsolvable))

    def test_move_swaps_adjacent_tile_with_blank(self) -> None:
        result = move_tile(SOLVED_BOARD, 14)
        self.assertEqual(result, tuple(range(1, 15)) + (0, 15))

    def test_non_adjacent_move_leaves_board_unchanged(self) -> None:
        self.assertEqual(move_tile(SOLVED_BOARD, 0), SOLVED_BOARD)

    def test_shuffle_is_deterministic_solvable_and_not_solved(self) -> None:
        first = new_shuffled_board(random.Random(42), moves=80)
        second = new_shuffled_board(random.Random(42), moves=80)
        self.assertEqual(first, second)
        self.assertNotEqual(first, SOLVED_BOARD)
        self.assertEqual(sorted(first), list(range(16)))
        self.assertTrue(is_solvable(first))

    def test_invalid_board_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            is_solvable((1, 2, 3))

    def test_shuffle_requires_at_least_one_move(self) -> None:
        with self.assertRaises(ValueError):
            new_shuffled_board(moves=0)


if __name__ == "__main__":
    unittest.main()
