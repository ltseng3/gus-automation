# Pineapple Experiment Automation
This repo consists of python code that will autonomously run the replication protocol experiments cited in our paper ("Pineapple: Unifying Multi-Paxos and Atomic Shared Registers") and plot them. See `config_instruction.md` for information on available configs.

## Table of Contents
- **Dependencies**
  - Code
  - Repos
  - Cloudlab
- **How to Run**
    - Setup
    - Running experiment
    - Plotting
- **Experiment-Specific Instructions**
    - Fig2top
    - Fig2bottom
    - Fig3
    - Fig10
## Dependencies and Setup
### Code
- Go 1.15 (for replication protocol code)
- Python 3.10 (for running experiments automatically, calculating stats, plotting data)
    - NumPy
        - Install with ```pip install numpy```
    - PrettyTable
        - Install with ```python -m pip install -U prettytable```
    - Matplotlib
        - Install with ```pip install matplotlib```
- GNUPlot
    - See [here](https://riptutorial.com/gnuplot/example/11275/installation-or-setup) to install
### Repositories
- The Pineapple repository: ``https://github.com/tigranb2/pineapple``
- The Gus, Epaxos, and PQR repository: ``https://github.com/tigranb2/gus-epaxos``
    - Note: this implementation only sports non conflicting operations.
- The Gryff repository: ``https://github.com/tigranb2/gryff-testing``
    - Note: Both ``gryff-testing`` and ``gus-epaxos`` repositories are derived from the EPaxos repository, but have different communication between clients and servers, so it is easier to have two separate repos.
### Cloudlab Profile
It is easiest to run the experiments by used the pre-configured profile on Cloudlab, which already has all necessary repositories and dependencies installed. The profile can be instantiated [here](https://www.cloudlab.us/instantiate.php?profile=b5d01b37-541e-11ee-b28b-e4434b2381fc).

## How to Run
### Setup
1. Connect to the control machine via ssh.
``` 
ssh -i <path-to-ssh-key> -p 22 -A <root/userid>@<public dns/ip>
```
   - The final address is the address of the **CONTROL** node. 
   - Make sure to include `-A` as an ssh argument
      - This enables port forwarding and allows the control machine to run remote commands over ssh on the other replicas.
2. Open ``gus-automation`` in the control machine. This repo and others can be found in `/root/go/src`. All repos are stored in root because cloudlab disk images do not save data stored in user home directories.
```
sudo su
cd ~/go/src/gus-automation
```

3. Make sure ``gus-automation`` is up to date.
```
git pull
```
   - If this doesn't work, run ```git reset --hard LATEST_COMMIT``` where LASTEST_COMMIT is the latest commit to the repo on github to update code
4. Recompile protocol code to ensure it's updated.
```
. compile.sh
```
- Pass in ``open-loop-client`` as the first argument to compile the open-loop-client versions

### RMWFig6.json
For this experiment, use the open-loop client version of the protocols. Visit each protocol's directory and checkout the ``open-loop-client`` branch. Remember to run the ``compile.sh`` in each protocol's directory after each branch change to recompile the protocol binaries. 

All other experiments are performed on the default branch (``main``).
### Running experiment
1. Go to gus-automation:
```
cd ~/go/src/gus-automation
```
2. If CloudLab experiment has a name other than “test”, set the experiment name with:
```
python3.8 set_experiment_name.py [CLOUDLAB_EXPERIMENT_NAME]
```
3. Run an experiment with the following command, filling in the name appropriately
```
python3.8 run_experiments.py [EXPERIMENT_CONFIG_NAME]
```
- EXPERIMENT_CONFIG_NAME is the path to the config file of the experiment you would like to run 
- The result will be output to a time-stamped folder in ~/go/src/gus-automation/results.


### Plotting
To plot, you can either move the result folder onto your local machine or continue on Cloudlab.
1. Go to plotFigs folder
```
cd ~/go/src/gus-automation/plotFigs
```
2. Run the following, which will plot the data in the latest timestamp folder:
```
python3.8 plot_figs.py
```
- The plots will be in the plots folder


## Experiment-Specific Instructions
Experiments can generally be run by following the instructions in the [Running experiment](running-experiment) section, simply using the corresponding config path as the EXPERIMENT_CONFIG_NAME (e.g., configs/fig2top.json). Many experiments can be plotted following the instructions in the [Plotting](plotting) section. However, some experiments use a different plotting script. The directions for how to plot the results of these experiments can be found in the sections below.

### Fig2top
1. After running the experiment, go to results folder:
```
cd ~/go/src/gus-automation/results
```
2. Find the name of the timestamped folder from the Fig2top experiment (which needs to be the most recently run experiment) and run the following:
```
python3.8 ~/go/src/gus-automation//client_metrics.py 50 --onlytputs --path=/root/go/src/gus-automation/results/[EXPERIMENT_FOLDER_NAME]
```
  - [EXPERIMENT_FOLDER_NAME] should be replaced by the name of the folder in results containing the data from the latest Fig2top experiment that was run (e.g., 2024-08-06-14-02-50)
  - The metrics file produced by this step can be found by going to the metrics folder:
    ```
    cd ~/go/src/gus-automation/metrics
    ```
3. Once the metrics file is produced, return to gus-automation folder:
```
cd ~/go/src/gus-automation
```
4. Run the following to plot the data from the metrics file:
```
python3.8 tpt-group-bar.py
```
5. The plot produced can be found in the plots folder:
```
cd ~/go/src/gus-automation/plotFigs/plots
```

### Fig2bottom
1. Follow steps 1-3 under Fig2top, but instead in step 2 finding the timestamped folder from the Fig2bottom experiment
2. Run the following to plot the data from the metrics file:
```
python3.8 tpt-group-bar-conflict.py
```
3. The plot produced can be found in the plots folder:
```
cd ~/go/src/gus-automation/plotFigs/plots
```

### Fig3
1. After running the experiment, go to results folder:
```
cd ~/go/src/gus-automation/results
```
2. Find the name of the timestamped folder from the Fig3 experiment (which needs to be the most recently run experiment) and run the following:
```
python3.8 ~/go/src/gus-automation//client_metrics.py 50 90 --tputsLatency --path=/root/go/src/gus-automation/results/[EXPERIMENT_FOLDER_NAME]
```
  - [EXPERIMENT_FOLDER_NAME] should be replaced by the name of the folder in results containing the data from the latest Fig3 experiment that was run (e.g., 2024-08-06-14-02-50)
  - The metrics files produced by this step can be found by going to the metrics folder:
    ```
    cd ~/go/src/gus-automation/metrics
    ```
3. Once the metrics files are produced, return to gus-automation folder:
```
cd ~/go/src/gus-automation
```
4. Run the following to plot the data from the metrics files:
```
python3.8 line.py
```
5. The plots produced can be found in the plots folder:
```
cd ~/go/src/gus-automation/plotFigs/plots
```

### Fig10
1. After running the experiment, go to results folder:
```
cd ~/go/src/gus-automation/results
```
2. Find the name of the timestamped folder from the Fig10 experiment (which needs to be the most recently run experiment) and run the following:
```
python3.8 ~/go/src/gus-automation//client_metrics.py 50 --maxSums --path=/root/go/src/gus-automation/results/[EXPERIMENT_FOLDER_NAME]
```
  - [EXPERIMENT_FOLDER_NAME] should be replaced by the name of the folder in results containing the data from the latest Fig3 experiment that was run (e.g., 2024-08-06-14-02-50)
  - The metrics file produced by this step can be found by going to the metrics folder:
    ```
    cd ~/go/src/gus-automation/metrics
    ```
3. Once the metrics file is produced, return to gus-automation folder:
```
cd ~/go/src/gus-automation
```
4. Run the following to plot the data from the metrics file:
```
python3.8 plotFig10.py
```
5. The plot produced can be found in the plots folder:
```
cd ~/go/src/gus-automation/plotFigs/plots
```

----
