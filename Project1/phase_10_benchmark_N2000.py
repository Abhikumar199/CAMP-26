"""
phase_10_benchmark_N2000.py

PHASE 10
--------

Goal:

    Test whether the current simulator can handle
    the paper-scale network:

        N = 2000

Before running a large probability sweep, benchmark:

    - runtime
    - number of spikes
    - last spike time
    - SUCCESS / FAILURE
    - shortcut count

This phase does NOT estimate the final probability curve.

It answers:

    1. Does N = 2000 run correctly?
    2. How long does one realization take?
    3. Which p values show interesting behavior?
    4. Is a larger Phase 11 sweep computationally practical?
"""

from pathlib import Path
import csv
import time

import numpy as np

from network import (
    build_ring_network,
    add_random_shortcuts,
)

from simulator import run_simulation


# ============================================================
# PATH SETUP
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent

RESULTS_DIR = (
    PROJECT_DIR
    / "results"
    / "phase10"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

RESULTS_FILE = (
    RESULTS_DIR
    / "phase10_N2000_benchmark.csv"
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

T_MAX = 200.0

STIMULUS_TIME = 10.0

STIMULUS_NEURON = N // 2


# ============================================================
# BENCHMARK PARAMETERS
# ============================================================

# Start small.
#
# Do NOT use 100 or 2000 realizations yet.

NUM_REALIZATIONS = 10


# Initial coarse p values.
#
# We are only checking:
#
#     runtime
#     stability
#     approximate behavior

P_VALUES = np.array([

    0.001,

    0.002,

    0.005,

    0.010,

    0.020,

])


# ============================================================
# CLASSIFICATION PARAMETERS
# ============================================================

FINAL_WINDOW_START = 180.0

FINAL_WINDOW_END = T_MAX


# ============================================================
# CLASSIFY ONE REALIZATION
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
    # SUCCESS / FAILURE
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
    }


# ============================================================
# HEADER
# ============================================================

print("=" * 80)

print(
    "PHASE 10: N = 2000 BENCHMARK"
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
    "t_max =",
    T_MAX,
)

print(
    "Realizations per p =",
    NUM_REALIZATIONS,
)


print("\np VALUES")

print("-" * 50)

print(
    P_VALUES
)


# ============================================================
# STORAGE
# ============================================================

all_results = []


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
    build_ring_network(N)
)


print(
    "Local ring created."
)

print(
    "Local directed edges =",
    2 * N,
)


# ============================================================
# TOTAL BENCHMARK TIMER
# ============================================================

benchmark_start_time = (
    time.perf_counter()
)


# ============================================================
# RUN p VALUES
# ============================================================

for p_index, p in enumerate(
    P_VALUES
):


    print("\n")

    print("=" * 80)

    print(
        f"BENCHMARKING p = {p:.4f}"
    )

    print("=" * 80)


    expected_shortcuts = int(
        round(
            p * N
        )
    )


    print(
        "Expected shortcuts =",
        expected_shortcuts,
    )


    p_start_time = (
        time.perf_counter()
    )


    success_count = 0

    failure_count = 0


    # ========================================================
    # REALIZATIONS
    # ========================================================

    for seed in range(
        NUM_REALIZATIONS
    ):


        # ----------------------------------------------------
        # BUILD EXACT NETWORK
        # ----------------------------------------------------

        network, shortcuts = (
            add_random_shortcuts(

                outgoing_connections=
                    local_network,

                p=
                    float(p),

                seed=
                    seed,
            )
        )


        # ----------------------------------------------------
        # START TIMER
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
        # END TIMER
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
        # COUNT OUTCOMES
        # ----------------------------------------------------

        if status == "SUCCESS":

            success_count += 1

        else:

            failure_count += 1


        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------

        result = {

            "N":
                N,

            "p":
                float(p),

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

            "late_spikes":
                classification[
                    "late_spikes"
                ],

            "runtime_seconds":
                runtime_seconds,
        }


        all_results.append(
            result
        )


        # ----------------------------------------------------
        # PRINT RESULT
        # ----------------------------------------------------

        print(

            f"Seed {seed:2d} | "

            f"{status:7s} | "

            f"Shortcuts = "
            f"{len(shortcuts):3d} | "

            f"Spikes = "
            f"{classification['total_spikes']:6d} | "

            f"Last = "
            f"{classification['last_spike_time']:7.2f} | "

            f"Late = "
            f"{classification['late_spikes']:5d} | "

            f"Runtime = "
            f"{runtime_seconds:7.2f} s"

        )


    # ========================================================
    # p SUMMARY
    # ========================================================

    p_runtime = (

        time.perf_counter()

        - p_start_time

    )


    probability_success = (

        success_count

        / NUM_REALIZATIONS

    )


    probability_failure = (

        failure_count

        / NUM_REALIZATIONS

    )


    p_runtimes = [

        row["runtime_seconds"]

        for row in all_results

        if np.isclose(
            row["p"],
            p,
        )
    ]


    mean_runtime = float(
        np.mean(
            p_runtimes
        )
    )


    print("\nSUMMARY")

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
        "Estimated P_success =",
        probability_success,
    )

    print(
        "Estimated P_failure =",
        probability_failure,
    )

    print(
        "Mean runtime per realization =",
        f"{mean_runtime:.2f} s",
    )

    print(
        "Total runtime for this p =",
        f"{p_runtime:.2f} s",
    )


