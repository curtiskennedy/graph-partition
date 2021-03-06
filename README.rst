***************
Graph-Partition
***************

Algorithms implemented as described in "Approximation algorithms for the maximally balanced connected graph tripartition problem" by Chen et al. 2019.

| Approx-1: MAX-MIN k=2 on 2-connected graphs
| Approx-2: MAX-MIN k=2 on connected graphs
| Approx-3: MIN-MAX k=3 on 2-connected graphs
| Approx-4: MIN-MAX k=3 on connected graphs with two bicomponents
| Approx-5: MIN-MAX k=3 on connected graphs
| Approx-6: MAX-MIN k=3 on 2-connected graphs
| Approx-7: MAX-MIN k=3 on connected graphs with two bicomponents
| Approx-8: MAX-MIN k=3 on connected graphs

Installation (linux commands shown)
############
Create a Python3.8 virtual environment (confirm version with 'python3.8 --version')::
    
    python3.8 -m venv env

Activate the created environment::
    
    source env/bin/activate
    
Install the package::
    
    pip install git+https://github.com/curtiskennedy/graph-partition.git@2021.8.27

Navigate to any folder containing instances (or containing sub-folders of instances)::
    
    cd instances

Run the package using::
    
    partition

Deactivate the virtual environment, the partition command will no longer work::
    
    deactivate
