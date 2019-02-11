import numpy as np
from enum import Enum
from collections import Counter
from common.utilities import plotter, GeneralConfig, get_enum_range, get_new_grid

"""
Module to do simple terrain generation- We randomise a starting grid
then have a probability threshold of living based on having a high enough number of neighbours
of same type. If we "die" we randomly generate a new square (so unlike Conway as not deterministic)
"""


class TerrainConfig(GeneralConfig):
    generations = 100


class Terrain:
    def __init__(self, prob_live):
        self.prob_live = prob_live
        self.prob_die = 1 - prob_live


class Land(Terrain):
    pass


class Water(Terrain):
    pass


class Hill(Terrain):
    pass


class TerrainType(Enum):
    WATER = 0
    LAND = 1
    HILL = 2

    def get_class(self):
        if self.value == 0:
            return Water
        elif self.value == 1:
            return Land
        elif self.value == 2:
            return Hill


class SetUpTerrainProbs:
    """Class to configure initial prob values of classes"""

    def __init__(self, water_live_prob: float, land_live_prob: float, hill_live_prob: float):
        self.water = Water(water_live_prob)
        self.land = Land(land_live_prob)
        self.hill = Hill(hill_live_prob)


class GoodInitialValues:
    fuzzy_land = (0.4, 0.5, 0)
    stable_land = (0.625, 0.625, 0)
    # test = (0.3, 0.3, 0)
    test = (0.3, 0.2, 0.1)


class Global:
    min_terrain_type_int, max_terrain_type_int = get_enum_range(TerrainType)
    terrain_holder = SetUpTerrainProbs(*GoodInitialValues.stable_land)


def get_new_terrain_grid(out_grid: np.ndarray) -> np.ndarray:
    """Counts neighbours and passes the counter object to get_next_state
        to apply game logic
    """
    return get_new_grid(out_grid, get_next_state,TerrainConfig.n )



def get_next_state(current_state: int, neighbours: Counter) -> int:
    """Applies the logic for next state- currently"""
    total = float(sum(neighbours.values()))
    current_state_terrain = TerrainType(current_state)
    terrain_class_type = current_state_terrain.get_class()
    # Take our current terrain holder, and look for attribute with name of matching class
    terrain_class_instance = Global.terrain_holder.__dict__.get(terrain_class_type.__name__.lower())
    same_neighbours = neighbours[current_state]
    relative_prob = same_neighbours / total
    if relative_prob > terrain_class_instance.prob_die:
        return current_state
    else:
        return np.random.randint(Global.min_terrain_type_int, Global.max_terrain_type_int)


def main():
    terrain_grid = np.random.randint(Global.min_terrain_type_int, Global.max_terrain_type_int + 1,
                                     (TerrainConfig.n, TerrainConfig.n))
    plotter(terrain_grid, get_new_terrain_grid, TerrainConfig.generations)


if __name__ == '__main__':
    main()