# ============================================================
# TOTAL BENCHMARK TIME
# ============================================================

total_benchmark_time = (

    time.perf_counter()

    - benchmark_start_time

)


# ============================================================
# SAVE RESULTS
# ============================================================

with open(
    RESULTS_FILE,
    "w",
    newline="",
) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=[
            "N",
            "p",
            "seed",
            "number_of_shortcuts",
            "status",
            "total_spikes",
            "last_spike_time",
            "late_spikes",
            "runtime_seconds",
        ],
    )


    writer.writeheader()


    writer.writerows(
        all_results
    )


# ============================================================
# FINAL SUMMARY TABLE
# ============================================================

print("\n")

print("=" * 80)

print(
    "PHASE 10 BENCHMARK SUMMARY"
)

print("=" * 80)


for p in P_VALUES:


    p_rows = [

        row

        for row in all_results

        if np.isclose(
            row["p"],
            p,
        )
    ]


    successes = sum(

        row["status"]
        == "SUCCESS"

        for row in p_rows

    )


    failures = sum(

        row["status"]
        == "FAILURE"

        for row in p_rows

    )


    mean_runtime = float(

        np.mean(

            [
                row[
                    "runtime_seconds"
                ]

                for row in p_rows
            ]

        )

    )


    print(

        f"p = {p:7.4f} | "

        f"Shortcuts = "
        f"{int(round(p * N)):3d} | "

        f"Success = "
        f"{successes:2d} | "

        f"Failure = "
        f"{failures:2d} | "

        f"Mean runtime = "
        f"{mean_runtime:7.2f} s"

    )


# ============================================================
# RUNTIME PROJECTION
# ============================================================

all_runtimes = [

    row["runtime_seconds"]

    for row in all_results

]


overall_mean_runtime = float(

    np.mean(
        all_runtimes
    )

)


print("\n")

print("=" * 80)

print(
    "RUNTIME PROJECTION"
)

print("=" * 80)


print(
    "Mean runtime per realization =",
    f"{overall_mean_runtime:.2f} seconds",
)


for number_of_runs in [
    100,
    500,
    2000,
]:


    projected_seconds = (

        overall_mean_runtime

        * number_of_runs

    )


    projected_minutes = (

        projected_seconds

        / 60.0

    )


    projected_hours = (

        projected_minutes

        / 60.0

    )


    print(

        f"{number_of_runs:4d} simulations: "

        f"{projected_minutes:8.2f} minutes "

        f"({projected_hours:6.2f} hours)"

    )


# ============================================================
# VALIDATION
# ============================================================

print("\n")

print("=" * 80)

print(
    "PHASE 10 VALIDATION"
)

print("=" * 80)


expected_total_runs = (

    len(P_VALUES)

    * NUM_REALIZATIONS

)


if len(all_results) == expected_total_runs:


    print("PASSED")


    print(

        f"Completed all "
        f"{expected_total_runs} "
        f"N = 2000 benchmark simulations."

    )


else:


    print("FAILED")


# ============================================================
# OUTPUT
# ============================================================

print("\n")

print("=" * 80)

print(
    "RESULTS SAVED"
)

print("=" * 80)


print(
    RESULTS_FILE
)


print(
    "\nTotal benchmark runtime =",
    f"{total_benchmark_time:.2f} seconds",
)


print("\n")

print("=" * 80)

print(
    "PHASE 10 COMPLETE"
)

print("=" * 80)