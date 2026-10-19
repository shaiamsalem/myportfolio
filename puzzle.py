import random
from collections.abc import Sequence


SIZE = 4
CELL_COUNT = SIZE * SIZE
SOLVED_BOARD = tuple(range(1, CELL_COUNT)) + (0,)


def is_solvable(board: Sequence[int]) -> bool:
    if len(board) != CELL_COUNT or sorted(board) != list(range(CELL_COUNT)):
        raise ValueError("The board must contain each value from 0 to 15 exactly once.")

    tiles = [tile for tile in board if tile != 0]
    inversions = sum(
        tiles[left] > tiles[right]
        for left in range(len(tiles))
        for right in range(left + 1, len(tiles))
    )
    blank_row_from_bottom = SIZE - board.index(0) // SIZE
    return (inversions + blank_row_from_bottom) % 2 == 1


def move_tile(board: Sequence[int], tile_index: int) -> tuple[int, ...]:
    if not 0 <= tile_index < CELL_COUNT:
        return tuple(board)

    blank_index = board.index(0)
    same_row = blank_index // SIZE == tile_index // SIZE
    adjacent = (
        (same_row and abs(blank_index - tile_index) == 1)
        or abs(blank_index - tile_index) == SIZE
    )
    if not adjacent:
        return tuple(board)

    updated = list(board)
    updated[blank_index], updated[tile_index] = updated[tile_index], updated[blank_index]
    return tuple(updated)


def new_shuffled_board(
    rng: random.Random | None = None, moves: int = 150
) -> tuple[int, ...]:
    if moves < 1:
        raise ValueError("At least one shuffle move is required.")

    generator = rng or random.Random()
    board = list(SOLVED_BOARD)
    blank_index = CELL_COUNT - 1
    previous_blank: int | None = None

    for _ in range(moves):
        row, column = divmod(blank_index, SIZE)
        neighbors = [
            index
            for index in (
                blank_index - SIZE if row > 0 else -1,
                blank_index + SIZE if row < SIZE - 1 else -1,
                blank_index - 1 if column > 0 else -1,
                blank_index + 1 if column < SIZE - 1 else -1,
            )
            if index >= 0 and index != previous_blank
        ]
        next_blank = generator.choice(neighbors)
        board[blank_index], board[next_blank] = board[next_blank], board[blank_index]
        previous_blank, blank_index = blank_index, next_blank

    if tuple(board) == SOLVED_BOARD:
        tile_index = blank_index - 1 if blank_index % SIZE else blank_index + 1
        board[blank_index], board[tile_index] = board[tile_index], board[blank_index]

    return tuple(board)
