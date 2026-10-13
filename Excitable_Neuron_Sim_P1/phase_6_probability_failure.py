"""
phase_6_probability_failure.py

PHASE 6
-------

Estimate:

    P_failure(p)
    P_success(p)

for different shortcut probabilities p.

For every p:
    1. Generate multiple network realizations.
    2. Run the simulation.
    3. Classify each realization using the Phase 5 rule.
    4. Calculate failure and success probabilities.
    5. Save results and plot the probability curves.
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
# PATH SETUP
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent

RESULTS_DIR = (
    PROJECT_DIR
    / "results"
    / "phase6"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# NETWORK PARAMETERS
# ============================================================

N = 100

P_VALUES = np.arange(
    0.00,
    0.301,
    0.02,
)

N_REALIZATIONS = 50


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
    T_MAX
    - FINAL_WINDOW
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
    "PHASE 6: PROBABILITY OF FAILURE VS p"
)

print("=" * 80)


print("\nNETWORK")

print("-" * 50)

print("N =", N)

print(
    "p values =",
    [
        round(float(p), 2)
        for p in P_VALUES
    ],
)

print(
    "Realizations per p =",
    N_REALIZATIONS,
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

all_results = []

probability_results = []


# ============================================================
# RUN p SWEEP
# ============================================================

print("\n")

print("=" * 80)

print("RUNNING p SWEEP")

print("=" * 80)


for p in P_VALUES:


    p = float(p)


    # --------------------------------------------------------
    # COUNTERS
    # --------------------------------------------------------

    success_count = 0

    failure_count = 0


    print("\n")

    print("-" * 80)

    print(
        f"p = {p:.2f}"
    )

    print("-" * 80)


    # --------------------------------------------------------
    # RUN NETWORK REALIZATIONS
    # --------------------------------------------------------

    for seed in range(
        N_REALIZATIONS
    ):


        # ----------------------------------------------------
        # BUILD LOCAL RING
        # ----------------------------------------------------

        local_network = (
            build_ring_network(N)
        )


        # ----------------------------------------------------
        # ADD RANDOM SHORTCUTS
        # ----------------------------------------------------

        small_world_network, shortcuts = (
            add_random_shortcuts(

                outgoing_connections=
                    local_network,

                p=p,

                seed=seed,
            )
        )


        # ----------------------------------------------------
        # RUN SIMULATION
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # CLASSIFY
        # ----------------------------------------------------

        result = classify_activity(

            spike_times=spike_times,

            stimulus_time=
                STIMULUS_TIME,

            t_max=T_MAX,

            final_window=
                FINAL_WINDOW,
        )


        # ----------------------------------------------------
        # COUNT OUTCOMES
        # ----------------------------------------------------

        if result["persistent"]:

            success_count += 1

        else:

            failure_count += 1


        # ----------------------------------------------------
        # STORE INDIVIDUAL RESULT
        # ----------------------------------------------------

        row = {

            "p": p,

            "seed": seed,

            "N": N,

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


        all_results.append(row)


        # ----------------------------------------------------
        # PRINT PROGRESS
        # ----------------------------------------------------

        print(

            f"Seed {seed:2d} | "

            f"{result['status']:7s} | "

            f"Spikes = "
            f"{result['total_spikes']:5d} | "

            f"Last = "
            f"{result['last_spike_time']:7.2f} | "

            f"Late = "
            f"{result['spikes_in_final_window']:4d}"
        )


    # --------------------------------------------------------
    # CALCULATE PROBABILITIES
    # --------------------------------------------------------

    success_probability = (

        success_count
        / N_REALIZATIONS
    )


    failure_probability = (

        failure_count
        / N_REALIZATIONS
    )


    # --------------------------------------------------------
    # STORE p SUMMARY
    # --------------------------------------------------------

    probability_results.append({

        "p": p,

        "success_count":
            success_count,

        "failure_count":
            failure_count,

        "probability_success":
            success_probability,

        "probability_failure":
            failure_probability,
    })


    # --------------------------------------------------------
    # PRINT p SUMMARY
    # --------------------------------------------------------

    print("\n")

    print(

        f"p = {p:.2f} | "

        f"Success = "
        f"{success_count}/{N_REALIZATIONS} | "

        f"Failure = "
        f"{failure_count}/{N_REALIZATIONS} | "

        f"P_success = "
        f"{success_probability:.3f} | "

        f"P_failure = "
        f"{failure_probability:.3f}"
    )


# ============================================================
# SAVE ALL REALIZATIONS
# ============================================================

all_results_file = (

    RESULTS_DIR

    / "phase6_all_realizations.csv"
)


fieldnames = [

    "p",

    "seed",

    "N",

    "number_of_shortcuts",

    "status",

    "total_spikes",

    "last_spike_time",

    "persistence_duration",

    "spikes_in_final_window",
]


with open(

    all_results_file,

    "w",

    newline="",

) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=fieldnames,
    )


    writer.writeheader()


    writer.writerows(
        all_results
    )


# ============================================================
# SAVE PROBABILITY CURVE
# ============================================================

probability_file = (

    RESULTS_DIR

    / "phase6_probability_curve.csv"
)


probability_fieldnames = [

    "p",

    "success_count",

    "failure_count",

    "probability_success",

    "probability_failure",
]


with open(

    probability_file,

    "w",

    newline="",

) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=
            probability_fieldnames,
    )


    writer.writeheader()


    writer.writerows(
        probability_results
    )


# ============================================================
# PREPARE PLOT DATA
# ============================================================

plot_p = np.array([

    row["p"]

    for row in probability_results
])


plot_success = np.array([

    row["probability_success"]

    for row in probability_results
])


plot_failure = np.array([

    row["probability_failure"]

    for row in probability_results
])


# ============================================================
# PLOT
# ============================================================

plt.figure(
    figsize=(9, 6)
)


plt.plot(

    plot_p,

    plot_failure,

    marker="o",

    linewidth=2,

    label="Failure probability",
)


plt.plot(

    plot_p,

    plot_success,

    marker="s",

    linewidth=2,

    label="Success probability",
)


plt.xlabel(
    "Shortcut probability p"
)


plt.ylabel(
    "Estimated probability"
)


plt.title(
    "Propagation Failure and Success Probability vs p"
)


plt.ylim(
    -0.05,
    1.05,
)


plt.grid(
    True,
    alpha=0.3,
)


plt.legend()


plt.tight_layout()


figure_file = (

    RESULTS_DIR

    / "phase6_probability_failure.png"
)


plt.savefig(

    figure_file,

    dpi=300,

    bbox_inches="tight",
)


plt.show()


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")

print("=" * 80)

print("PHASE 6 PROBABILITY SUMMARY")

print("=" * 80)


for row in probability_results:

    print(

        f"p = {row['p']:.2f} | "

        f"Success = "
        f"{row['success_count']:2d} | "

        f"Failure = "
        f"{row['failure_count']:2d} | "

        f"P_success = "
        f"{row['probability_success']:.3f} | "

        f"P_failure = "
        f"{row['probability_failure']:.3f}"
    )


# ============================================================
# TRANSITION REGION
# ============================================================

transition_rows = [

    row

    for row in probability_results

    if (
        row["probability_success"] > 0.0

        and

        row["probability_success"] < 1.0
    )
]


print("\n")

print("=" * 80)

print("TRANSITION REGION")

print("=" * 80)


if len(transition_rows) > 0:

    print(

        "Values of p where both "
        "SUCCESS and FAILURE occur:"
    )


    for row in transition_rows:

        print(

            f"p = {row['p']:.2f} | "

            f"P_success = "
            f"{row['probability_success']:.3f} | "

            f"P_failure = "
            f"{row['probability_failure']:.3f}"
        )


else:

    print(

        "No mixed SUCCESS/FAILURE region "
        "was detected."
    )


# ============================================================
# OUTPUT FILES
# ============================================================

print("\n")

print("=" * 80)

print("RESULTS SAVED")

print("=" * 80)


print("\nAll realizations:")

print(
    all_results_file
)


print("\nProbability curve:")

print(
    probability_file
)


print("\nFigure:")

print(
    figure_file
)


print("\n")

print("=" * 80)

print("PHASE 6 COMPLETE")

print("=" * 80)