"""
phase_12_N2000_failure_probability.py

PHASE 12
--------

Goal:

    Generate the failure-probability curve for N = 2000.

This is the first direct step toward reproducing the inset of Fig. 2:

        % Failure
            vs
        shortcut density p

For every p:

    1. Generate many random network realizations.
    2. Run the neural simulation.
    3. Classify each realization as SUCCESS or FAILURE.
    4. Calculate:

           P_failure =
               number of failures
               ------------------
               total realizations

    5. Plot:

           100 * P_failure

           versus

           p

IMPORTANT:

    Phase 11 showed that the pure N = 2000 ring
    dies around t ≈ 1000.

Therefore:

    T_MAX = 3000

and:

    final observation window = 2800 to 3000

are used here.

A realization is classified as SUCCESS only if
activity reaches the final observation window.
"""


# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path

import csv
import time

import numpy as np
import matplotlib.pyplot as plt


from network import (
    build_ring_network,
    add_random_shortcuts,
)


from simulator import (
    run_simulation,
)


# ============================================================
# PATH SETUP
# ============================================================

PROJECT_DIR = (
    Path(__file__)
    .resolve()
    .parent
)


RESULTS_DIR = (

    PROJECT_DIR

    / "results"

    / "phase12"

)


RESULTS_DIR.mkdir(

    parents=True,

    exist_ok=True,

)


ALL_REALIZATIONS_FILE = (

    RESULTS_DIR

    / "phase12_N2000_all_realizations.csv"

)


PROBABILITY_FILE = (

    RESULTS_DIR

    / "phase12_N2000_probability_curve.csv"

)


FIGURE_FILE = (

    RESULTS_DIR

    / "phase12_N2000_failure_probability.png"

)


# ============================================================
# NETWORK PARAMETERS
# ============================================================

N = 2000


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


T_MAX = 3000.0


STIMULUS_NEURON = (

    N // 2

)


STIMULUS_TIME = 10.0


# ============================================================
# CLASSIFICATION WINDOW
# ============================================================

FINAL_WINDOW_START = 2800.0

FINAL_WINDOW_END = 3000.0


# ============================================================
# NUMBER OF REALIZATIONS
# ============================================================

# Start with 100.
#
# After locating the transition region:
#
#     rerun only that region with:
#
#         500
#
# or ideally:
#
#         2000
#
# realizations.

NUM_REALIZATIONS = 100


# ============================================================
# p VALUES
# ============================================================

# Based on Phase 11 pilot results.
#
# IMPORTANT:
#
# This is a first exploratory sweep.
#
# After this run, refine the p grid around
# the actual transition region.

# ============================================================
# p VALUES — 20 EQUALLY SPACED VALUES FROM 0 TO 1
# ============================================================

P_VALUES = np.linspace(
    0.0,
    1.0,
    20,
)


# ============================================================
# CLASSIFY REALIZATION
# ============================================================

def classify_realization(

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

            "status":

                "FAILURE",


            "total_spikes":

                0,


            "last_spike_time":

                np.nan,


            "late_spikes":

                0,


            "activity_duration":

                0.0,

        }


    # --------------------------------------------------------
    # LAST SPIKE TIME
    # --------------------------------------------------------

    last_spike_time = float(

        np.max(

            spike_times

        )

    )


    # --------------------------------------------------------
    # ACTIVITY DURATION
    # --------------------------------------------------------

    activity_duration = (

        last_spike_time

        - STIMULUS_TIME

    )


    # --------------------------------------------------------
    # SPIKES IN FINAL WINDOW
    # --------------------------------------------------------

    late_spikes = int(

        np.sum(

            (

                spike_times

                >= FINAL_WINDOW_START

            )

            &

            (

                spike_times

                <= FINAL_WINDOW_END

            )

        )

    )


    # --------------------------------------------------------
    # CLASSIFICATION
    # --------------------------------------------------------

    if late_spikes > 0:


        status = "SUCCESS"


    else:


        status = "FAILURE"


    return {

        "status":

            status,


        "total_spikes":

            len(spike_times),


        "last_spike_time":

            last_spike_time,


        "late_spikes":

            late_spikes,


        "activity_duration":

            activity_duration,

    }


