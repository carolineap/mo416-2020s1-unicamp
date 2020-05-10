# mo416-2020s1-unicamp

## Installation Guide

To download the repository:

`git clone https://github.com/gabrielpreviato/mo416-2020s1-unicamp.git`

Then you need to install the basic dependencies to run the project on your system:

```
cd mo416-2020s1-unicamp
pip install -r requirements.txt
```

You also need to fetch the datasets from the [`aima-data`](https://github.com/aimacode/aima-data) repository:

```
git submodule init
git submodule update
```

## Project 1 - Search Algorithms

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

## Project 1 - Division of Tasks
Caroline Silva contributed with the base code structure, the DFS, BFS and Greedy search algorithms, Manhattan Heuristic and graphical visualization.

Gabriel Previato contributed with the A* search, the Wavefront Heuristic and the Simulated Annealing.

Thales Oliveira contributed with the A* search, the Ghost Avoidance Heuristic and Hill-Climbing.

Letícia Berto contributed with the Mazes creation, experiments executions, graphical visualization and the solution video.

All of the above mentioned contributed in the analysis and final report.

## Acknowledgements
This repository uses AIMA-Python modules (Copyright (c) 2016 aima-python contributors) distributed under the MIT license.
