import random
from collections import Counter
from enum import Enum
import numpy as np
from common.utilities import plotter, GeneralConfig, get_new_grid

class NationConfig(GeneralConfig):
    pass

class AllNations(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3


class Nation:
    def __init__(self, attack_strength: int, defence_strength: int):
        self.attack_strength = attack_strength
        self.defence_strength = defence_strength

    def battle(self, enemy)->bool:
        attack_roll = random.randint(0, self.attack_strength)
        defence_roll = random.randint(0, enemy.defence_strength)
        return attack_roll > defence_roll

class NationHolder:
    nation_dict ={
        AllNations.RED: Nation(2,3),
        AllNations.BLUE: Nation(3,4),
        AllNations.GREEN: Nation(2,5)
    }

def get_next_state(current_state: int, neighbours: Counter)->int:
    attacker = int(random.choice(list(neighbours.keys())))
    #If there are enemies and no allies surronding, we die
    if current_state>0 and [i for i in neighbours.keys() if i!=0 and i!=current_state] and neighbours.get(current_state)is None:
        return 0
    if attacker!=0:
        if current_state==0:
            return attacker
        attacker_class = NationHolder.nation_dict[AllNations(attacker)]
        defender_class = NationHolder.nation_dict[AllNations(current_state)]
        if attacker_class.battle(defender_class):
            return attacker
    return current_state

def get_initial_grid():
    grid = np.zeros((NationConfig.n,NationConfig.n))
    grid[5,5] = 1
    grid[-5,-5]=2
    grid[-5,5] = 3
    return grid

def get_next_nation_grid(out_grid:np.ndarray)->np.ndarray:
    return get_new_grid(out_grid,get_next_state, NationConfig.n )

def main():
    grid = get_initial_grid()
    plotter(grid, get_next_nation_grid, NationConfig.generations)


if __name__ == '__main__':
    main()
