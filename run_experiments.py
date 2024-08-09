from run_experiment import run_experiment
import os
import subprocess
import sys
import time
import json
from update_json import update
from update_json import updateLatencies3
from update_json import updateLatencies5
from pathlib import Path
from setup_network_delay_test import setup_network_delay
from set_config import set_config


######### Main Script for running the experiments.  #################
# This will call all of the other scripts/function that setup nodes,
# add latency and adjust configs.
####################################################################

def replace_fig4(config_paths):
    last_slash_index = config_paths[0].rfind("/")
    parent_path = config_paths[0][:last_slash_index + 1]

    for config_path in config_paths:
        if "fig4.json" in config_path:
            # remove fig4
            config_paths.remove(config_path)

            # add fig4top fig4bottom
            for x in ["top", "bottom"]:
                config_paths.append(parent_path + "fig4" + x + ".json")

    return config_paths

def replace_fig5(config_paths):
    last_slash_index = config_paths[0].rfind("/")
    parent_path = config_paths[0][:last_slash_index + 1]

    for config_path in config_paths:
        if "fig5.json" in config_path:
            # remove fig5
            config_paths.remove(config_path)

            # add fig5a fig5b fig5c
            for x in ["a", "b", "c"]:
                config_paths.append(parent_path + "fig5" + x + ".json")
    return config_paths

def replace_fig7(config_paths):
    last_slash_index = config_paths[0].rfind("/")
    parent_path = config_paths[0][:last_slash_index + 1]

    for config_path in config_paths:
        if "fig7.json" in config_path:
            # remove fig7
            config_paths.remove(config_path)

            # add fig7top fig7bottom
            for x in ["top", "bottom"]:
                config_paths.append(parent_path + "fig7" + x + ".json")

    return config_paths

def replace_fig8(config_paths):
    last_slash_index = config_paths[0].rfind("/")
    parent_path = config_paths[0][:last_slash_index + 1]

    for config_path in config_paths:
        if "fig8.json" in config_path:
            # remove fig6
            config_paths.remove(config_path)

            # replace with fig8top fig8bottom
            for x in ["top", "bottom"]:
                config_paths.append(parent_path + "fig8" + x + ".json")

    return config_paths

