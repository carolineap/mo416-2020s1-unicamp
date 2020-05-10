# Project 1 - Search Algorithms

To implement and evaluate solutions based on search methods for the problem described in [Project 1 PDF](p1.pdf) using the AIMA
function library (https://github.com/aimacode/aima-python/blob/master/search.ipynb). This project aims in
providing the solution implemeted with the following:

- Two search methods without information
- Two informed search methods with 2 distinct heuristics
- One local search method

The work consists of finding an adequate solution to the chosen problem, evaluating it according to: computational
cost, completeness, optimality. Your are required to clearly define:

- How the problem was modeled
- Implementation specifics and restrictions

## Project 1 - Repository Structure

The [Figure](https://github.com/gabrielpreviato/mo416-2020s1-unicamp/tree/master/project1/Figure) directory contains the images with the paths that the search algorithms had found.

The [Mazes](https://github.com/gabrielpreviato/mo416-2020s1-unicamp/tree/master/project1/Mazes) directory contains the txt files representing the Pacman maze.
In these mazes files, a vertical bar (|) represents a wall, a space ( ) represents a path and a dot (.) represents a path with food.

The [notebooks](https://github.com/gabrielpreviato/mo416-2020s1-unicamp/tree/master/project1/notebooks) directory contains some auxiliary Jupyter notebooks that were used but are not relevant for the final experiment, and may contains deprecated code.

The [src](https://github.com/gabrielpreviato/mo416-2020s1-unicamp/tree/master/project1/src) directory contains the implementation of the Pacman problem and all search algorithms that were used.

The [pacman](https://github.com/gabrielpreviato/mo416-2020s1-unicamp/tree/master/project1/pacman.ipynb) is the Jupyter Notebook used for evaluating the search algorithms, all data collected was then compiled in the [results](https://github.com/gabrielpreviato/mo416-2020s1-unicamp/tree/master/project1/results.csv) file.

The [analysis](https://github.com/gabrielpreviato/mo416-2020s1-unicamp/tree/master/project1/analysis.ipynb) is the Jupyter Notebook with the problem description, discussion and analysis over the search methods in the Pacman enviroment.
