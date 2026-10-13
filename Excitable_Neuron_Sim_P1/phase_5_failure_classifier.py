# git """
# phase_5_failure_classifier.py

# PHASE 5
# -------

# Automatically classify different network realizations as:

#     SUCCESS
#     FAILURE

# and measure:

#     - total spikes
#     - last spike time
#     - persistence duration
#     - spikes in final observation window

# This implements project task (e).
# """

from pathlib import Path
import csv

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
    / "phase5"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# NETWORK PARAMETERS
# ============================================================

N = 100
P = 0.1

N_REALIZATIONS = 20


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

STIMULUS_NEURON = N // 2
STIMULUS_TIME = 10.0


# ============================================================
# CLASSIFIER PARAMETERS
# ============================================================

FINAL_WINDOW = 20.0

FINAL_WINDOW_START = (
    T_MAX - FINAL_WINDOW
)


# ============================================================
# PERSISTENCE CLASSIFIER
# ============================================================

def classify_activity(
    spike_times,
    stimulus_time,
    t_max,
    final_window,
):
    """
    Classify one simulation.

    SUCCESS:
        Activity exists in the final observation window.

    FAILURE:
        Activity dies before the final observation window.

    Returns
    -------
    Dictionary containing classification results.
    """

    spike_times = np.asarray(
        spike_times,
        dtype=float,
    )


    # --------------------------------------------------------
    # NO SPIKES
    # --------------------------------------------------------

    if len(spike_times) == 0:

        return {

            "status": "FAILURE",

            "persistent": False,

            "total_spikes": 0,

            "last_spike_time": 0.0,

            "persistence_duration": 0.0,

            "spikes_in_final_window": 0,
        }


    # --------------------------------------------------------
    # LAST SPIKE TIME
    # --------------------------------------------------------

    last_spike_time = float(
        spike_times[-1]
    )


    # --------------------------------------------------------
    # PERSISTENCE DURATION
    # --------------------------------------------------------

    persistence_duration = max(

        0.0,

        last_spike_time
        - stimulus_time
    )


    # --------------------------------------------------------
    # FINAL OBSERVATION WINDOW
    # --------------------------------------------------------

    final_window_start = (

        t_max
        - final_window
    )


    final_spikes = spike_times[

        spike_times
        >= final_window_start
    ]


    spikes_in_final_window = len(
        final_spikes
    )


    # --------------------------------------------------------
    # CLASSIFICATION
    # --------------------------------------------------------

    persistent = (

        spikes_in_final_window
        > 0
    )


    if persistent:

        status = "SUCCESS"

    else:

        status = "FAILURE"


    return {

        "status": status,

        "persistent": persistent,

        "total_spikes": len(spike_times),

        "last_spike_time":
            last_spike_time,

        "persistence_duration":
            persistence_duration,

        "spikes_in_final_window":
            spikes_in_final_window,
    }


# ============================================================
# EXPERIMENT HEADER
# ============================================================

print("=" * 80)

print(
    "PHASE 5: FAILURE VS SUCCESS CLASSIFIER"
)

print("=" * 80)


print("\nNETWORK")

print("-" * 50)

print("N =", N)

print("p =", P)

print(
    "Number of shortcuts =",
    int(round(P * N)),
)


print("\nNEURON PARAMETERS")

print("-" * 50)

print("I_ext =", I_EXT)

print("g_syn =", G_SYN)

print("tau_m =", TAU_M)

print("tau_D =", TAU_D)


print("\nCLASSIFICATION RULE")

print("-" * 50)

print(

    f"Final observation window: "

    f"{FINAL_WINDOW_START} "

    f"to {T_MAX}"
)

print(

    "SUCCESS = activity reaches "
    "the final observation window"
)

print(

    "FAILURE = activity dies before "
    "the final observation window"
)


# ============================================================
# STORAGE
# ============================================================

results = []

success_count = 0

failure_count = 0


# ============================================================
# RUN REALIZATIONS
# ============================================================

print("\n")

print("=" * 80)

print("RUNNING NETWORK REALIZATIONS")

print("=" * 80)


