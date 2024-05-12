from update_json import update
import os
import sys

# Goes into config files and adjusts Cloudlab experiment name
def set_experiment_name(name):
    # Assumes all config files are in config dir
    configs = os.listdir("configs")

    for config in configs:
        if config == "legacy": # Ignores the legacy directory
            continue
        path = "configs/" + config
        update(path, "experiment_name", name)
    
    # Handles renaming experiments in the legacy directory
    # Written to adhere to the coding style of the rest of the script
    legacies = os.listdir("configs/legacy")

    for legacy in legacies:
        path = "configs/legacy/" + legacy
        update(path, "experiment_name", name)
    
def usage():
    print("Usage: python3 set_experiment_name.py NEW_NAME")

if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage()
    else:
        set_experiment_name(sys.argv[1])