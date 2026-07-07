"""
PHASE 18
--------

QUESTION:

    For a fixed network size N = 1000,
    how does the mean whole-network firing rate
    change with shortcut density p?

FIXED:

    N = 1000

VARIED:

    p = 0 to 1

FOR EACH p:

    1. Generate multiple random network realizations.
    2. Run the neural simulation.
    3. Calculate whole-network mean firing rate.
    4. Average firing rate across realizations.

FIRING RATE:

                         total post-stimulus spikes
    mean firing rate = --------------------------------
                        N × post-stimulus duration

FINAL PLOT:

    x-axis = Shortcut density p
    y-axis = Mean whole-network firing rate

    Connected curve with error bars.
"""


# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
import csv
import time
import os

from concurrent.futures import (
    ProcessPoolExecutor,
    as_completed,
)

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
    / "phase18_firing_rate_vs_p"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


ALL_FILE = (
    RESULTS_DIR
    / "all_realizations.csv"
)


SUMMARY_FILE = (
    RESULTS_DIR
    / "firing_rate_vs_p_summary.csv"
)


FIGURE_FILE = (
    RESULTS_DIR
    / "firing_rate_vs_density_p.png"
)


# ============================================================
# FIXED NETWORK SIZE
# ============================================================

N = 1000


# ============================================================
# SHORTCUT DENSITY p
# ============================================================

# 21 equally spaced values:
#
# 0.00, 0.05, 0.10, ..., 1.00

P_VALUES = np.linspace(
    0.0,
    1.0,
    21,
)


# ============================================================
# NUMBER OF RANDOM NETWORK REALIZATIONS
# ============================================================

# First test:
#     3
#
# Final exploratory result:
#     10
#
# Stronger result:
#     20 or more

NUM_REALIZATIONS = 10


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
# CPU SETTINGS
# ============================================================

CPU_COUNT = os.cpu_count() or 4

MAX_WORKERS = max(
    1,
    CPU_COUNT - 1,
)


# ============================================================
# CALCULATE WHOLE-NETWORK MEAN FIRING RATE
# ============================================================

