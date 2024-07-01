# Using modified quick-clique library to calculate 0-1-2 problem results

## Setup:

### Clone this repo

`git clone git@github.com:shivaanshag/max_len_clique.git`

### Initialize the quick-clique dependency

`git submodule update --init --recursive`

### Apply changes to the quick-cliques library (find a workaround for submodule changes)
`cp main.cpp quick-cliques/src/`
`cp Tools.cpp quick-cliques/src/`

### Build quick-cliques binary
- `cd quick-cliques`
- `make && cd ..`

## Run the calculations
### For running a specific combination:

`python quick_clique.py n n0 n2`

Ex. `python quick_clique.py 6 4 2`

### For running all combinations till n:

`python script_caculate_values.py n`

Ex. `python script_caculate_values.py 6`

## (Optional) Visualize
### Reads from results folder and generates a 3D graph with largest set size as color

`python visualize.py`


