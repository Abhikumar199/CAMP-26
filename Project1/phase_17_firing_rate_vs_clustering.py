"""
phase_17_firing_rate_vs_clustering_curve.py

FIXED:
    N = 1000

QUESTION:
    How does mean whole-network firing rate vary
    with the clustering coefficient?

For every shortcut density p:

    1. Generate multiple random networks.
    2. Calculate clustering coefficient using:

           C_i = 2 e_i / [k_i (k_i - 1)]

    3. Average over all neurons:

           C = (1/N) sum_i C_i

    4. Run neuron simulation.
    5. Calculate whole-network mean firing rate.
    6. Average across random realizations.

FINAL PLOT:

    x-axis = Mean clustering coefficient C
    y-axis = Mean whole-network firing rate

    One connected curve.
"""


from pathlib import Path
import csv

import numpy as np
import matplotlib.pyplot as plt

from network import (
    build_ring_network,
    add_random_shortcuts,
)

from simulator import run_simulation


# ============================================================
# PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent

RESULTS_DIR = (
    PROJECT_DIR
    / "results"
    / "phase17_firing_rate_vs_clustering"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


SUMMARY_FILE = (
    RESULTS_DIR
    / "summary_firing_rate_vs_clustering.csv"
)


FIGURE_FILE = (
    RESULTS_DIR
    / "firing_rate_vs_clustering_curve.png"
)


# ============================================================
# FIXED NETWORK SIZE
# ============================================================

N = 1000


# ============================================================
# SHORTCUT DENSITIES
# ============================================================

P_VALUES = [

    0.00,
    0.01,
    0.02,
    0.03,
    0.05,
    0.075,
    0.10,
    0.15,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
    0.80,
    0.90,
    1.00,

]


# ============================================================
# NUMBER OF RANDOM NETWORKS PER p
# ============================================================

# Start with 3 for testing.
# Later use 10 or 20.

NUM_REALIZATIONS = 3


# ============================================================
# NEURON PARAMETERS
# ============================================================

I_EXT = 0.85

G_SYN = 0.20

TAU_M = 10.0

TAU_D = 1.0


# ============================================================
# SIMULATION PARAMETERS
# ============================================================

DT = 0.01

T_MAX = 2000.0

STIMULUS_TIME = 10.0

STIMULUS_NEURON = N // 2


# ============================================================
# CLUSTERING COEFFICIENT
# ============================================================

def calculate_clustering_coefficient(
    outgoing_connections,
):

    number_of_nodes = len(
        outgoing_connections
    )


    # ========================================================
    # CREATE UNDIRECTED NEIGHBOR SETS
    # ========================================================

    neighbors = [

        set()

        for _ in range(
            number_of_nodes
        )

    ]


    for i in range(
        number_of_nodes
    ):

        for j in outgoing_connections[i]:

            if i == j:

                continue


            neighbors[i].add(j)

            neighbors[j].add(i)


    # ========================================================
    # CALCULATE C_i FOR EVERY NEURON
    # ========================================================

    local_coefficients = []


    for i in range(
        number_of_nodes
    ):


        node_neighbors = list(
            neighbors[i]
        )


        # --------------------------------------------
        # k_i = degree of neuron i
        # --------------------------------------------

        k_i = len(
            node_neighbors
        )


        if k_i < 2:

            C_i = 0.0


        else:


            # ----------------------------------------
            # e_i = number of connections among
            #       neighbors of neuron i
            # ----------------------------------------

            e_i = 0


            for a in range(
                k_i
            ):

                u = node_neighbors[a]


                for b in range(
                    a + 1,
                    k_i,
                ):

                    v = node_neighbors[b]


                    if v in neighbors[u]:

                        e_i += 1


            # ----------------------------------------
            # CLUSTERING FORMULA
            #
            #          2 e_i
            # C_i = ------------
            #        k_i(k_i-1)
            # ----------------------------------------

            C_i = (

                2.0
                * e_i

                /

                (
                    k_i
                    * (k_i - 1)
                )

            )


        # Numerical safety check

        if not (
            0.0
            <= C_i
            <= 1.0
        ):

            raise ValueError(

                f"Invalid C_i = {C_i} "
                f"for neuron {i}"

            )


        local_coefficients.append(
            C_i
        )


    # ========================================================
    # WHOLE-NETWORK CLUSTERING
    #
    #          1
    # C = --------- sum C_i
    #          N
    # ========================================================

    C = float(

        np.mean(
            local_coefficients
        )

    )


    # Final mathematical check

    if not (
        0.0
        <= C
        <= 1.0
    ):

        raise ValueError(

            f"Invalid network clustering "
            f"coefficient C = {C}"

        )


    return C


# ============================================================
# WHOLE-NETWORK MEAN FIRING RATE
# ============================================================

def calculate_mean_firing_rate(
    spike_times,
):


    spike_times = np.asarray(

        spike_times,

        dtype=float,

    )


    # Only analyse activity after stimulus

    analysis_spikes = spike_times[

        spike_times
        >= STIMULUS_TIME

    ]


    analysis_duration = (

        T_MAX
        - STIMULUS_TIME

    )


    # --------------------------------------------------------
    # WHOLE-NETWORK NORMALIZED FIRING RATE
    #
    #              total spikes
    # r = --------------------------------
    #       N × post-stimulus duration
    # --------------------------------------------------------

    firing_rate = (

        len(
            analysis_spikes
        )

        /

        (
            N
            * analysis_duration
        )

    )


    return float(
        firing_rate
    )


# ============================================================
# MAIN
# ============================================================

def main():


    print("=" * 90)

    print(
        "PHASE 17: FIRING RATE VS CLUSTERING COEFFICIENT"
    )

    print("=" * 90)


    print(
        "\nFixed N =",
        N,
    )


    print(
        "Realizations per p =",
        NUM_REALIZATIONS,
    )


    summary_results = []


    # ========================================================
    # LOOP OVER SHORTCUT DENSITY p
    # ========================================================

    for p in P_VALUES:


        print("\n")

        print("=" * 90)

        print(
            f"p = {p}"
        )

        print("=" * 90)


        clustering_values = []

        firing_rate_values = []


        # ====================================================
        # RANDOM NETWORK REALIZATIONS
        # ====================================================

        for realization in range(
            NUM_REALIZATIONS
        ):


            seed = (

                int(
                    round(
                        p * 10000
                    )
                )

                * 100

                + realization

            )


            # ================================================
            # BUILD NETWORK
            # ================================================

            local_network = (

                build_ring_network(
                    N
                )

            )


            network, shortcuts = (

                add_random_shortcuts(

                    outgoing_connections=
                        local_network,

                    p=p,

                    seed=seed,

                )

            )


            # ================================================
            # CALCULATE CLUSTERING COEFFICIENT
            # ================================================

            C = (

                calculate_clustering_coefficient(
                    network
                )

            )


            clustering_values.append(
                C
            )


            # ================================================
            # RUN SIMULATION
            # ================================================

            spike_times, spike_neurons = (

                run_simulation(

                    outgoing_connections=
                        network,

                    I_ext=
                        I_EXT,

                    g_syn=
                        G_SYN,

                    tau_m=
                        TAU_M,

                    tau_D=
                        TAU_D,

                    dt=
                        DT,

                    t_max=
                        T_MAX,

                    stimulus_neuron=
                        STIMULUS_NEURON,

                    stimulus_time=
                        STIMULUS_TIME,

                )

            )


            # ================================================
            # CALCULATE FIRING RATE
            # ================================================

            firing_rate = (

                calculate_mean_firing_rate(
                    spike_times
                )

            )


            firing_rate_values.append(
                firing_rate
            )


            print(

                f"realization = {realization:2d}"

                f"   C = {C:.6f}"

                f"   firing rate = {firing_rate:.6f}"

                f"   shortcuts = {len(shortcuts)}"

            )


        # ====================================================
        # CALCULATE MEAN AND SD FOR THIS p
        # ====================================================

        clustering_values = np.asarray(

            clustering_values,

            dtype=float,

        )


        firing_rate_values = np.asarray(

            firing_rate_values,

            dtype=float,

        )


        mean_C = float(

            np.mean(
                clustering_values
            )

        )


        std_C = float(

            np.std(
                clustering_values,
                ddof=1,
            )

        ) if NUM_REALIZATIONS > 1 else 0.0


        mean_firing_rate = float(

            np.mean(
                firing_rate_values
            )

        )


        std_firing_rate = float(

            np.std(
                firing_rate_values,
                ddof=1,
            )

        ) if NUM_REALIZATIONS > 1 else 0.0


        summary_results.append({

            "p":
                p,

            "mean_clustering":
                mean_C,

            "std_clustering":
                std_C,

            "mean_firing_rate":
                mean_firing_rate,

            "std_firing_rate":
                std_firing_rate,

        })


        print("\nSUMMARY FOR THIS p")

        print("-" * 90)


        print(

            f"p = {p:.3f}"

            f"   Mean C = {mean_C:.6f}"

            f"   SD C = {std_C:.6f}"

            f"   Mean firing rate = "
            f"{mean_firing_rate:.6f}"

        )


    # ========================================================
    # SAVE SUMMARY CSV
    # ========================================================

    with open(

        SUMMARY_FILE,

        "w",

        newline="",

    ) as file:


        fieldnames = [

            "p",

            "mean_clustering",

            "std_clustering",

            "mean_firing_rate",

            "std_firing_rate",

        ]


        writer = csv.DictWriter(

            file,

            fieldnames=fieldnames,

        )


        writer.writeheader()


        writer.writerows(
            summary_results
        )


    # ========================================================
    # PRINT FINAL CLUSTERING TABLE
    # ========================================================

    print("\n")

    print("=" * 90)

    print(
        "CALCULATED CLUSTERING COEFFICIENT VALUES"
    )

    print("=" * 90)


    print(

        f"{'p':>8}"

        f"{'Mean C':>15}"

        f"{'SD C':>15}"

        f"{'Mean firing rate':>22}"

    )


    print("-" * 90)


    for row in summary_results:


        print(

            f"{row['p']:8.3f}"

            f"{row['mean_clustering']:15.6f}"

            f"{row['std_clustering']:15.6f}"

            f"{row['mean_firing_rate']:22.6f}"

        )


    # ========================================================
    # PREPARE CURVE DATA
    # ========================================================

    C_plot = np.asarray([

        row["mean_clustering"]

        for row in summary_results

    ])


    firing_plot = np.asarray([

        row["mean_firing_rate"]

        for row in summary_results

    ])


    firing_std = np.asarray([

        row["std_firing_rate"]

        for row in summary_results

    ])


    # ========================================================
    # SORT BY CLUSTERING COEFFICIENT
    # ========================================================

    # This is important because the x-axis is C,
    # not p.

    sort_order = np.argsort(
        C_plot
    )


    C_plot = C_plot[
        sort_order
    ]


    firing_plot = firing_plot[
        sort_order
    ]


    firing_std = firing_std[
        sort_order
    ]


    # ========================================================
    # CREATE CURVE
    # ========================================================

    plt.figure(
        figsize=(10, 7)
    )


    plt.plot(

        C_plot,

        firing_plot,

        marker="o",

        markersize=7,

        linewidth=2,

        label=(
            f"N = {N}"
        ),

    )


    # ========================================================
    # SHOW VARIABILITY
    # ========================================================

    plt.fill_between(

        C_plot,

        np.maximum(
            firing_plot
            - firing_std,
            0,
        ),

        firing_plot
        + firing_std,

        alpha=0.2,

        label="Mean ± SD",

    )


    # ========================================================
    # LABEL EVERY POINT WITH ITS p VALUE
    # ========================================================

    sorted_rows = [

        summary_results[i]

        for i in sort_order

    ]


    for x, y, row in zip(

        C_plot,

        firing_plot,

        sorted_rows,

    ):


        plt.annotate(

            f"p={row['p']:.2f}",

            xy=(
                x,
                y,
            ),

            xytext=(
                5,
                7,
            ),

            textcoords=
                "offset points",

            fontsize=8,

        )


    # ========================================================
    # AXES
    # ========================================================

    plt.xlabel(

        "Mean clustering coefficient, C",

        fontsize=13,

    )


    plt.ylabel(

        "Mean whole-network firing rate",

        fontsize=13,

    )


    plt.title(

        "Whole-Network Firing Rate vs Clustering Coefficient\n"

        f"N = {N}",

        fontsize=14,

    )


    # Clustering coefficient is mathematically
    # bounded between 0 and 1.

    plt.xlim(
        0,
        1,
    )


    plt.ylim(
        bottom=0,
    )


    plt.grid(
        alpha=0.3
    )


    plt.legend(
        fontsize=10
    )


    plt.tight_layout()


    # ========================================================
    # SAVE
    # ========================================================

    plt.savefig(

        FIGURE_FILE,

        dpi=300,

        bbox_inches="tight",

    )


    plt.show()


    print("\n")

    print("=" * 90)

    print(
        "PHASE 17 COMPLETE"
    )

    print("=" * 90)


    print(
        "\nSummary CSV:"
    )

    print(
        SUMMARY_FILE
    )


    print(
        "\nFigure:"
    )

    print(
        FIGURE_FILE
    )


# ============================================================
# WINDOWS ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()