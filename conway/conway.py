from collections import Counter
from enum import Enum

import numpy as np

from common.utilities import plotter, GeneralConfig, get_new_grid


class SeedFunctionTypes(Enum):
    GLIDER = "glider"
    R_PENTOMINO = "r_pentomino"
    RANDOM = "random"

    def __str__(self):
        return self.value


class SeedFunctions:
    """Methods for some default seed functions.
     Note use of frozen set, as these are used as default arguments,
     so we make sure they immutable"""

    @staticmethod
    def get_glider_indices(n):
        return frozenset({(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)})

    @staticmethod
    def get_r_pentomino(n, offset=None):
        if offset is None:
            offset = int(n / 2)
        base = {(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)}
        return frozenset((i + offset, j + offset) for i, j in base)

    @staticmethod
    def get_random_seed(n, p=0.4):
        """Choose random (Bernoulli dist) starting grid, where p is prob of cell being alive"""
        indices_with_dist = zip(
            np.random.binomial(1, p, n ** 2), np.ndenumerate(np.zeros((n, n)))
        )
        return frozenset(j[0] for i, j in indices_with_dist if i == 1)

    seed_dict = {
        SeedFunctionTypes.GLIDER: get_glider_indices,
        SeedFunctionTypes.R_PENTOMINO: get_r_pentomino,
        SeedFunctionTypes.RANDOM: get_random_seed,
    }


class ConwayConfig(GeneralConfig):
    GeneralConfig.parser.add_argument(
        "--seed",
        metavar="s",
        type=SeedFunctionTypes,
        choices=list(SeedFunctionTypes),
        help="Initial grid state",
    )

    @classmethod
    def parse_args(cls,):
        args = GeneralConfig.parser.parse_args()
        if args.size is not None:
            cls.n = args.size
        if args.generations is not None:
            cls.generations = GeneralConfig.generations
        if args.seed is None:
            cls.seed = SeedFunctions.get_r_pentomino
        else:
            cls.seed = SeedFunctions.seed_dict[args.seed]


def get_new_conway_grid(out_grid: np.ndarray):
    """Simple iterative implementation of Conway engine. Loop through each cell
    count number of alive neighbours and adjust next grid according to Conway rules"""
    return get_new_grid(out_grid, get_next_generation_state, ConwayConfig.n)


def get_initial_grid(n, initial_seed=None):
    """Sets an initial grid with some points used as seed functions"""
    out_grid = np.zeros((n, n))
    if initial_seed is not None:
        out_grid = get_seed(out_grid, initial_seed(n))
    else:
        raise ValueError("Initial seed must be passed")
    return out_grid


def get_seed(out_grid, initial_alive_points=None):
    """Given an array of indices, sets these points to alive"""
    for index in initial_alive_points:
        out_grid[index] = 1
    return out_grid


def get_next_generation_state(cell_alive: int, neighbours: Counter):
    """Base logic for each cell"""
    grid_sum = neighbours[1]
    return int(
        (cell_alive and grid_sum in (2, 3)) or (not cell_alive and grid_sum == 3)
    )


def main():
    ConwayConfig.parse_args()
    plotter(
        get_initial_grid(ConwayConfig.n, ConwayConfig.seed),
        get_new_conway_grid,
        ConwayConfig.generations,
    )


if __name__ == "__main__":
    main()
