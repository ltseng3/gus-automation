import numpy as np
import matplotlib.pyplot as plt
import json
from utils.command_util import check_cmd_output

# load data from the latest experiment's metrics throughput and latency files
experiment = check_cmd_output("ls results/| sort -r | head -n 1")
file_latency = open("metrics/" + experiment + "-latency" + ".json", 'r')
file_latency_contents = json.load(file_latency)
file_tpt = open("metrics/" + experiment + "-tpt" + ".json", 'r')
file_tpt_contents = json.load(file_tpt)

# Clients: 3, 10, 20, 30, 40, 50, 60, 70
pineappley50 = []
pineappley90 = []
pineapplex = []

pqry50 = []
pqry90 = []
pqrx = []

gryffy50 = []
gryffy90 = []
gryffx = []

epaxosy50 = []
epaxosy90 = []
epaxosx = []

mpaxosy50 = []
mpaxosy90 = []
mpaxosx = []

mpaxosly50 = []
mpaxosly90 = []
mpaxoslx = []


# make sure these labels match the client values in run_experiments.py
clients = ('3', '10', '20', '30', '40', '50', '60', '70')

# grab p50.0 and p90.0 throughput data from throughput file as y-axis data if it exists for each figure
# (sometimes some data is not received and the throughput for some systems is missing, in which case, the value 0 will be used for plotting)
# grab latency data from latency file as x-axis data
for client in clients:
    if 'total_protocol_data' in file_latency_contents['fig3']['pineapple-' + client]:
        pineappley50.append(file_latency_contents['fig3']['pineapple-' + client]['total_protocol_data']['p50.0'])
        pineappley90.append(file_latency_contents['fig3']['pineapple-' + client]['total_protocol_data']['p90.0'])
    else:
        pineappley50.append(0.0)
        pineappley90.append(0.0)
    pineapplex.append(file_tpt_contents['fig3']['pineapple-' + client]['mean'])

    if 'total_protocol_data' in file_latency_contents['fig3']['pqr-' + client]:
        pqry50.append(file_latency_contents['fig3']['pqr-' + client]['total_protocol_data']['p50.0'])
        pqry90.append(file_latency_contents['fig3']['pqr-' + client]['total_protocol_data']['p90.0'])
    else:
        pqry50.append(0.0)
        pqry90.append(0.0)
    pqrx.append(file_tpt_contents['fig3']['pqr-' + client]['mean'])

    if 'total_protocol_data' in file_latency_contents['fig3']['mp-' + client]:
        mpaxosy50.append(file_latency_contents['fig3']['mp-' + client]['total_protocol_data']['p50.0'])
        mpaxosy90.append(file_latency_contents['fig3']['mp-' + client]['total_protocol_data']['p90.0'])
    else:
        mpaxosy50.append(0.0)
        mpaxosy90.append(0.0)
    mpaxosx.append(file_tpt_contents['fig3']['mp-' + client]['mean'])

    if 'total_protocol_data' in file_latency_contents['fig3']['mpl-' + client]:
        mpaxosly50.append(file_latency_contents['fig3']['mpl-' + client]['total_protocol_data']['p50.0'])
        mpaxosly90.append(file_latency_contents['fig3']['mpl-' + client]['total_protocol_data']['p90.0'])
    else:
        mpaxosly50.append(0.0)
        mpaxosly90.append(0.0)
    mpaxoslx.append(file_tpt_contents['fig3']['mpl-' + client]['mean'])

    if 'total_protocol_data' in file_latency_contents['fig3']['gryff-' + client]:
        gryffy50.append(file_latency_contents['fig3']['gryff-' + client]['total_protocol_data']['p50.0'])
        gryffy90.append(file_latency_contents['fig3']['gryff-' + client]['total_protocol_data']['p90.0'])
    else:
        gryffy50.append(0.0)
        gryffy90.append(0.0)
    gryffx.append(file_tpt_contents['fig3']['gryff-' + client]['mean'])

    if 'total_protocol_data' in file_latency_contents['fig3']['epaxos-' + client]:
        epaxosy50.append(file_latency_contents['fig3']['epaxos-' + client]['total_protocol_data']['p50.0'])
        epaxosy90.append(file_latency_contents['fig3']['epaxos-' + client]['total_protocol_data']['p90.0'])
    else:
        epaxosy50.append(file_latency_contents['fig3']['epaxos-' + client]['total_protocol_data']['p50.0'])
        epaxosy90.append(file_latency_contents['fig3']['epaxos-' + client]['total_protocol_data']['p90.0'])
    epaxosx.append(file_tpt_contents['fig3']['epaxos-' + client]['mean'])

#fig = plt.figure(figsize = (10, 3))

fig, ax = plt.subplots(figsize = (6, 2))

#fig.set_figheight(3)
#fig.set_figwidth(10)

ax.plot(pineapplex, pineappley50, color='orange', linestyle="solid", label="Pineapple")
ax.plot(pqrx, pqry50, color='blue', linestyle="dotted", label="PQR")
ax.plot(mpaxosx,mpaxosy50, color='black', linestyle="dotted", label="MPaxos")
ax.plot(mpaxoslx,mpaxosly50, color='brown', linestyle="dotted", label="MPaxos(L")
ax.plot(gryffx,gryffy50, color='green', linestyle="dashdot", label="Gryff")
ax.plot(epaxosx,epaxosy50, color='red', linestyle="dashed", label="EPaxos")
ax.set_ylabel("p50 Latency (ms)")

ax.set_xlim(left=0)
# ax.set_ylim(top=50)
ax.set_xlabel("Throughput (Ops/sec)")
ax.legend(('Pineapple', 'Gryff', 'EPaxos', 'MPaxos', 'MPaxos(L)'))
# ax.legend(loc='upper left', ncols=6)
ax.legend(loc='upper left', ncols=1)
# plt.show()

fig.savefig("./plotFigs/plots/fig3left_p50.png", bbox_inches="tight")

ax.cla()

ax.plot(pineapplex, pineappley90, color='orange', linestyle="solid", label="Pineapple")
ax.plot(pqrx, pqry90, color='blue', linestyle="dotted", label="PQR")
ax.plot(mpaxosx,mpaxosy90, color='black', linestyle="dotted", label="MPaxos")
ax.plot(mpaxoslx,mpaxosly90, color='brown', linestyle="dotted", label="MPaxos(L)")
ax.plot(gryffx,gryffy90, color='green', linestyle='dashdot', label="Gryff")
ax.plot(epaxosx,epaxosy90, color='red', linestyle='dashed', label="EPaxos")
ax.set_ylabel("p90 Latency (ms)")

ax.set_xlim(left=0)
# ax.set_ylim(top=50)
ax.set_xlabel("Throughput (Ops/sec)")
ax.legend(('Pineapple', 'Gryff', 'EPaxos', 'MPaxos', 'MPaxos(L)'))
# ax.legend(loc='upper left', ncols=6)
ax.legend(loc='upper left', ncols=1)
# plt.show()

fig.savefig("./plotFigs/plots/fig3right_p90.png", bbox_inches="tight")