for seed in range(N_REALIZATIONS):


    # --------------------------------------------------------
    # BUILD LOCAL RING
    # --------------------------------------------------------

    local_network = (
        build_ring_network(N)
    )


    # --------------------------------------------------------
    # ADD RANDOM SHORTCUTS
    # --------------------------------------------------------

    small_world_network, shortcuts = (
        add_random_shortcuts(

            outgoing_connections=
                local_network,

            p=P,

            seed=seed,
        )
    )


    # --------------------------------------------------------
    # RUN SIMULATION
    # --------------------------------------------------------

    spike_times, spike_neurons = (
        run_simulation(

            outgoing_connections=
                small_world_network,

            I_ext=I_EXT,

            g_syn=G_SYN,

            tau_m=TAU_M,

            tau_D=TAU_D,

            dt=DT,

            t_max=T_MAX,

            stimulus_neuron=
                STIMULUS_NEURON,

            stimulus_time=
                STIMULUS_TIME,
        )
    )


    # --------------------------------------------------------
    # CLASSIFY
    # --------------------------------------------------------

    result = classify_activity(

        spike_times=spike_times,

        stimulus_time=
            STIMULUS_TIME,

        t_max=T_MAX,

        final_window=
            FINAL_WINDOW,
    )


    # --------------------------------------------------------
    # COUNT OUTCOMES
    # --------------------------------------------------------

    if result["persistent"]:

        success_count += 1

    else:

        failure_count += 1


    # --------------------------------------------------------
    # STORE RESULT
    # --------------------------------------------------------

    row = {

        "seed": seed,

        "N": N,

        "p": P,

        "number_of_shortcuts":
            len(shortcuts),

        "status":
            result["status"],

        "total_spikes":
            result["total_spikes"],

        "last_spike_time":
            result["last_spike_time"],

        "persistence_duration":
            result[
                "persistence_duration"
            ],

        "spikes_in_final_window":
            result[
                "spikes_in_final_window"
            ],
    }


    results.append(row)


    # --------------------------------------------------------
    # PRINT RESULT
    # --------------------------------------------------------

    print(

        f"Seed {seed:2d} | "

        f"{result['status']:7s} | "

        f"Spikes = "
        f"{result['total_spikes']:5d} | "

        f"Last = "
        f"{result['last_spike_time']:7.2f} | "

        f"Duration = "
        f"{result['persistence_duration']:7.2f} | "

        f"Late spikes = "
        f"{result['spikes_in_final_window']:4d}"
    )


# ============================================================
# CALCULATE PROBABILITIES
# ============================================================

success_probability = (

    success_count
    / N_REALIZATIONS
)


failure_probability = (

    failure_count
    / N_REALIZATIONS
)


# ============================================================
# SUMMARY
# ============================================================

print("\n")

print("=" * 80)

print("PHASE 5 CLASSIFICATION SUMMARY")

print("=" * 80)


print(

    "Total realizations:",

    N_REALIZATIONS
)


print(

    "Successful realizations:",

    success_count
)


print(

    "Failed realizations:",

    failure_count
)


print(

    "Estimated probability of success:",

    success_probability
)


print(

    "Estimated probability of failure:",

    failure_probability
)


# ============================================================
# SUCCESS AND FAILURE SEEDS
# ============================================================

success_seeds = [

    row["seed"]

    for row in results

    if row["status"] == "SUCCESS"
]


failure_seeds = [

    row["seed"]

    for row in results

    if row["status"] == "FAILURE"
]


print("\nSUCCESS SEEDS")

print("-" * 50)

print(success_seeds)


print("\nFAILURE SEEDS")

print("-" * 50)

print(failure_seeds)


# ============================================================
# SAVE RESULTS
# ============================================================

output_file = (

    RESULTS_DIR

    / "phase5_classification_results.csv"
)


fieldnames = [

    "seed",

    "N",

    "p",

    "number_of_shortcuts",

    "status",

    "total_spikes",

    "last_spike_time",

    "persistence_duration",

    "spikes_in_final_window",
]


with open(

    output_file,

    "w",

    newline="",

) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=fieldnames,
    )


    writer.writeheader()


    writer.writerows(
        results
    )


print("\nResults saved to:")

print(output_file)


# ============================================================
# VALIDATION
# ============================================================

print("\n")

print("=" * 80)

print("CLASSIFIER VALIDATION")

print("=" * 80)


if (
    success_count > 0
    and failure_count > 0
):

    print("PASSED")

    print(

        "The classifier detected both "
        "SUCCESS and FAILURE realizations."
    )

else:

    print(

        "Only one outcome type was found "
        "in this realization sample."
    )


print("\n")

print("=" * 80)

print("PHASE 5 COMPLETE")

print("=" * 80)