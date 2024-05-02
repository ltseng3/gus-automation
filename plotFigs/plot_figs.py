from folder_to_norm_latencies import extract_norm_latencies
from extract_latencies import extract_latencies
from latencies_to_csv import latencies_to_csv
from csvs_to_plot import cdf_csvs_to_plot, tput_wp_plot, max_tas_plot
import os
from pathlib import Path
import sys
import subprocess
import json
import numpy as np


########## PRIMARY PLOTTING CODE ############
# This Code plots figures 4,5,6, and 9 and gives directions how to produce other figures


# File path has structure: TIMESTAMP / FIG# / PROTOCOL/ CLIENT
# Make sure to run when current wording directory is plot_figs/
def main(results_path):
    plot_target_directory = Path("plots")
    csv_target_directory = Path("csvs")

    # list all figs in timestap
    figs = os.listdir(results_path)
    for fig in figs:
        fig_path = Path(results_path) / Path(fig)

        protocols = os.listdir(fig_path)
        latencies_folder_paths = {}
        for protocol in protocols:
            latencies_folder_path = fig_path / Path(protocol + "/client")
            latencies_folder_paths[protocol] = latencies_folder_path

        if "epaxos" not in latencies_folder_paths:
            latencies_folder_paths["epaxos"] = ""

        if fig == "fig4a":
            print("Plotting fig4a...")
            plot_fig4(plot_target_directory, csv_target_directory, "4a", latencies_folder_paths["gryff"],
                      latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"])
        elif fig == "fig4b":
            print("Plotting fig4b...")
            plot_fig4(plot_target_directory, csv_target_directory, "4b", latencies_folder_paths["gryff"],
                      latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"])
        elif fig == "fig4c":
            print("Plotting fig4c...")
            plot_fig4(plot_target_directory, csv_target_directory, "4c", latencies_folder_paths["gryff"],
                      latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"])
        elif fig == "fig5":
            print("Plotting fig5...")
            plot_fig5(plot_target_directory, csv_target_directory, latencies_folder_paths["gryff"],
                      latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"])
        # elif fig == "fig6":
        #     print("Plotting fig6...")
        #     plot_fig6(plot_target_directory, results_path, csv_target_directory, latencies_folder_paths)
        # elif fig == "fig7":
        #     print(
        #         "Separate from automated plotting. Latencies were originanlly manually extracted. Use layered/plot.py")
        # elif fig == "fig8":
        #     print(
        #         "Plot was produced manually through extracting latencies from each sub experiment, finding percentiles and plotting")
        elif fig == "fig9":
            print("Plotting fig9...")
            plot_fig9(plot_target_directory, csv_target_directory, latencies_folder_paths["gryff"],
                      latencies_folder_paths["pineapple"])
        elif fig == "fig11":
            # Old fig12 and fig12 n=5
            print("Seperate from automated plotting. Use scale/scale_plot.py. See README for details")
        elif fig == "fig6top":
            print("Plotting fig6top...")
            plot_fig6(plot_target_directory, csv_target_directory, "fig6top", latencies_folder_paths["gryff"],
                           latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"], latencies_folder_paths["mp"], latencies_folder_paths["mpl"])
        elif fig == "fig6bottom":
            print("Plotting fig6bottom...")
            plot_fig6(plot_target_directory, csv_target_directory, "fig6bottom", latencies_folder_paths["gryff"],
                           latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"], latencies_folder_paths["mp"], latencies_folder_paths["mpl"])
        elif fig == "fig6top-VA":
            print("Plotting fig6top...")
            plot_fig6(plot_target_directory, csv_target_directory, "fig6top", latencies_folder_paths["gryff"],
                           latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"], latencies_folder_paths["mp"], latencies_folder_paths["mpl"])
        elif fig == "fig6bottom-VA":
            print("Plotting fig6bottom...")
            plot_fig6(plot_target_directory, csv_target_directory, "fig6bottom", latencies_folder_paths["gryff"],
                           latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"], latencies_folder_paths["mp"], latencies_folder_paths["mpl"])
        elif fig == "fig7a": # can re-use plot_fig6
            print("Plotting fig7a...")
            plot_fig6(plot_target_directory, csv_target_directory, "fig7a", latencies_folder_paths["gryff"],
                           latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"], latencies_folder_paths["mp"], latencies_folder_paths["mpl"])
        elif fig == "fig7b":
            print("Plotting fig7b...")
            plot_fig6(plot_target_directory, csv_target_directory, "fig7b", latencies_folder_paths["gryff"],
                           latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"], latencies_folder_paths["mp"], latencies_folder_paths["mpl"])
        elif fig == "fig7c":
            print("Plotting fig7c...")
            plot_fig6(plot_target_directory, csv_target_directory, "fig7c", latencies_folder_paths["gryff"],
                           latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"], latencies_folder_paths["mp"], latencies_folder_paths["mpl"])
        elif fig == "fig8top":
            print("Plotting fig8top...")
            plot_fig8(plot_target_directory, csv_target_directory, "fig8top", latencies_folder_paths["gryff"],
                           latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"], latencies_folder_paths["mp"], latencies_folder_paths["mpl"])
        elif fig == "fig8bottom":
            print("Plotting fig8bottom...")
            plot_fig8(plot_target_directory, csv_target_directory, "fig8bottom", latencies_folder_paths["gryff"],
                           latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"], latencies_folder_paths["mp"], latencies_folder_paths["mpl"])
        # elif fig == "gryffFig6a":
        #     print("Plotting gryffFig6a...")
        #     plot_gryffFig6(plot_target_directory, csv_target_directory, "gryff6a", latencies_folder_paths["gryff"],
        #                    latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"])
        # elif fig == "gryffFig6b":
        #     print("Plotting gryffFig6b...")
        #     plot_gryffFig6(plot_target_directory, csv_target_directory, "gryff6b", latencies_folder_paths["gryff"],
        #                    latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"])
        # elif fig == "gryffFig6c":
        #     print("Plotting gryffFig6c...")
        #     plot_gryffFig6(plot_target_directory, csv_target_directory, "gryff6c", latencies_folder_paths["gryff"],
        #                    latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"])
        elif fig == "gryffFig8":
            print("Plotting gryffFig8...")
            plot_gryffFig8(plot_target_directory, csv_target_directory, latencies_folder_paths["gryff"],
                           latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"])
        # elif fig == "gryffFig9":
        #     print("Plotting gryffFig9...")
        #     plot_gryffFig9(plot_target_directory, csv_target_directory, latencies_folder_paths["gryff"],
        #                    latencies_folder_paths["pineapple"], latencies_folder_paths["pqr"], latencies_folder_paths["epaxos"])
        elif fig == "gryffFig11":
            print("Plotting gryffFig11...")
            plot_gryffFig11(plot_target_directory, results_path, csv_target_directory, latencies_folder_paths)
        elif fig == "RMWFig6":
            print("Plotting RMWFig6...")
            plot_RMWFig6(plot_target_directory, results_path, csv_target_directory, latencies_folder_paths)

        else:
            print("Default reached, Plotting Case not found")


def plot_fig5(plot_target_directory, csv_target_directory, gryff_latency_folder, pineapple_latency_folder,
              pqr_latency_folder):
    # gryff_fig_csvs, gus_fig_csvs, epaxos_fig_csvs = calculate_fig_5_csvs(csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder)
    read_csvs, write_csvs, _, _ = calculate_csvs_cdf("5", csv_target_directory, gryff_latency_folder,
                                                     pineapple_latency_folder, pqr_latency_folder)

    # Reads
    cdf_csvs_to_plot(plot_target_directory, "5", read_csvs, is_for_reads=True)

    # Writes
    cdf_csvs_to_plot(plot_target_directory, "5" + "-write", write_csvs, is_for_reads=False)


def plot_fig4(plot_target_directory, csv_target_directory, figure_name, gryff_latency_folder, pineapple_latency_folder,
              pqr_latency_folder):
    read_csvs, write_csvs, _, _ = calculate_csvs_cdf(figure_name, csv_target_directory, gryff_latency_folder,
                                                     pineapple_latency_folder, pqr_latency_folder)

    cdf_csvs_to_plot(plot_target_directory, figure_name, read_csvs, is_for_reads=True)
    cdf_csvs_to_plot(plot_target_directory, figure_name + "-write", write_csvs, is_for_reads=False)


# Plots log scale writes only
def plot_fig9(plot_target_directory, csv_target_directory, gryff_latency_folder, pineapple_latency_folder):
    _, _, _, write_log_csvs = calculate_csvs_cdf("9", csv_target_directory, gryff_latency_folder,
                                                 pineapple_latency_folder)

    # Writes 
    cdf_csvs_to_plot(plot_target_directory, "9-write-log", write_log_csvs, is_for_reads=False, log=True)


# def plot_fig6(plot_target_directory, results_path, csv_target_directory, latencies_folder_paths):
#     # For fig6, now results file structure is: TIMESTAMP/FIG6/PROTOCOL-WRITE_PERCENTAGE/CLIENT/....
#     # latencies_folder_paths = TIMESTAMP/FIG6/PROTOCOL/
#
#     # throughputs is a dictionary of throughputs (lookup via throughputs[protocol][wp])
#     throughputs = calculate_tput_wp("6", results_path, csv_target_directory, latencies_folder_paths)
#     tput_wp_plot(plot_target_directory, "6", throughputs)


def plot_RMWFig6(plot_target_directory, results_path, csv_target_directory, latencies_folder_paths):
    # For fig6, now results file structure is: TIMESTAMP/FIG6/PROTOCOL-WRITE_PERCENTAGE/CLIENT/....
    # latencies_folder_paths = TIMESTAMP/FIG6/PROTOCOL/

    # throughputs is a dictionary of throughputs (lookup via throughputs[protocol][wp])
    throughputs = calculate_tput_wp("rmw6", results_path, csv_target_directory, latencies_folder_paths)
    tput_wp_plot(plot_target_directory, "rmw6", throughputs, rmw=True)

def plot_fig6(plot_target_directory, csv_target_directory, figure_name, gryff_latency_folder,
                   pineapple_latency_folder, pqr_latency_folder, epaxos_latency_folder, mp_latency_folder, mpl_latency_folder):
    read_csvs, write_csvs, _, _, rmw_csvs, _ = calculate_csvs_cdf(figure_name, csv_target_directory,
                                                                  gryff_latency_folder,
                                                                  pineapple_latency_folder, pqr_latency_folder,
                                                                  epaxos_latency_folder, mp_latency_folder, mpl_latency_folder, rmw=True)

    cdf_csvs_to_plot(plot_target_directory, figure_name, read_csvs, is_for_reads=True)
    cdf_csvs_to_plot(plot_target_directory, figure_name + "-write", write_csvs, is_for_reads=False)
    cdf_csvs_to_plot(plot_target_directory, figure_name + "-rmw", rmw_csvs, is_for_reads=False, rmw=True)

# def plot_gryffFig6(plot_target_directory, csv_target_directory, figure_name, gryff_latency_folder,
#                    pineapple_latency_folder, pqr_latency_folder, epaxos_latency_folder=""):
#     read_csvs, write_csvs, _, _, rmw_csvs, _ = calculate_csvs_cdf(figure_name, csv_target_directory,
#                                                                   gryff_latency_folder,
#                                                                   pineapple_latency_folder, pqr_latency_folder,
#                                                                   epaxos_latency_folder, rmw=True)
#
#     cdf_csvs_to_plot(plot_target_directory, figure_name, read_csvs, is_for_reads=True)
#     cdf_csvs_to_plot(plot_target_directory, figure_name + "-write", write_csvs, is_for_reads=False)
#     cdf_csvs_to_plot(plot_target_directory, figure_name + "-rmw", rmw_csvs, is_for_reads=False, rmw=True)


def plot_gryffFig8(plot_target_directory, csv_target_directory, gryff_latency_folder, pineapple_latency_folder,
                   pqr_latency_folder, epaxos_latency_folder=""):
    read_csvs, write_csvs, _, _, rmw_csvs, _ = calculate_csvs_cdf("gryff8", csv_target_directory, gryff_latency_folder,
                                                                  pineapple_latency_folder, pqr_latency_folder,
                                                                  epaxos_latency_folder, rmw=True)

    # Reads
    cdf_csvs_to_plot(plot_target_directory, "gryff8", read_csvs, is_for_reads=True)

    # Writes
    cdf_csvs_to_plot(plot_target_directory, "gryff8" + "-write", write_csvs, is_for_reads=False)

    # RMWs
    cdf_csvs_to_plot(plot_target_directory, "gryff8" + "-rmw", rmw_csvs, is_for_reads=False, rmw=True)

def plot_fig8(plot_target_directory, csv_target_directory, figure_name, gryff_latency_folder, pineapple_latency_folder,
                   pqr_latency_folder, epaxos_latency_folder=""):
    read_csvs, write_csvs, _, _, rmw_csvs, _ = calculate_csvs_cdf(figure_name, csv_target_directory, gryff_latency_folder,
                                                                  pineapple_latency_folder, pqr_latency_folder,
                                                                  epaxos_latency_folder, rmw=True)

    # Reads
    cdf_csvs_to_plot(plot_target_directory, figure_name, read_csvs, is_for_reads=True)

    # Writes
    cdf_csvs_to_plot(plot_target_directory, figure_name + "-write", write_csvs, is_for_reads=False)

    # RMWs
    cdf_csvs_to_plot(plot_target_directory, figure_name + "-rmw", rmw_csvs, is_for_reads=False, rmw=True)


# def plot_gryffFig9(plot_target_directory, csv_target_directory, gryff_latency_folder, pineapple_latency_folder,
#                    pqr_latency_folder, epaxos_latency_folder=""):
#     read_csvs, write_csvs, _, _, rmw_csvs, _ = calculate_csvs_cdf("gryff9", csv_target_directory, gryff_latency_folder,
#                                                                   pineapple_latency_folder, pqr_latency_folder,
#                                                                   epaxos_latency_folder, rmw=True)
#
#     # Reads
#     cdf_csvs_to_plot(plot_target_directory, "gryff9", read_csvs, is_for_reads=True)
#
#     # Writes
#     cdf_csvs_to_plot(plot_target_directory, "gryff9" + "-write", write_csvs, is_for_reads=False)
#
#     # RMWs
#     cdf_csvs_to_plot(plot_target_directory, "gryff9" + "-rmw", rmw_csvs, is_for_reads=False, rmw=True)


def plot_gryffFig11(plot_target_directory, results_path, csv_target_directory, latencies_folder_paths):
    max_lats = calculate_lat_tas("gryff11", results_path, csv_target_directory, latencies_folder_paths)
    max_tas_plot(plot_target_directory, "gryff11", max_lats)


# Returns a tuple of tuple of csv paths.
# This is used for figs 4 , 5 and 9
def calculate_csvs_cdf(figure_name, csv_target_directory, gryff_latency_folder, pineapple_latency_folder, \
                       pqr_latency_folder, epaxos_latency_folder, mp_latency_folder, mpl_latency_folder, rmw=False):
    print("quick print")
    if epaxos_latency_folder != "":
        protocols = ["gryff", "pineapple", "pqr", "epaxos", "mp", "mpl"]
        folders = {"gryff": gryff_latency_folder, "pineapple": pineapple_latency_folder, "pqr": pqr_latency_folder, "epaxos": epaxos_latency_folder, "mp": mp_latency_folder, "mpl": mpl_latency_folder}
    else:
        protocols = ["gryff", "pineapple", "pqr"]
        folders = {"gryff": gryff_latency_folder, "pineapple": pineapple_latency_folder, "pqr": pqr_latency_folder}

    write_latencies = {}
    read_latencies = {}
    rmw_latencies = {}

    write_log_latencies = {}
    read_log_latencies = {}
    rmw_log_latencies = {}

    for protocol, folder in folders.items():
        # Create dictionary of write latencies (one key-value pair per protocol)
        w_latencies = extract_norm_latencies(folder, is_for_reads=False)
        write_latencies[protocol] = w_latencies

        # Create dictionary of read latencies
        r_latencies = extract_norm_latencies(folder, is_for_reads=True)
        read_latencies[protocol] = r_latencies

        # Create dictionary of RMW latencies
        if rmw:
            m_latencies = extract_norm_latencies(folder, is_for_reads=False, rmw=True)
            rmw_latencies[protocol] = m_latencies

    print("read latencies: ", len(read_latencies))

    # Protocol : csv
    read_csvs = {}
    write_csvs = {}
    rmw_csvs = {}

    read_log_csvs = {}
    write_log_csvs = {}
    rmw_log_csvs = {}

    # read
    for protocol, latency in read_latencies.items():
        norm_cdf_csv, norm_log_cdf_csv = latencies_to_csv(csv_target_directory, latency, protocol, figure_name)
        read_csvs[protocol] = norm_cdf_csv
        read_log_csvs[protocol] = norm_log_cdf_csv

    # write
    for protocol, latency in write_latencies.items():
        norm_cdf_csv, norm_log_cdf_csv = latencies_to_csv(csv_target_directory, latency, protocol,
                                                          figure_name + "-write")
        write_csvs[protocol] = norm_cdf_csv
        write_log_csvs[protocol] = norm_log_cdf_csv

    # rmw
    if rmw:
        for protocol, latency in rmw_latencies.items():
            norm_cdf_csv, norm_log_cdf_csv = latencies_to_csv(csv_target_directory, latency, protocol,
                                                              figure_name + "-rmw")
            rmw_csvs[protocol] = norm_cdf_csv
            rmw_log_csvs[protocol] = norm_log_cdf_csv

    if rmw:
        return read_csvs, write_csvs, read_log_csvs, write_log_csvs, rmw_csvs, rmw_log_csvs
    return read_csvs, write_csvs, read_log_csvs, write_log_csvs


# # calculates thoughput vs write percentage (fig6)
def calculate_tput_wp(figure_name, results_path, csv_target_directory, latencies_folder_paths):
    # ex: gryff_latency_dict contains subfolders with write percentage 
    # should give a dictionary of p100 throughputs (I think this is "maximum attainable througput" as referenced in the NSDI23_GUS paper) with PROTOCOL-WP as key (outer key of fig6)
    if figure_name == "rmw6":
        raw_throughputs = \
            json.loads(check_cmd_output("python3.8 ../client_metrics.py 50 --onlytputs --path=" + results_path))[
                "RMWFig6"]
    else:
        raw_throughputs = \
            json.loads(check_cmd_output("python3.8 ../client_metrics.py 50 --onlytputs --path=" + results_path))[
                "fig" + figure_name]

    # 2D dictionary indexed like: throughputs[PROTOCOL][WRITE_PERCENTAGE]
    throughputs = {}

    for protocol_wp, tput in raw_throughputs.items():
        temp = protocol_wp.split("-")
        protocol = temp[0]
        wp = temp[1]

        if protocol not in throughputs:
            throughputs[protocol] = np.empty([0, 2], dtype=float)
        throughputs[protocol] = np.append(throughputs[protocol], [[float(wp), float(tput)]],
                                          axis=0)  # throughputs[protocl] is a 2D numpy array with the strucutre [write-percentage, tput] on each row

    return throughputs

# # calculates latency vs tail at scale (fig11)
def calculate_lat_tas(figure_name, results_path, csv_target_directory, latencies_folder_paths):
    # ex: gryff_latency_dict contains subfolders with tail at scale values
    # should give a dictionary of p50 latencies
    raw_latencies = \
        json.loads(check_cmd_output("python3.8 ../client_metrics.py 50 --onlymax --path=" + results_path))["gryffFig11"]

    # 2D dictionary indexed like: throughputs[PROTOCOL][TAIL_AT_SCALE]
    latencies = {}

    for protocol_tas, lat in raw_latencies.items():
        temp = protocol_tas.split("-")
        protocol = temp[0]
        tas = temp[1]

        if protocol not in latencies:
            latencies[protocol] = np.empty([0, 2], dtype=float)
        latencies[protocol] = np.append(latencies[protocol], [[float(tas), float(lat)]],
                                          axis=0)

    return latencies


# Delete and fix packaging
def check_cmd_output(cmd):
    # output = subprocess.check_output(cmd)
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    return output.decode("utf-8").strip("\n")


# returns newest results. Assumes results are in ../results
def most_recent_results():
    results_dir = "../results/"
    return results_dir + check_cmd_output("ls " + results_dir + "| sort -r | head -n 1")


def usage():
    print("Usage: python3 plot_figs.py RESULTS_PATH")


if __name__ == "__main__":
    l = len(sys.argv)
    if l == 1:
        main(most_recent_results())
    elif l == 2:
        main(sys.argv[1])
    else:
        usage()
