import numpy as np

from common.utilities import plotter


class SeedFunctions:
    """Methods for some default seed functions.
     Note use of frozen set, as these are used as default arguments,
     so we make sure they immutable"""

    @staticmethod
    def get_glider_indices():
        return frozenset({(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)})

    @staticmethod
    def get_r_pentomino(offset=0):
        base = {(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)}
        return frozenset((i + offset, j + offset) for i, j in base)

    @staticmethod
    def get_random_seed(n, p=0.5):
        """Choose random (Bernoulli dist) starting grid, where p is prob of cell being alive"""
        indices_with_dist = zip(np.random.binomial(1, p, n ** 2), np.ndenumerate(np.zeros((n, n))))
        return frozenset(j[0] for i, j in indices_with_dist if i == 1)


class Config:
    generations = 1000
    n = 100
    seed = SeedFunctions.get_random_seed(n, p=0.3)


def get_new_grid(out_grid: np.ndarray):
    """Simple iterative implementation of Conway engine. Loop through each cell
    count number of alive neighbours and adjust next grid according to Conway rules"""
    new_grid = out_grid.copy()
    for index, _ in np.ndenumerate(out_grid):
        cell_alive = out_grid[index] == 1
        grid_sum = - out_grid[index]
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    grid_sum += out_grid[index[0] + i, index[1] + j]
                except IndexError:
                    pass
        new_state = get_next_generation_state(cell_alive, grid_sum)
        new_grid[index] = new_state
    return new_grid


def get_initial_grid(n, initial_seed=None):
    """Sets an initial grid with some points used as seed functions"""
    out_grid = np.zeros((n, n))
    if initial_seed is not None:
        out_grid = get_seed(out_grid, initial_seed)
    else:
        out_grid = get_seed(out_grid)
    return out_grid


def get_seed(out_grid, initial_alive_points=SeedFunctions.get_r_pentomino(10)):
    """Given an array of indices, sets these points to alive"""
    for index in initial_alive_points:
        out_grid[index] = 1
    return out_grid


def get_next_generation_state(cell_alive, grid_sum):
    """Base logic for each cell"""
    return int((cell_alive and grid_sum in (2, 3)) or (not cell_alive and grid_sum == 3))


if __name__ == '__main__':
    plotter(get_initial_grid, get_new_grid, Config.n, Config.generations, Config.seed)
