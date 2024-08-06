import numpy as np
import matplotlib.pyplot as plt
import json
from utils.command_util import check_cmd_output

experiment = check_cmd_output("ls results/| sort -r | head -n 1")
file = open("metrics/" + experiment + "-tpt" + ".json", 'r')
file_contents = json.load(file)

rmw = ("RMW% = 1%", "RMW% = 10%", "RMW% = 20%", "RMW% = 50%", "RMW% = 100%")
pineapple_vals = []
pqr_vals =  []
mp_vals = []
mpl_vals = []
gryff_vals = []
epaxos_vals = []

rmw_vals = ('0.01', '0.1', '0.2', '0.5', '1.0')

for rmw_val in rmw_vals:
    pineapple_vals.append(file_contents['fig2top']['pineapple-' + rmw_val]['p50.0'])
    pqr_vals.append(file_contents['fig2top']['pqr-' + rmw_val]['p50.0'])
    mp_vals.append(file_contents['fig2top']['mp-' + rmw_val]['p50.0'])
    mpl_vals.append(file_contents['fig2top']['mpl-' + rmw_val]['p50.0'])
    gryff_vals.append(file_contents['fig2top']['gryff-' + rmw_val]['p50.0'])
    epaxos_vals.append(file_contents['fig2top']['epaxos-' + rmw_val]['p50.0'])

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


plt.savefig("./plotFigs/plots/fig2top_tpt.png", bbox_inches="tight")
