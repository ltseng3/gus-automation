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
            print("\nRunning", protocol, config_path, "...\n")
            update(config_path, "replication_protocol", protocol)

            results_extension = Path(temp_path) / Path(protocol)

            setup_network_delay(config_path)
            run_experiment(results_extension, config_path)

# Must be run as:
# python run_n_experiments <config#> <config#> ...
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: python3 run_n_experiments <fig#> <fig#> ...\n')
        sys.exit(1)

    run()