def run():
    now_string = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())

    parent_path = Path("/root/go/src/gus-automation/")

    base_config_file = open("configs/config.json")

    base_config = json.load(base_config_file)

    results_parent_path = Path(base_config["base_control_experiment_directory"]) / now_string

    config_paths = sys.argv[1:]

    config_paths = replace_fig4(config_paths)
    config_paths = replace_fig5(config_paths)
    config_paths = replace_fig7(config_paths)
    config_paths = replace_fig8(config_paths)

    print("Here are config_paths: ", config_paths)

    # Need to adjust for figure 11 and figure 8 which just runs gus, but changes n ( =3, =5, =7, =9)
    for config_path in config_paths:

        # adjust user name
        set_config(config_path)

        # default is all protocols
        protocols = ["pqr", "pineapple", "mp", "mpl", "epaxos", "gryff"]

        print("Config path = ", config_path)

        # Get final fig name:
        trimmed_fig = config_path.split("/")[-1].replace(".json", "")
        temp_path = results_parent_path / (trimmed_fig)

        for protocol in protocols:
            if "fig10.json" in config_path:
                # gryff is not run for fig10
                if protocol == "gryff":
                    continue
                else:
                    print("\nRunning", protocol, config_path, "...\n")
                    # change replication protocol to the WAN version (affects command_util.py)
                    update(config_path, "replication_protocol", "WAN-" + protocol)
                    numClients = 1;
                    # hard-coded client values for fig10
                    # NOT FINALIZED
                    # may need to be tweaked
                    # also may need to change line 135 in ~/src/gus-epaxos/src/clientWAN/clientWAN.go to have the value of id be lower than 10000
                    # see this doc for test results, some with this value varied: https://docs.google.com/spreadsheets/d/1oZv0o1yT4O1DVXK8TLS4Rkkbs3HNMyvcCTludUltKdU/edit?gid=2059564213#gid=2059564213
                    if protocol == "pqr":
                        numClients = 128;
                    elif protocol == "pineapple":
                        numClients = 250;
                    elif protocol == "mp":
                        numClients = 15;
                    elif protocol == "mpl":
                        numClients = 150;
                    elif protocol == "epaxos":
                        numClients = 20;

                    update(config_path, "clients_per_replica", numClients)
            else:
                print("\nRunning", protocol, config_path, "...\n")
                update(config_path, "replication_protocol", protocol)

            results_extension = Path(temp_path) / Path(protocol)

            if "fig2top.json" in config_path:
                print("about to run fig2top")
                # make sure tpt-group-bar.py has matching labels to these values for plotting
                rmw_percentages = [.01, .1, .2, .5, 1.0]
                for rmw in rmw_percentages:
                    update(config_path, "rmw_percentage", rmw)
                    wr = (1 - rmw) / 2  # split reads/writes evenly
                    update(config_path, "write_percentage", wr)

                    # For fig2top, now results file structure is: TIMESTAMP/FIG2TOP/PROTOCOL-RMW_PERCENTAGE/CLIENT/...
                    results_extension_fig2top = Path(str(results_extension) + "-" + (str(rmw)))

                    setup_network_delay(config_path)
                    run_experiment(results_extension_fig2top, config_path)
            elif "fig2bottom.json" in config_path:
                # make sure tpt-group-bar-conflict.py has matching labels to these values for plotting
                conflict_percentages = [2, 25, 50, 75, 100]
                for conflict in conflict_percentages:
                    update(config_path, "conflict_percentage", conflict)

                    # For fig2bottom, now results file structure is: TIMESTAMP/FIG2BOTTOM/PROTOCOL-CONFLICT_PERCENTAGE/CLIENT/...
                    results_extension_fig2bottom = Path(str(results_extension) + "-" + (str(conflict)))

                    setup_network_delay(config_path)
                    run_experiment(results_extension_fig2bottom, config_path)
            elif "fig3.json" in config_path:
                # check fig3.json for experiment_length: 180 fills up disk space on c6525-25g machines at least sometimes, so if that happens you may want to lower it (90 and 30 both should not have issues)
                # make sure line.py has matching labels to these values for plotting
                num_clients = [3, 10, 20, 30, 40, 50, 60, 70]
                for num_client in num_clients :
                    update(config_path, "clients_per_replica", num_client)

                    # For fig3, now results file structure is: TIMESTAMP/FIG3/PROTOCOL-NUM_CLIENT/CLIENT/...
                    results_extension_fig3 = Path(str(results_extension) + "-" + (str(num_client)))

                    setup_network_delay(config_path)
                    run_experiment(results_extension_fig3, config_path)
            elif "fig10.json" in config_path:
                # updateLatencies5 and updateLatencies3 in update_json.py make sure there are the correct
                # number of replicas and the correct latencies dependent on the given leader, in this case
                # so that fig4top, fig4bottom, fig7top, and fig7botto can have the correct setups with only
                # one config to run them all

                updateLatencies5(config_path, "ireland")
                results_extension_fig10 = Path(str(results_extension) + "-fig7top")
                setup_network_delay(config_path)
                run_experiment(results_extension_fig10, config_path)

                update(config_path, "conflict_percentage", 25)
                results_extension_fig10 = Path(str(results_extension) + "-fig7bottom")
                setup_network_delay(config_path)
                run_experiment(results_extension_fig10, config_path)

                updateLatencies3(config_path, "virginia")
                results_extension_fig10 = Path(str(results_extension) + "-fig4bottom")
                setup_network_delay(config_path)
                run_experiment(results_extension_fig10, config_path)

                update(config_path, "conflict_percentage", 2)
                results_extension_fig10 = Path(str(results_extension) + "-fig4top")
                setup_network_delay(config_path)
                run_experiment(results_extension_fig10, config_path)
            else:
                setup_network_delay(config_path)
                run_experiment(results_extension, config_path)

# Must be run as:
# python run_n_experiments <config#> <config#> ...
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: python3 run_n_experiments <fig#> <fig#> ...\n')
        sys.exit(1)

    run()
