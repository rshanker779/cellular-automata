# cellular-automata
Python implementations of two simple cellular automata, with a numpy engine and matplotlib graphics.
Includes Conway's game of life and a terrain generation script.

To install, clone code and then from cellular_automata/ run 
```
python setup.py install
pip install .
``` 
( using a virtual environment). This add command line scripts
```
conway_
terrain_
```
that can then be run.

Both scripts take arguments of the form
```
--size int
--generations int
```
where the size is the number of pixels in output grid and generations is number of iterative steps.
In addition Conway accepts one of three seed arguments
```
--seed <'random', 'r_pentomino', 'glider'> 
```
that specifies a starting state.

Note dependencies are restrictive and project will likely work with lower versions of
python, numpy and matplotlib.
