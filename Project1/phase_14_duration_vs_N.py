"""
phase_14_duration_vs_N.py

PHASE 14
--------

QUESTION:

    At fixed shortcut density p = 0.1,
    how does the duration of activity depend on
    the number of neurons N?

PLOT:

    Activity duration
           vs
    Number of neurons N


IMPORTANT:

    For every N:

        1. Generate many random network realizations.
        2. Keep p fixed.
        3. Run the simulation.
        4. Measure:

               duration =
                   last_spike_time
                   - stimulus_time

        5. Calculate:

               mean duration
               standard deviation
               median duration
               fraction reaching T_MAX

        6. Plot mean duration ± standard deviation.


This experiment tests whether activity lifetime:

    - increases with N,
    - decreases with N,
    - peaks at intermediate N,
    - or shows another pattern.

The curve is NOT forced to have any particular shape.
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
    / "phase14_duration_vs_N"
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
    / "duration_vs_N_summary.csv"
)


FIGURE_FILE = (
    RESULTS_DIR
    / "duration_vs_number_of_neurons.png"
)


# ============================================================
# EXPERIMENT PARAMETERS
# ============================================================

# Number of neurons
N_VALUES = [

    100,

    200,

    250,

    500,

    1000,

    2000,

]


# ------------------------------------------------------------
# FIXED SHORTCUT DENSITY
# ------------------------------------------------------------

P = 0.10


# ------------------------------------------------------------
# NUMBER OF RANDOM NETWORK REALIZATIONS
# ------------------------------------------------------------

# Start with 20 for testing.
#
# After confirming everything works:
#
#     50  = good exploratory result
#     100 = stronger result

NUM_REALIZATIONS = 50


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


# IMPORTANT:
#
# Large N may produce very long activity.
#
# We use the same long horizon as Phase 11–13.

T_MAX = 3000.0


STIMULUS_TIME = 10.0


# ============================================================
# END-OF-SIMULATION WINDOW
# ============================================================

# If spikes occur in the final 200 time units,
# the activity is considered to have reached T_MAX.

FINAL_WINDOW = 200.0


FINAL_WINDOW_START = (

    T_MAX
    - FINAL_WINDOW

)


# ============================================================
# CPU SETTINGS
# ============================================================

CPU_COUNT = os.cpu_count() or 4


# Leave one logical CPU core free
# so Windows remains responsive.

MAX_WORKERS = max(

    1,

    CPU_COUNT - 1,

)


# ============================================================
# ANALYZE ONE REALIZATION
# ============================================================

def analyze_activity(
    spike_times,
):


    spike_times = np.asarray(

        spike_times,

        dtype=float,

    )


    # --------------------------------------------------------
    # NO SPIKES
    # --------------------------------------------------------

    if len(spike_times) == 0:


        return {

            "total_spikes":

                0,


            "last_spike_time":

                np.nan,


            "activity_duration":

                0.0,


            "reached_tmax":

                False,


            "censored":

                False,

        }


    # --------------------------------------------------------
    # LAST SPIKE
    # --------------------------------------------------------

    last_spike_time = float(

        np.max(

            spike_times

        )

    )


    # --------------------------------------------------------
    # ACTIVITY DURATION
    # --------------------------------------------------------

    activity_duration = max(

        0.0,

        last_spike_time

        - STIMULUS_TIME,

    )


    # --------------------------------------------------------
    # DID ACTIVITY REACH THE END?
    # --------------------------------------------------------

    spikes_in_final_window = int(

        np.sum(

            spike_times

            >= FINAL_WINDOW_START

        )

    )


    reached_tmax = (

        spikes_in_final_window

        > 0

    )


    # --------------------------------------------------------
    # CENSORING
    # --------------------------------------------------------

    # If activity is still present near T_MAX,
    # we do not know the true lifetime.
    #
    # Therefore:
    #
    #     true duration >= measured duration

    censored = reached_tmax


    return {

        "total_spikes":

            len(spike_times),


        "last_spike_time":

            last_spike_time,


        "activity_duration":

            activity_duration,


        "reached_tmax":

            reached_tmax,


        "censored":

            censored,

    }


# ============================================================
# WORKER FUNCTION
# ============================================================

def run_one_realization(
    task,
):


    N, seed = task


    # --------------------------------------------------------
    # BUILD LOCAL RING
    # --------------------------------------------------------

    local_network = (

        build_ring_network(

            N

        )

    )


    # --------------------------------------------------------
    # ADD RANDOM SHORTCUTS
    # --------------------------------------------------------

    network, shortcuts = (

        add_random_shortcuts(

            outgoing_connections=

                local_network,

            p=P,

            seed=seed,

        )

    )


    # --------------------------------------------------------
    # STIMULUS NEURON
    # --------------------------------------------------------

    stimulus_neuron = (

        N // 2

    )


    # --------------------------------------------------------
    # RUN SIMULATION
    # --------------------------------------------------------

    start_time = (

        time.perf_counter()

    )


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

                stimulus_neuron,

            stimulus_time=

                STIMULUS_TIME,

        )

    )


    runtime = (

        time.perf_counter()

        - start_time

    )


    # --------------------------------------------------------
    # ANALYZE ACTIVITY
    # --------------------------------------------------------

    result = (

        analyze_activity(

            spike_times

        )

    )


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "N":

            N,


        "p":

            P,


        "seed":

            seed,


        "number_of_shortcuts":

            len(shortcuts),


        "total_spikes":

            result[

                "total_spikes"

            ],


        "last_spike_time":

            result[

                "last_spike_time"

            ],


        "activity_duration":

            result[

                "activity_duration"

            ],


        "reached_tmax":

            result[

                "reached_tmax"

            ],


        "censored":

            result[

                "censored"

            ],


        "runtime_seconds":

            runtime,

    }


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def main():


    print("=" * 80)


    print(

        "PHASE 14: ACTIVITY DURATION VS NUMBER OF NEURONS"

    )


    print("=" * 80)


    print("\nQUESTION")

    print("-" * 50)


    print(

        "How does activity duration change with N"

    )


    print(

        "when shortcut density p is fixed?"

    )


    print("\nFIXED PARAMETERS")

    print("-" * 50)


    print(

        "p =",

        P,

    )


    print(

        "N values =",

        N_VALUES,

    )


    print(

        "Realizations per N =",

        NUM_REALIZATIONS,

    )


    print(

        "T_MAX =",

        T_MAX,

    )


    print("\nCPU")

    print("-" * 50)


    print(

        "Logical CPU cores =",

        CPU_COUNT,

    )


    print(

        "Worker processes =",

        MAX_WORKERS,

    )


    # ========================================================
    # CREATE TASKS
    # ========================================================

    tasks = []


    for N in N_VALUES:


        for realization in range(

            NUM_REALIZATIONS

        ):


            # Unique deterministic seed
            #
            # Example:
            #
            # N=100, realization=0
            #     seed = 100000
            #
            # N=500, realization=3
            #     seed = 500003

            seed = (

                N * 1000

                + realization

            )


            tasks.append(

                (

                    N,

                    seed,

                )

            )


    print("\nTOTAL SIMULATIONS")

    print("-" * 50)


    print(

        len(tasks)

    )


    # ========================================================
    # RUN PARALLEL SIMULATIONS
    # ========================================================

    all_results = []


    experiment_start = (

        time.perf_counter()

    )


    print("\nRUNNING SIMULATIONS")

    print("-" * 50)


    completed = 0


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


            task = (

                future_to_task[

                    future

                ]

            )


            N, seed = task


            try:


                result = (

                    future.result()

                )


                all_results.append(

                    result

                )


                completed += 1


                print(

                    f"[{completed:4d}/"

                    f"{len(tasks):4d}]"

                    f"  N={N:4d}"

                    f"  seed={seed}"

                    f"  duration="

                    f"{result['activity_duration']:.2f}"

                    f"  reached_TMAX="

                    f"{result['reached_tmax']}"

                    f"  runtime="

                    f"{result['runtime_seconds']:.2f}s"

                )


            except Exception as error:


                print(

                    "\nERROR"

                )


                print(

                    "N =",

                    N,

                )


                print(

                    "seed =",

                    seed,

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

                row["N"],

                row["seed"],

            )

    )


    # ========================================================
    # SAVE ALL REALIZATIONS
    # ========================================================

    fieldnames = [

        "N",

        "p",

        "seed",

        "number_of_shortcuts",

        "total_spikes",

        "last_spike_time",

        "activity_duration",

        "reached_tmax",

        "censored",

        "runtime_seconds",

    ]


    with open(

        ALL_FILE,

        "w",

        newline="",

    ) as file:


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
    # CALCULATE SUMMARY FOR EACH N
    # ========================================================

    summary_results = []


    print("\n")

    print("=" * 80)

    print(

        "SUMMARY"

    )

    print("=" * 80)


    for N in N_VALUES:


        rows = [

            row

            for row in all_results

            if row["N"] == N

        ]


        durations = np.array(

            [

                row[

                    "activity_duration"

                ]

                for row in rows

            ],

            dtype=float,

        )


        reached_tmax = np.array(

            [

                row[

                    "reached_tmax"

                ]

                for row in rows

            ],

            dtype=bool,

        )


        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        mean_duration = float(

            np.mean(

                durations

            )

        )


        std_duration = float(

            np.std(

                durations,

                ddof=1,

            )

        )


        median_duration = float(

            np.median(

                durations

            )

        )


        min_duration = float(

            np.min(

                durations

            )

        )


        max_duration = float(

            np.max(

                durations

            )

        )


        fraction_reached_tmax = float(

            np.mean(

                reached_tmax

            )

        )


        num_reached_tmax = int(

            np.sum(

                reached_tmax

            )

        )


        summary = {

            "N":

                N,


            "p":

                P,


            "num_realizations":

                len(rows),


            "mean_duration":

                mean_duration,


            "std_duration":

                std_duration,


            "median_duration":

                median_duration,


            "min_duration":

                min_duration,


            "max_duration":

                max_duration,


            "num_reached_tmax":

                num_reached_tmax,


            "fraction_reached_tmax":

                fraction_reached_tmax,

        }


        summary_results.append(

            summary

        )


        print(

            f"\nN = {N}"

        )


        print(

            f"Mean duration   = "

            f"{mean_duration:.2f}"

        )


        print(

            f"Std duration    = "

            f"{std_duration:.2f}"

        )


        print(

            f"Median duration = "

            f"{median_duration:.2f}"

        )


        print(

            f"Reached T_MAX   = "

            f"{num_reached_tmax}"

            f"/{len(rows)}"

            f"  "

            f"({100 * fraction_reached_tmax:.1f}%)"

        )


    # ========================================================
    # SAVE SUMMARY CSV
    # ========================================================

    summary_fieldnames = [

        "N",

        "p",

        "num_realizations",

        "mean_duration",

        "std_duration",

        "median_duration",

        "min_duration",

        "max_duration",

        "num_reached_tmax",

        "fraction_reached_tmax",

    ]


    with open(

        SUMMARY_FILE,

        "w",

        newline="",

    ) as file:


        writer = csv.DictWriter(

            file,

            fieldnames=

                summary_fieldnames,

        )


        writer.writeheader()


        writer.writerows(

            summary_results

        )

       # ========================================================
    # PREPARE DATA FOR BOXPLOT
    # ========================================================

    boxplot_data = []

    for N in N_VALUES:

        durations_for_N = [

            row["activity_duration"]

            for row in all_results

            if row["N"] == N

        ]

        boxplot_data.append(
            durations_for_N
        )


    # ========================================================
    # MAXIMUM OBSERVABLE DURATION
    # ========================================================

    MAX_OBSERVABLE_DURATION = (
        T_MAX
        - STIMULUS_TIME
    )


    # ========================================================
    # CREATE BOXPLOT
    # ========================================================

    plt.figure(
        figsize=(10, 6)
    )


    plt.boxplot(

        boxplot_data,

        tick_labels=[
            str(N)
            for N in N_VALUES
        ],

        showmeans=True,

        meanline=False,

        showfliers=True,

        patch_artist=True,

    )


    # ========================================================
    # ADD INDIVIDUAL REALIZATIONS
    # ========================================================

    # This shows every network realization.
    #
    # A small horizontal jitter prevents points
    # from lying exactly on top of each other.

    rng = np.random.default_rng(42)


    for position, durations in enumerate(
        boxplot_data,
        start=1,
    ):

        jitter = rng.normal(

            loc=0.0,

            scale=0.04,

            size=len(durations),

        )


        plt.scatter(

            position + jitter,

            durations,

            s=18,

            alpha=0.45,

            zorder=3,

        )


    # ========================================================
    # OBSERVATION LIMIT
    # ========================================================

    plt.axhline(

        y=MAX_OBSERVABLE_DURATION,

        linestyle="--",

        linewidth=1.5,

        label=(
            f"Observation limit "
            f"({MAX_OBSERVABLE_DURATION:.0f} ms)"
        ),

    )


    # ========================================================
    # AXIS LABELS
    # ========================================================

    plt.xlabel(

        "Number of neurons, N",

        fontsize=13,

    )


    plt.ylabel(

        "Activity duration (ms)",

        fontsize=13,

    )


    # ========================================================
    # TITLE
    # ========================================================

    plt.title(

        "Distribution of Activity Duration vs Network Size\n"

        f"Fixed shortcut density p = {P}",

        fontsize=14,

    )


    # ========================================================
    # Y-AXIS
    # ========================================================

    plt.ylim(
        bottom=0
    )


    # ========================================================
    # GRID
    # ========================================================

    plt.grid(

        axis="y",

        alpha=0.3,

    )


    # ========================================================
    # LEGEND
    # ========================================================

    plt.legend(
        fontsize=10
    )


    # ========================================================
    # FINALIZE
    # ========================================================

    plt.tight_layout()


    # ========================================================
    # SAVE
    # ========================================================

    BOX_FIGURE_FILE = (

        RESULTS_DIR

        / "duration_vs_N_boxplot.png"

    )


    plt.savefig(

        BOX_FIGURE_FILE,

        dpi=300,

        bbox_inches="tight",

    )


    # ========================================================
    # SHOW
    # ========================================================

    plt.show()

    # ========================================================
    # FINAL RUNTIME
    # ========================================================

    total_runtime = (
        time.perf_counter()
        - experiment_start
    )

    print("\n")
    print("=" * 80)
    print("PHASE 14 COMPLETE")
    print("=" * 80)

    print(
        "\nTotal runtime =",
        f"{total_runtime / 60:.2f} minutes",
    )

    print("\nAll realizations:")
    print(ALL_FILE)

    print("\nSummary:")
    print(SUMMARY_FILE)

    print("\nFigure:")
    print(FIGURE_FILE)


# ============================================================
# WINDOWS MULTIPROCESSING ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()