# ============================================================
# HEADER
# ============================================================

print("=" * 80)


print(

    "PHASE 12: N = 2000 FAILURE PROBABILITY CURVE"

)


print("=" * 80)


print("\nNETWORK")


print("-" * 50)


print(

    "N =",

    N,

)


print("\nNEURON PARAMETERS")


print("-" * 50)


print(

    "I_ext =",

    I_EXT,

)


print(

    "g_syn =",

    G_SYN,

)


print(

    "tau_m =",

    TAU_M,

)


print(

    "tau_D =",

    TAU_D,

)


print("\nSIMULATION")


print("-" * 50)


print(

    "dt =",

    DT,

)


print(

    "T_max =",

    T_MAX,

)


print(

    "Final observation window =",

    FINAL_WINDOW_START,

    "to",

    FINAL_WINDOW_END,

)


print(

    "Realizations per p =",

    NUM_REALIZATIONS,

)


print("\np VALUES")


print("-" * 50)


for p in P_VALUES:


    print(

        f"p = {p:8.5f} | "

        f"shortcuts = "

        f"{int(round(p * N)):3d}"

    )


# ============================================================
# STORAGE
# ============================================================

all_realization_results = []

probability_results = []


# ============================================================
# BUILD LOCAL RING ONCE
# ============================================================

print("\n")


print("=" * 80)


print(

    "BUILDING N = 2000 LOCAL RING"

)


print("=" * 80)


local_network = (

    build_ring_network(

        N

    )

)


print(

    "Local ring created."

)


print(

    "Local directed edges =",

    2 * N,

)


# ============================================================
# TOTAL TIMER
# ============================================================

total_start_time = (

    time.perf_counter()

)


# ============================================================
# RUN PROBABILITY SWEEP
# ============================================================

