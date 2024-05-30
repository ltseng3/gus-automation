import os
import subprocess
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pathlib import Path
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import FixedLocator, FuncFormatter

### Helper functions for plotting ###

# Defining lines and colors
colors = {"gryff":"green", "pineapple":"orange", "pqr":"blue", "epaxos":"red", "mp":"black", "mpl":"brown"}
linestyles = {"gryff":"dashdot", "pineapple":"solid", "pqr":"dotted", "epaxos":"dashed", "mp":"dotted", "mpl":"dotted"}
labels = {"gryff":"Gryff", "pineapple":"Pineapple", "pqr":"PQR", "epaxos":"EPaxos", "mp":"MPaxos", "mpl":"MPaxos(L)"} # properly stylized
markers ={"gryff":"v", "pineapple": "o"}

# New in development version with matplotlib
def cdf_csvs_to_plot(plot_target_directory, figure, csvs, is_for_reads, rmw=False, log=False):
    # Reformat function header to just pass csvs dictionary
    # csvs = {"gus": gus_csv, "gryff":gryff_csv, "epaxos":epaxos_csv}
    print("csvs = " , csvs)

    # Each data object is a np array. 1st column is x data (latency), 2nd column is y data (percentile). label is the protocol
    # Creates data dictionary from csvs dictionary. Exclude anything beyond first two columns
    data = {protocol: np.genfromtxt(csv, delimiter=',', usecols=np.arange(0,2)) for protocol, csv in csvs.items()}

    fig, ax = plt.subplots()

    # sizing and margins
    fig.set_figheight(1.5)
    fig.set_figwidth(6)

    # d is data (singular)
    for protocol, d in data.items():
        print("d = ", d)
        ax.plot(d[:,0], d[:,1], color=colors[protocol], linestyle=linestyles[protocol], label=labels[protocol])

    # log settings
    if log == True:
        ax.set_yscale('log')
        ax.set_ylim(bottom=(0.1 * 6))
        ax.set_ylim(top=1.1)
        ax.set_xlim(left=250)
        ax.set_xlim(right=550)
    else:
        ax.set_xlim(left=0)

    # Adding labels
    ax.set_xlabel('Latency (ms)')

    if is_for_reads:
        ax.set_ylabel('Fraction of Reads')
    elif rmw:
        ax.set_ylabel('Fraction of RMW')
    else:
        ax.set_ylabel('Fraction of Writes')

    fig.savefig(plot_target_directory / Path(figure + ".png") , bbox_inches="tight")


# Used for figure 6 - new version of plotting with matplotlib
# throughputs is a dictionary indexed via: thoughputs[protocol][wp]
def tput_wp_plot(plot_target_directory, figure, throughputs, rmw=False):

    fig, ax = plt.subplots()

    # sizing and margins
    fig.set_figheight(1.5)
    fig.set_figwidth(6)
    ax.margins(x=0.01)

    print("throughputs = ", throughputs)

    # d is data
    for protocol, d  in throughputs.items():
        d = d[d[:,0].argsort()]  # sort the data before plotting
        ax.plot(d[:,0], d[:,1], color=colors[protocol], linestyle=linestyles[protocol], label=labels[protocol])

    if rmw:
        ax.set_xlabel("RMW Percentage")
    else:
        ax.set_xlabel("Write Percentage")
    ax.set_ylabel("Throughput (ops/s)")
    ax.set_ylim(bottom=0)

    ax.legend()

    fig.savefig(plot_target_directory / Path(figure + ".png") , bbox_inches="tight")


# Used for figure 6 - new version of plotting with matplotlib
# throughputs is a dictionary indexed via: thoughputs[protocol][wp]
def max_tas_plot(plot_target_directory, figure, max_lats):
    fig, ax = plt.subplots()

    # sizing and margins
    fig.set_figheight(1.2)
    fig.set_figwidth(6)
    ax.margins(x=0.01)

    print("max latencies = ", max_lats)

    # d is data
    for protocol, d  in max_lats.items():
        d = d[d[:,0].argsort()]  # sort the data before plotting
        ax.plot(d[:,0], d[:,1], color=colors[protocol], linestyle=linestyles[protocol], label=labels[protocol], marker=markers[protocol])

    ax.set_xlabel("# of subrequests")
    ax.set_ylabel("p50 Latency (ms)")
    ax.set_ylim(bottom=0)
    ax.set_ylim(top=150)
    ax.set_xlim(left=0)
    ax.set_xlim(right=105)

    ax.legend(loc="lower right")

    fig.savefig(plot_target_directory / Path(figure + ".png") , bbox_inches="tight")
