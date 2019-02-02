import numpy as np
import unittest
import matplotlib.pyplot as plt


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


class Config:
    generations = 1000
    n = 100
    seed = SeedFunctions.get_r_pentomino(40)


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


def plotter(n=10, generations=100, initial_seed=None):
    """Plotter using matplotlib to plot each array."""
    im = None
    out_grid = get_initial_grid(n, initial_seed)
    for _ in range(generations):
        if im is None:
            # Plot initial data
            im = plt.imshow(out_grid, interpolation='none', vmin=0, vmax=2)
        else:
            # update
            out_grid = get_new_grid(out_grid)
            im.set_data(out_grid)
        plt.draw()
        plt.pause(0.1)


class ConwayTest(unittest.TestCase):
    """Test class"""

    def test_next_generation_case(self):
        """Tests the function that applies base Conway logic"""
        state_1 = get_next_generation_state(True, 0)
        self.assertEqual(state_1, 0)
        state_2 = get_next_generation_state(True, 1)
        self.assertEqual(state_2, 0)
        state_3 = get_next_generation_state(True, 2)
        self.assertEqual(state_3, 1)
        state_4 = get_next_generation_state(True, 3)
        self.assertEqual(state_4, 1)
        for i in range(4, 9):
            self.assertEqual(get_next_generation_state(True, i), 0)
        self.assertEqual(get_next_generation_state(False, 3), 1)
        for i in range(9):
            if i != 3:
                self.assertEqual(get_next_generation_state(False, i), 0)


if __name__ == '__main__':
    plotter(Config.n, Config.generations, Config.seed)