for p_index, p in enumerate(

    P_VALUES

):


    p = float(p)


    number_of_shortcuts = int(

        round(

            p * N

        )

    )


    print("\n")


    print("=" * 80)


    print(

        f"p = {p:.5f}"

    )


    print("=" * 80)


    print(

        "Shortcut count =",

        number_of_shortcuts,

    )


    print(

        "Progress =",

        f"{p_index + 1}/"

        f"{len(P_VALUES)}",

    )


    # --------------------------------------------------------
    # COUNTERS
    # --------------------------------------------------------

    success_count = 0

    failure_count = 0


    p_start_time = (

        time.perf_counter()

    )


    # ========================================================
    # NETWORK REALIZATIONS
    # ========================================================

    for seed in range(

        NUM_REALIZATIONS

    ):


        # ----------------------------------------------------
        # BUILD NETWORK
        # ----------------------------------------------------

        network, shortcuts = (

            add_random_shortcuts(

                outgoing_connections=

                    local_network,


                p=

                    p,


                seed=

                    seed,

            )

        )


        # ----------------------------------------------------
        # START RUN TIMER
        # ----------------------------------------------------

        run_start_time = (

            time.perf_counter()

        )


        # ----------------------------------------------------
        # RUN SIMULATION
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # RUNTIME
        # ----------------------------------------------------

        runtime_seconds = (

            time.perf_counter()

            - run_start_time

        )


        # ----------------------------------------------------
        # CLASSIFY
        # ----------------------------------------------------

        classification = (

            classify_realization(

                spike_times

            )

        )


        status = (

            classification[

                "status"

            ]

        )


        # ----------------------------------------------------
        # COUNT OUTCOME
        # ----------------------------------------------------

        if status == "SUCCESS":


            success_count += 1


        else:


            failure_count += 1


        # ----------------------------------------------------
        # SAVE REALIZATION
        # ----------------------------------------------------

        realization_row = {


            "N":

                N,


            "p":

                p,


            "seed":

                seed,


            "number_of_shortcuts":

                len(shortcuts),


            "status":

                status,


            "total_spikes":

                classification[

                    "total_spikes"

                ],


            "last_spike_time":

                classification[

                    "last_spike_time"

                ],


            "activity_duration":

                classification[

                    "activity_duration"

                ],


            "late_spikes":

                classification[

                    "late_spikes"

                ],


            "runtime_seconds":

                runtime_seconds,

        }


        all_realization_results.append(

            realization_row

        )


        # ----------------------------------------------------
        # PRINT PROGRESS
        # ----------------------------------------------------

        print(

            f"\r"

            f"Seed "

            f"{seed + 1:3d}/"

            f"{NUM_REALIZATIONS:3d} | "

            f"Success = "

            f"{success_count:3d} | "

            f"Failure = "

            f"{failure_count:3d}",

            end="",

            flush=True,

        )


    print()


    # ========================================================
    # CALCULATE PROBABILITIES
    # ========================================================

    probability_success = (

        success_count

        / NUM_REALIZATIONS

    )


    probability_failure = (

        failure_count

        / NUM_REALIZATIONS

    )


    percent_failure = (

        100.0

        * probability_failure

    )


    # --------------------------------------------------------
    # BINOMIAL STANDARD ERROR
    # --------------------------------------------------------

    standard_error = np.sqrt(

        probability_failure

        * (

            1.0

            - probability_failure

        )

        / NUM_REALIZATIONS

    )


    percent_standard_error = (

        100.0

        * standard_error

    )


    # --------------------------------------------------------
    # p RUNTIME
    # --------------------------------------------------------

    p_runtime = (

        time.perf_counter()

        - p_start_time

    )


    # --------------------------------------------------------
    # STORE PROBABILITY RESULT
    # --------------------------------------------------------

    probability_row = {


        "N":

            N,


        "p":

            p,


        "number_of_shortcuts":

            number_of_shortcuts,


        "realizations":

            NUM_REALIZATIONS,


        "success_count":

            success_count,


        "failure_count":

            failure_count,


        "probability_success":

            probability_success,


        "probability_failure":

            probability_failure,


        "percent_failure":

            percent_failure,


        "percent_standard_error":

            percent_standard_error,


        "runtime_seconds":

            p_runtime,

    }


    probability_results.append(

        probability_row

    )


    # --------------------------------------------------------
    # PRINT p SUMMARY
    # --------------------------------------------------------

    print("\nRESULT")


    print("-" * 50)


    print(

        "Successes =",

        success_count,

    )


    print(

        "Failures =",

        failure_count,

    )


    print(

        "P_success =",

        f"{probability_success:.3f}",

    )


    print(

        "P_failure =",

        f"{probability_failure:.3f}",

    )


    print(

        "% Failure =",

        f"{percent_failure:.1f}",

    )


    print(

        "Standard error =",

        f"{percent_standard_error:.2f}%",

    )


    print(

        "Runtime for p =",

        f"{p_runtime:.2f} seconds",

    )


# ============================================================
# SAVE ALL REALIZATIONS
# ============================================================

with open(

    ALL_REALIZATIONS_FILE,

    "w",

    newline="",

) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=

            list(

                all_realization_results[0].keys()

            ),

    )


    writer.writeheader()


    writer.writerows(

        all_realization_results

    )


# ============================================================
# SAVE PROBABILITY CURVE
# ============================================================

with open(

    PROBABILITY_FILE,

    "w",

    newline="",

) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=

            list(

                probability_results[0].keys()

            ),

    )


    writer.writeheader()


    writer.writerows(

        probability_results

    )


# ============================================================
# PRINT FINAL PROBABILITY TABLE
# ============================================================

print("\n")


print("=" * 80)


print(

    "N = 2000 FAILURE PROBABILITY CURVE"

)


print("=" * 80)


print(

    f"{'p':>10s} | "

    f"{'Shortcuts':>9s} | "

    f"{'Success':>7s} | "

    f"{'Failure':>7s} | "

    f"{'% Failure':>10s}"

)


print("-" * 65)


for row in probability_results:


    print(

        f"{row['p']:10.5f} | "

        f"{row['number_of_shortcuts']:9d} | "

        f"{row['success_count']:7d} | "

        f"{row['failure_count']:7d} | "

        f"{row['percent_failure']:10.1f}"

    )


# ============================================================
# FIND APPROXIMATE CRITICAL p
# ============================================================

mixed_rows = [

    row

    for row in probability_results

    if (

        row["probability_failure"] > 0.0

        and

        row["probability_failure"] < 1.0

    )

]