def calculate_mean_firing_rate(
    spike_times,
):

    spike_times = np.asarray(
        spike_times,
        dtype=float,
    )


    # --------------------------------------------------------
    # ONLY ANALYZE SPIKES AFTER THE STIMULUS
    # --------------------------------------------------------

    analysis_spikes = spike_times[
        spike_times >= STIMULUS_TIME
    ]


    # --------------------------------------------------------
    # POST-STIMULUS OBSERVATION DURATION
    # --------------------------------------------------------

    analysis_duration = (
        T_MAX
        - STIMULUS_TIME
    )


    # --------------------------------------------------------
    # MEAN WHOLE-NETWORK FIRING RATE
    #
    #                 total spikes
    # r = -----------------------------------
    #       N × post-stimulus duration
    # --------------------------------------------------------

    firing_rate = (

        len(analysis_spikes)

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
# RUN ONE REALIZATION
# ============================================================

def run_one_realization(
    task,
):

    p, realization = task


    # --------------------------------------------------------
    # UNIQUE DETERMINISTIC SEED
    # --------------------------------------------------------

    seed = (

        int(
            round(
                p * 10000
            )
        )

        * 1000

        + realization

    )


    # --------------------------------------------------------
    # BUILD LOCAL RING
    # --------------------------------------------------------

    local_network = build_ring_network(
        N
    )


    # --------------------------------------------------------
    # ADD RANDOM SHORTCUTS
    # --------------------------------------------------------

    network, shortcuts = add_random_shortcuts(

        outgoing_connections=
            local_network,

        p=p,

        seed=seed,

    )


    # --------------------------------------------------------
    # RUN SIMULATION
    # --------------------------------------------------------

    start_time = time.perf_counter()


    spike_times, spike_neurons = run_simulation(

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


    runtime = (
        time.perf_counter()
        - start_time
    )


    # --------------------------------------------------------
    # CALCULATE FIRING RATE
    # --------------------------------------------------------

    firing_rate = calculate_mean_firing_rate(
        spike_times
    )


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "N":
            N,

        "p":
            float(p),

        "realization":
            realization,

        "seed":
            seed,

        "number_of_shortcuts":
            len(shortcuts),

        "total_spikes":
            len(spike_times),

        "mean_firing_rate":
            firing_rate,

        "runtime_seconds":
            runtime,

    }


# ============================================================
# MAIN
# ============================================================

def main():


    print("=" * 90)

    print(
        "PHASE 18: FIRING RATE VS SHORTCUT DENSITY p"
    )

    print("=" * 90)


    print(
        "\nFixed N =",
        N,
    )


    print(
        "p range =",
        f"{P_VALUES[0]:.2f}",
        "to",
        f"{P_VALUES[-1]:.2f}",
    )


    print(
        "Number of p values =",
        len(P_VALUES),
    )


    print(
        "Realizations per p =",
        NUM_REALIZATIONS,
    )


    print(
        "Logical CPU cores =",
        CPU_COUNT,
    )


    print(
        "Workers used =",
        MAX_WORKERS,
    )


    # ========================================================
    # CREATE TASKS
    # ========================================================

    tasks = []


    for p in P_VALUES:

        for realization in range(
            NUM_REALIZATIONS
        ):

            tasks.append(
                (
                    float(p),
                    realization,
                )
            )


    print(
        "\nTotal simulations =",
        len(tasks),
    )


    # ========================================================
    # RUN SIMULATIONS IN PARALLEL
    # ========================================================

    all_results = []

    completed = 0

    total_start = time.perf_counter()


    print("\nRUNNING SIMULATIONS")

    print("-" * 90)


    with ProcessPoolExecutor(

        max_workers=
            MAX_WORKERS

    ) as executor:


        future_to_task = {


            executor.submit(

                run_one_realization,

                task,

            ):

            task


            for task in tasks

        }


        for future in as_completed(
            future_to_task
        ):


            p, realization = (
                future_to_task[future]
            )


            try:


                result = future.result()


                all_results.append(
                    result
                )


                completed += 1


                print(

                    f"[{completed:4d}/"
                    f"{len(tasks):4d}]"

                    f"  p={p:.2f}"

                    f"  realization="
                    f"{realization:2d}"

                    f"  shortcuts="
                    f"{result['number_of_shortcuts']:4d}"

                    f"  FR="
                    f"{result['mean_firing_rate']:.8f}"

                    f"  runtime="
                    f"{result['runtime_seconds']:.2f}s"

                )


            except Exception as error:


                print(
                    "\nERROR:"
                )

                print(
                    "p =",
                    p,
                )

                print(
                    "realization =",
                    realization,
                )

                print(
                    error
                )


    # ========================================================
    # SORT RESULTS
    # ========================================================

    all_results.sort(

        key=lambda row:

            (
                row["p"],
                row["realization"],
            )

    )


    # ========================================================
    # SAVE ALL REALIZATIONS
    # ========================================================

    with open(

        ALL_FILE,

        "w",

        newline="",

    ) as file:


        fieldnames = [

            "N",

            "p",

            "realization",

            "seed",

            "number_of_shortcuts",

            "total_spikes",

            "mean_firing_rate",

            "runtime_seconds",

        ]


        writer = csv.DictWriter(

            file,

            fieldnames=
                fieldnames,

        )


        writer.writeheader()


        writer.writerows(
            all_results
        )


    # ========================================================
    # CALCULATE SUMMARY FOR EACH p
    # ========================================================

    summary_results = []


    print("\n")

    print("=" * 90)

    print(
        "SUMMARY"
    )

    print("=" * 90)


    for p in P_VALUES:


        p = float(p)


        p_rows = [

            row

            for row in all_results

            if np.isclose(
                row["p"],
                p,
            )

        ]


        firing_rates = np.asarray(

            [

                row["mean_firing_rate"]

                for row in p_rows

            ],

            dtype=float,

        )


        shortcut_counts = np.asarray(

            [

                row["number_of_shortcuts"]

                for row in p_rows

            ],

            dtype=float,

        )


        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        mean_firing_rate = float(
            np.mean(firing_rates)
        )


        std_firing_rate = float(

            np.std(
                firing_rates,
                ddof=1,
            )

        ) if len(firing_rates) > 1 else 0.0


        mean_shortcuts = float(
            np.mean(shortcut_counts)
        )


        # ----------------------------------------------------
        # SAVE SUMMARY
        # ----------------------------------------------------

        summary_results.append({

            "N":
                N,

            "p":
                p,

            "mean_number_of_shortcuts":
                mean_shortcuts,

            "number_of_realizations":
                len(p_rows),

            "mean_firing_rate":
                mean_firing_rate,

            "std_firing_rate":
                std_firing_rate,

        })


        # ----------------------------------------------------
        # PRINT VALUES
        # ----------------------------------------------------

        print(

            f"p = {p:4.2f}"

            f" | shortcuts = "
            f"{mean_shortcuts:7.2f}"

            f" | mean FR = "
            f"{mean_firing_rate:.8f}"

            f" | SD = "
            f"{std_firing_rate:.8f}"

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

            "N",

            "p",

            "mean_number_of_shortcuts",

            "number_of_realizations",

            "mean_firing_rate",

            "std_firing_rate",

        ]


        writer = csv.DictWriter(

            file,

            fieldnames=
                fieldnames,

        )


        writer.writeheader()


        writer.writerows(
            summary_results
        )


    # ========================================================
    # PREPARE PLOT DATA
    # ========================================================

    p_plot = np.asarray(

        [

            row["p"]

            for row in summary_results

        ],

        dtype=float,

    )


    mean_fr_plot = np.asarray(

        [

            row["mean_firing_rate"]

            for row in summary_results

        ],

        dtype=float,

    )


    std_fr_plot = np.asarray(

        [

            row["std_firing_rate"]

            for row in summary_results

        ],

        dtype=float,

    )


    # ========================================================
    # CREATE CONNECTED CURVE
    # ========================================================

    plt.figure(
        figsize=(9, 6)
    )


    plt.plot(

        p_plot,

        mean_fr_plot,

        marker="o",

        linewidth=2.0,

        markersize=6,

        label="N = 1000",

    )


    # --------------------------------------------------------
    # ERROR REGION
    # --------------------------------------------------------

    plt.fill_between(

        p_plot,

        mean_fr_plot - std_fr_plot,

        mean_fr_plot + std_fr_plot,

        alpha=0.20,

    )


    plt.xlabel(
        "Shortcut density, p"
    )


    plt.ylabel(
        "Mean whole-network firing rate"
    )


    plt.title(
        "Firing Rate vs Shortcut Density (N = 1000)"
    )


    plt.xlim(
        0.0,
        1.0,
    )


    plt.legend()


    plt.grid(
        alpha=0.25
    )


    plt.tight_layout()


    plt.savefig(

        FIGURE_FILE,

        dpi=300,

        bbox_inches="tight",

    )


    plt.show()


    # ========================================================
    # FINAL INFORMATION
    # ========================================================

    total_runtime = (

        time.perf_counter()

        - total_start

    )


    print("\n")

    print("=" * 90)

    print(
        "EXPERIMENT COMPLETE"
    )

    print("=" * 90)


    print(
        "Total runtime =",
        f"{total_runtime:.2f} seconds",
    )


    print(
        "All realizations saved to:"
    )

    print(
        ALL_FILE
    )


    print(
        "\nSummary saved to:"
    )

    print(
        SUMMARY_FILE
    )


    print(
        "\nFigure saved to:"
    )

    print(
        FIGURE_FILE
    )


# ============================================================
# WINDOWS MULTIPROCESSING PROTECTION
# ============================================================

if __name__ == "__main__":

    main()