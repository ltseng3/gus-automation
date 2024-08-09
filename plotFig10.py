import numpy as np
import matplotlib.pyplot as plt
import json
from utils.command_util import check_cmd_output

# load data from the latest experiment's metrics file
experiment = check_cmd_output("ls results/| sort -r | head -n 1")
file = open("metrics/" + experiment + "-maxSums" + ".json", 'r')
file_contents = json.load(file)

fig_names = ("Fig4top", "Fig4bottom", "Fig7top", "Fig7bottom")
pineapple_vals = []
pqr_vals =  []
mp_vals = []
mpl_vals = []
epaxos_vals = []

figs = ('fig4top', 'fig4bottom', 'fig7top', 'fig7bottom')

# Currently, the sum of the max value in each lattput file is used for mp and epaxos for fig10
# while pineapple, pqr, and mpl are not summed and simply use the "normal" method of calculation
# in client_metrics.py. Sections of code are commented out with instructions on what to uncomment
# and what to comment to switch to getting the max sum of pqr and mpl. Similar code can be used to
# get the max sum for pineapple if that is desired
print("")
print("Note: maxSums except for pineapple, pqr, and mpl")
print("")

for figure in figs:
    print("-----" + figure + "-----")

    # non-maxSum pineapple
    print("pineapple: " + str(file_contents['fig10']['pineapple-' + figure]['tput']['p50.0']))
    pineapple_vals.append(file_contents['fig10']['pineapple-' + figure]['tput']['p50.0'])

    numFiles = 3
    if figure == "fig7top" or figure == 'fig7bottom':
        numFiles = 5

    # comment this section to get maxSum of pqr
    print("pqr: " + str(file_contents['fig10']['pqr-' + figure]['tput']['p50.0']))
    pqr_vals.append(file_contents['fig10']['pqr-' + figure]['tput']['p50.0'])

    # uncomment this section to get maxSum of pqr
    #maxSum = 0.0
    #for i in range(0, numFiles):
    #    if file_contents['fig10']['pqr-' + figure].get('lattput-' + str(i) + '.txt') is not None:
    #        maxSum += file_contents['fig10']['pqr-' + figure]['lattput-' + str(i) + '.txt']['max']
    #print("pqr: " + str(maxSum))
    #pqr_vals.append(maxSum)

    # maxSum mp
    maxSum = 0.0
    for i in range(0, numFiles):
        if file_contents['fig10']['mp-' + figure].get('lattput-' + str(i) + '.txt') is not None:
            maxSum += file_contents['fig10']['mp-' + figure]['lattput-' + str(i) + '.txt']['max']
    print("mp: " + str(maxSum))
    mp_vals.append(maxSum)

    # comment this section to get maxSum of mpl
    print("mpl: " + str(file_contents['fig10']['mpl-' + figure]['tput']['p50.0']))
    mpl_vals.append(file_contents['fig10']['mpl-' + figure]['tput']['p50.0'])

    # uncomment this section to get maxSum of mpl
    #maxSum = 0.0
    #for i in range(0, numFiles):
    #    if file_contents['fig10']['mpl-' + figure].get('lattput-' + str(i) + '.txt') is not None:
    #        maxSum += file_contents['fig10']['mpl-' + figure]['lattput-' + str(i) + '.txt']['max']
    #print("mpl: " + str(maxSum))
    #mpl_vals.append(maxSum)

    # maxSum epaxos
    maxSum = 0.0
    for i in range(0, numFiles):
        if file_contents['fig10']['epaxos-' + figure].get('lattput-' + str(i) + '.txt') is not None:
            maxSum += file_contents['fig10']['epaxos-' + figure]['lattput-' + str(i) + '.txt']['max']
    print("epaxos: " + str(maxSum))
    epaxos_vals.append(maxSum)

    print("")

protocol = {
    'Pineapple': tuple(pineapple_vals),
    'PQR': tuple(pqr_vals),
    'MPaxos': tuple(mp_vals),
    'MPaxos(L)': tuple(mpl_vals),
    'EPaxos': tuple(epaxos_vals),
}

x = np.arange(len(fig_names))  # the label locations
width = 0.15  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout="constrained", figsize = (15, 2))



for attribute, measurement in protocol.items():
    offset = width * multiplier
    if attribute == 'Pineapple':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='orange', hatch='-')
    if attribute == 'PQR':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='blue', hatch='o')
    if attribute == 'MPaxos':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='black', hatch='O')
    if attribute == 'MPaxos(L)':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='brown', hatch='.')
    if attribute == 'EPaxos':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='red', hatch='\\')
    # ax.bar_label(rects, padding=3)
    multiplier += 1

# for x in range(2):
#     rects[6*x].set_color('orange')
#     rects[6*x+1].set_color('blue')
    # rects[6*x+2].set_color('green')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Throughput (Ops/sec)')
#ax.set_title('Penguin attributes by species')
ax.set_xticks(x + width, fig_names)
ax.legend(loc='upper right', ncols=6)
#ax.set_ylim(0, 62000)
ax.set_ylim(0, 150000)
ax.yaxis.grid(True, color='#EEEEEE')
ax.set_axisbelow(True)
# plt.show()


plt.savefig("./plotFigs/plots/fig10.png", bbox_inches="tight")