if len(mixed_rows) > 0:


    critical_row = min(

        mixed_rows,

        key=lambda row:

            abs(

                row["probability_failure"]

                - 0.5

            )

    )


else:


    critical_row = min(

        probability_results,

        key=lambda row:

            abs(

                row["probability_failure"]

                - 0.5

            )

    )


p_critical_estimate = (

    critical_row["p"]

)


print("\n")


print("=" * 80)


print(

    "APPROXIMATE CRITICAL POINT"

)


print("=" * 80)


print(

    "p_cr estimate =",

    p_critical_estimate,

)


print(

    "P_failure at p_cr =",

    critical_row[

        "probability_failure"

    ],

)


print(

    "Number of shortcuts =",

    critical_row[

        "number_of_shortcuts"

    ],

)


# ============================================================
# EXTRACT PLOT DATA
# ============================================================

plot_p = np.array(

    [

        row["p"]

        for row in probability_results

    ]

)


plot_failure = np.array(

    [

        row["percent_failure"]

        for row in probability_results

    ]

)


plot_error = np.array(

    [

        row["percent_standard_error"]

        for row in probability_results

    ]

)


# ============================================================
# PLOT FAILURE CURVE
# ============================================================

plt.figure(

    figsize=(8, 6)

)


plt.errorbar(

    plot_p,

    plot_failure,

    yerr=plot_error,

    marker="o",

    linewidth=1.5,

    capsize=4,

)


# ------------------------------------------------------------
# 50% FAILURE LINE
# ------------------------------------------------------------

plt.axhline(

    50.0,

    linestyle="--",

    linewidth=1,

)


# ------------------------------------------------------------
# ESTIMATED CRITICAL p
# ------------------------------------------------------------

plt.axvline(

    p_critical_estimate,

    linestyle=":",

    linewidth=1,

)


plt.xlabel(

    "Shortcut density p"

)


plt.ylabel(

    "% Failure"

)


plt.title(

    "Failure Probability at N = 2000"

)


plt.ylim(

    -5,

    105,

)


plt.grid(

    True,

    alpha=0.3,

)


plt.tight_layout()


plt.savefig(

    FIGURE_FILE,

    dpi=300,

    bbox_inches="tight",

)


plt.show()


# ============================================================
# TOTAL RUNTIME
# ============================================================

total_runtime = (

    time.perf_counter()

    - total_start_time

)


# ============================================================
# VALIDATION
# ============================================================

print("\n")


print("=" * 80)


print(

    "PHASE 12 VALIDATION"

)


print("=" * 80)


expected_runs = (

    len(P_VALUES)

    * NUM_REALIZATIONS

)


actual_runs = (

    len(

        all_realization_results

    )

)


if actual_runs == expected_runs:


    print("PASSED")


    print(

        "Completed",

        actual_runs,

        "simulations."

    )


else:


    print("FAILED")


# ============================================================
# NEXT-STEP DIAGNOSTIC
# ============================================================

print("\n")


print("=" * 80)


print(

    "TRANSITION DIAGNOSTIC"

)


print("=" * 80)


if len(mixed_rows) == 0:


    print(

        "WARNING: No mixed transition point was found."

    )


    print(

        "The p range must be changed or refined."

    )


else:


    print(

        "Mixed transition points found:"

    )


    for row in mixed_rows:


        print(

            f"p = {row['p']:.5f} | "

            f"P_failure = "

            f"{row['probability_failure']:.3f}"

        )


    print(

        "\nRefine the next sweep around:"

    )


    print(

        "p_cr ≈",

        p_critical_estimate,

    )


# ============================================================
# OUTPUT FILES
# ============================================================

print("\n")


print("=" * 80)


print(

    "RESULTS SAVED"

)


print("=" * 80)


print(

    "\nAll realizations:"

)


print(

    ALL_REALIZATIONS_FILE

)


print(

    "\nProbability curve:"

)


print(

    PROBABILITY_FILE

)


print(

    "\nFigure:"

)


print(

    FIGURE_FILE

)


print(

    "\nTotal runtime =",

    f"{total_runtime:.2f} seconds",

)


print("\n")


print("=" * 80)


print(

    "PHASE 12 COMPLETE"

)


print("=" * 80)