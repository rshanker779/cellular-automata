from enum import EnumMeta
from typing import Tuple, Callable
import numpy as np
from matplotlib import pyplot as plt
from collections import Counter
import argparse

class GeneralConfig:
    n = 100
    generations = 1000
    parser = argparse.ArgumentParser("Conway variables")
    parser.add_argument('--size', metavar='n', type=int, help='Number of pixels in gid')
    parser.add_argument('--generations', metavar='g', type=int, help='Number of generations to run for')

def plotter(initial_grid, repeated_function, generations=100):
    """Plotter using matplotlib to plot each array."""
    im = None
    out_grid = initial_grid
    for _ in range(generations):
        if im is None:
            # Plot initial data
            im = plt.imshow(out_grid, interpolation='none', vmin=0, vmax=3, cmap='ocean')
        else:
            # update
            out_grid = repeated_function(out_grid)
            im.set_data(out_grid)
        plt.draw()
        plt.pause(0.1)


def get_new_grid(out_grid: np.ndarray, get_next_function:Callable[[int, Counter], int],n:int ) -> np.ndarray:
    """Counts neighbours and passes the counter object to get_next_state
        to apply game logic
    """
    new_grid = out_grid.copy()
    neighbours = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i or j]
    for (x, y), _ in np.ndenumerate(out_grid):
        surrounding_list = []
        surrounding_dict = {}
        for dx, dy in neighbours:
            new_x, new_y = x + dx, y + dy
            if new_x >= 0 and new_x < n and new_y >= 0 and new_y < n:
                surrounding_list.append(out_grid[new_x, new_y])
                surrounding_dict[(dx, dy)] = out_grid[new_x, new_y]
        counter = Counter(surrounding_list)
        new_grid[x, y] = get_next_function(out_grid[x, y], counter)
    return new_grid

def get_enum_range(cls: EnumMeta) -> Tuple[int, int]:
    """Takes an EnumMeta class and returns a tuple of min and max int
    used in internal representation (as unlike other languages thiEnums is not
    standardised."""
    cls_members = {i.value for i in cls}
    return min(cls_members), max(cls_members)