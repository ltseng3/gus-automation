from run_experiment import run_experiment
import os
import subprocess
import sys
import time
import json
from update_json import update
from pathlib import Path
from setup_network_delay_test import setup_network_delay
from set_config import set_config


######### Main Script for running the experiments.  #################
# This will call all of the other scripts/function that setup nodes, 
# add latency and adjust configs.
####################################################################

# Replaces fig4 with fig4a fig4b fig4c
# def replace_fig4(config_paths):
#     last_slash_index = config_paths[0].rfind("/")
#     parent_path = config_paths[0][:last_slash_index + 1]
#
#     for config_path in config_paths:
#         if "fig4.json" in config_path:
#             # remove fig4
#             config_paths.remove(config_path)
#
#             # add fig4a fig4b fig4c
#             for x in ["a", "b", "c"]:
#                 config_paths.append(parent_path + "fig4" + x + ".json")
#
#     return config_paths


def replace_fig6(config_paths):
    last_slash_index = config_paths[0].rfind("/")
    parent_path = config_paths[0][:last_slash_index + 1]

    for config_path in config_paths:
        if "fig6.json" in config_path:
            # remove fig6
            config_paths.remove(config_path)

            # replace with fig6top fig6bottom
            for x in ["top", "bottom"]:
                config_paths.append(parent_path + "fig6" + x + ".json")

    return config_paths

def replace_fig7(config_paths):
    last_slash_index = config_paths[0].rfind("/")
    parent_path = config_paths[0][:last_slash_index + 1]

    for config_path in config_paths:
        if "fig7.json" in config_path:
            # remove fig7
            config_paths.remove(config_path)

            # replace with fig7a fig7b fig7c
            for x in ["a", "b", "c"]:
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
    # Adjusts for fig4
    # config_paths = replace_fig4(config_paths)
    config_paths = replace_fig6(config_paths)
    config_paths = replace_fig7(config_paths)
    config_paths = replace_fig8(config_paths)

    print("Here are config_paths: ", config_paths)

    # Need to adjust for figure 11 and figure 8 which just runs gus, but changes n ( =3, =5, =7, =9)
    for config_path in config_paths:

        # adjust user name
        set_config(config_path)

        # default is all protocols
        protocols = ["pqr", "pineapple", "mp", "mpl", "epaxos", "gryff"]
        # protocols = ["pqr", "pineapple", "epaxos"]
        # Figs 8 and 9 plotting is combined gus and giza only
        # if "fig9" in config_path or "fig8" in config_path:
        #     protocols = ["gus", "giza"]
        #
        # Fig 6 is only Pineapple and Gryff

        print("Config path = ", config_path)

        # Get final fig name:
        trimmed_fig = config_path.split("/")[-1].replace(".json", "")
        temp_path = results_parent_path / (trimmed_fig)

        for protocol in protocols:
            print("\nRunning", protocol, config_path, "...\n")
            update(config_path, "replication_protocol", protocol)

            results_extension = Path(temp_path) / Path(protocol)

            # For fig 6; for each protocol, change write percentage
            # if "fig6" in trimmed_fig:
            #     if protocol == "pqr":
            #         continue
            #     write_percentages = [.1, .3, .5, .7, .9]
            #     for wr in write_percentages:
            #
            #         update(config_path, "write_percentage", wr)
            #
            #         # For fig, now results file structure is: TIMESTAMP/FIG6/PROTOCOL-WRITE_PERCENTAGE/CLIENT/...
            #         results_extension_fig6 = Path(str(results_extension) + "-" + (str(wr)))
            #
            #         setup_network_delay(config_path)
            #         run_experiment(results_extension_fig6, config_path)
            # For RMWFig 6; for each protocol, change RMW percentage
            if "RMWFig6.json" in config_path:
                rmw_percentages = [.01, .1, .5, 1.0]
                for rmw in rmw_percentages:
                    update(config_path, "rmw_percentage", rmw)
                    wr = (1 - rmw) / 2  # split reads/writes evenly
                    update(config_path, "write_percentage", wr)

                    # For fig7, now results file structure is: TIMESTAMP/FIG7/PROTOCOL-RMW_PERCENTAGE/CLIENT/...
                    results_extension_RMWfig6 = Path(str(results_extension) + "-" + (str(rmw)))

                    setup_network_delay(config_path)
                    run_experiment(results_extension_RMWfig6, config_path)
            if "RMWFig6-5.json" in config_path:
                rmw_percentages = [.01, .1, .5, 1.0]
                for rmw in rmw_percentages:
                    update(config_path, "rmw_percentage", rmw)
                    wr = (1 - rmw) / 2  # split reads/writes evenly
                    update(config_path, "write_percentage", wr)

                    # For fig7, now results file structure is: TIMESTAMP/FIG7/PROTOCOL-RMW_PERCENTAGE/CLIENT/...
                    results_extension_RMWfig6_5 = Path(str(results_extension) + "-" + (str(rmw)))

                    setup_network_delay(config_path)
                    run_experiment(results_extension_RMWfig6_5, config_path)
            # For gryffFig 11; for each protocol, change tail-at-scale value
            elif "gryffFig11.json" in config_path:
                tas_values = [1, 15, 30, 45, 60, 75, 90, 105]
                for tas in tas_values:
                    update(config_path, "tail_at_scale", tas)

                    results_extension_gryffFig11 = Path(str(results_extension) + "-" + (str(tas)))

                    setup_network_delay(config_path)
                    run_experiment(results_extension_gryffFig11, config_path)
            # This is the Cloudlab experiment that should really be run with 3 and 5 replicas
            elif "fig8n5.json" in config_path:

                num_replicas = [3, 5]

                for n in num_replicas:
                    update(config_path, "number_of_replicas", n)

                    # For fig 8, now results file stricture is: TIMESTAMP/FIG8/PROTOCOL-NUM_REPLICAS/CLIENT/...
                    results_extension_fig8 = Path(str(results_extension) + "-" + (str(n)))

                    setup_network_delay(config_path)
                    run_experiment(results_extension_fig8, config_path)

            # For fig8 and fig11 This is the Cloudlab experiment that should really be run with 7 and 9 replicas
            # elif "fig8" in config_path or "fig11" in config_path:
            #     num_replicas = [7, 9]
            #
            #     for n in num_replicas:
            #         update(config_path, "number_of_replicas", n)
            #
            #         # For fig 8 or fig 11, now results file stricture is: TIMESTAMP/FIG#/PROTOCOL-NUM_REPLICAS/CLIENT/...
            #         results_extension_add = Path(str(results_extension) + "-" + (str(n)))
            #
            #         setup_network_delay(config_path)
            #         run_experiment(results_extension_add, config_path)

            # for fig9, data size is altered between trials
            elif "fig9" in config_path:
                sizes = [4000, 40000, 400000, 4000000]  # size of data packets in MB

                for size in sizes:
                    update(config_path, "size", size)

                    # For fig9, now results file structure is TIMESTAMP/FIG9/PROTOCL-size/Client ...
                    results_extension_add = Path(str(results_extension) + "-" + (str(size)))

                    setup_network_delay(config_path)
                    run_experiment(results_extension_add, config_path)
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
