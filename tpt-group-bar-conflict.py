import numpy as np
import matplotlib.pyplot as plt
import json
from utils.command_util import check_cmd_output

# load data from the latest experiment's metrics file
experiment = check_cmd_output("ls results/| sort -r | head -n 1")
file = open("metrics/" + experiment + "-tpt" + ".json", 'r')
file_contents = json.load(file)

rmw = ("Conflict% = 2%", "Conflict% = 25%", "Conflict% = 50%", "Conflict% = 75%", "Conflict% = 100%")
pineapple_vals = []
pqr_vals =  []
mp_vals = []
mpl_vals = []
gryff_vals = []
epaxos_vals = []

# make sure these labels match the conflict values in run_experiments.py
conflicts = ('2', '25', '50', '75', '100')

# grab throughput data from metrics file
for conflict in conflicts:
    pineapple_vals.append(file_contents['fig2bottom']['pineapple-' + conflict]['p50.0'])
    pqr_vals.append(file_contents['fig2bottom']['pqr-' + conflict]['p50.0'])
    mp_vals.append(file_contents['fig2bottom']['mp-' + conflict]['p50.0'])
    mpl_vals.append(file_contents['fig2bottom']['mpl-' + conflict]['p50.0'])
    gryff_vals.append(file_contents['fig2bottom']['gryff-' + conflict]['p50.0'])
    epaxos_vals.append(file_contents['fig2bottom']['epaxos-' + conflict]['p50.0'])

protocol = {
    'Pineapple': tuple(pineapple_vals),
    'PQR': tuple(pqr_vals),
    'MPaxos': tuple(mp_vals),
    'MPaxos(L)': tuple(mpl_vals),
    'Gryff': tuple(gryff_vals),
    'EPaxos': tuple(epaxos_vals),
}

x = np.arange(len(rmw))  # the label locations
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
    if attribute == 'Gryff':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='green', hatch='/')
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
ax.set_xticks(x + width, rmw)
ax.legend(loc='upper right', ncols=6)
ax.set_ylim(0, 62000)
ax.yaxis.grid(True, color='#EEEEEE')
ax.set_axisbelow(True)
# plt.show()


plt.savefig("./plotFigs/plots/fig2bottom_tpt.png", bbox_inches="tight")
