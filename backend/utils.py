import itertools

def get_cells_around(row: int, column: int):
    cells = list(itertools.product(
        (row - 1, row, row + 1),
        (column - 1, column, column + 1)
    ))
    cells.remove((row, column))
    return tuple(cells)
