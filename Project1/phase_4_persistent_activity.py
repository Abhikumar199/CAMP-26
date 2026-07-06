"""
phase_4_persistent_activity.py

PHASE 4
-------

Design an algorithm to classify one simulation as:

    SUCCESS  -> activity is still present near T_MAX
    FAILURE  -> activity dies before T_MAX

Also measure:

    - failure time
    - persistence duration after the initial stimulus
    - total spikes
    - last spike time

This directly implements project task (e).
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
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

FIGURE_DIR = (
    PROJECT_DIR
    / "figures"
    / "phase4"
)

FIGURE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# MODEL PARAMETERS
# ============================================================

N = 100

P = 0.1

SEED = 3


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
# CLASSIFICATION PARAMETERS
# ============================================================

"""
We classify activity using a final observation window.

Example:

T_MAX = 200
FINAL_WINDOW = 20

Then we ask:

Were there spikes between t = 180 and t = 200?

If yes:
    SUCCESS

If no:
    FAILURE
"""

FINAL_WINDOW = 20.0


# ============================================================
# PERSISTENCE CLASSIFIER
# ============================================================

def classify_persistent_activity(
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
    # CASE 1 — NO SPIKES
    # --------------------------------------------------------

    if len(spike_times) == 0:

        return {
            "status": "FAILURE",

            "persistent": False,

            "total_spikes": 0,

            "last_spike_time": None,

            "persistence_duration": 0.0,

            "spikes_in_final_window": 0,
        }


    # --------------------------------------------------------
    # LAST SPIKE
    # --------------------------------------------------------

    last_spike_time = float(
        spike_times[-1]
    )


    # --------------------------------------------------------
    # ACTIVITY DURATION
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


    spikes_in_final_window = np.sum(

        spike_times
        >= final_window_start
    )


    # --------------------------------------------------------
    # SUCCESS / FAILURE
    # --------------------------------------------------------

    persistent = (

        spikes_in_final_window
        > 0
    )


    if persistent:

        status = "SUCCESS"

    else:

        status = "FAILURE"


    # --------------------------------------------------------
    # RETURN RESULTS
    # --------------------------------------------------------

    return {
        "status": status,

        "persistent": persistent,

        "total_spikes": len(spike_times),

        "last_spike_time": last_spike_time,

        "persistence_duration": persistence_duration,

        "spikes_in_final_window": int(
            spikes_in_final_window
        ),
    }


# ============================================================
# STEP 1 — BUILD LOCAL RING
# ============================================================

print("=" * 60)

print("PHASE 4: PERSISTENT ACTIVITY CLASSIFIER")

print("=" * 60)


local_network = build_ring_network(
    N
)


# ============================================================
# STEP 2 — ADD RANDOM SHORTCUTS
# ============================================================

small_world_network, shortcuts = (
    add_random_shortcuts(

        outgoing_connections=local_network,

        p=P,

        seed=SEED,
    )
)


print("\nNETWORK")

print("-" * 40)

print("N:", N)

print("p:", P)

print("seed:", SEED)

print(
    "Number of shortcuts:",
    len(shortcuts),
)


# ============================================================
# STEP 3 — SINGLE INPUT AND SIMULATION
# ============================================================

spike_times, spike_neurons = run_simulation(

    outgoing_connections=small_world_network,

    I_ext=I_EXT,

    g_syn=G_SYN,

    tau_m=TAU_M,

    tau_D=TAU_D,

    dt=DT,

    t_max=T_MAX,

    stimulus_neuron=STIMULUS_NEURON,

    stimulus_time=STIMULUS_TIME,
)


spike_times = np.asarray(
    spike_times,
    dtype=float,
)

spike_neurons = np.asarray(
    spike_neurons,
    dtype=int,
)


# ============================================================
# STEP 4 — CLASSIFY THE SIMULATION
# ============================================================

result = classify_persistent_activity(

    spike_times=spike_times,

    stimulus_time=STIMULUS_TIME,

    t_max=T_MAX,

    final_window=FINAL_WINDOW,
)


# ============================================================
# STEP 5 — PRINT RESULTS
# ============================================================

print("\nCLASSIFICATION RESULTS")

print("-" * 40)


print(
    "Status:",
    result["status"],
)


print(
    "Persistent:",
    result["persistent"],
)


print(
    "Total spikes:",
    result["total_spikes"],
)


print(
    "Last spike time:",
    result["last_spike_time"],
)


print(
    "Persistence duration:",
    result["persistence_duration"],
)


print(
    "Spikes in final window:",
    result["spikes_in_final_window"],
)


print(
    "Final window:",
    f"{T_MAX - FINAL_WINDOW} to {T_MAX}",
)


# ============================================================
# STEP 6 — EXPLAIN THE DECISION
# ============================================================

print("\nDECISION")

print("-" * 40)


if result["persistent"]:

    print(
        "SUCCESS:"
    )

    print(
        "Activity was still present "
        "near the end of the simulation."
    )

else:

    print(
        "FAILURE:"
    )

    print(
        "Activity disappeared before "
        "the final observation window."
    )


# ============================================================
# STEP 7 — RASTER PLOT
# ============================================================

plt.figure(
    figsize=(12, 6)
)


plt.scatter(

    spike_times,

    spike_neurons,

    s=8,
)


# Mark beginning of final observation window

plt.axvline(

    T_MAX - FINAL_WINDOW,

    linestyle="--",

    label="Final observation window",
)


plt.xlabel(
    "Time"
)


plt.ylabel(
    "Neuron index"
)


plt.title(

    f"Phase 4: Persistent Activity Classification\n"

    f"Seed = {SEED}, "
    f"p = {P}, "
    f"Result = {result['status']}"
)


plt.xlim(
    0,
    T_MAX,
)


plt.legend()


plt.tight_layout()


# ============================================================
# SAVE FIGURE
# ============================================================

output_file = (

    FIGURE_DIR

    / f"seed_{SEED}_"
      f"{result['status'].lower()}.png"
)


plt.savefig(

    output_file,

    dpi=150,

    bbox_inches="tight",
)


plt.close()


print("\nFigure saved to:")

print(output_file)


# ============================================================
# PHASE COMPLETE
# ============================================================

print("\n" + "=" * 60)

print("PHASE 4 COMPLETE")

print("=" * 60)




# Added new 


# ============================================================
# PHASE 4 — VALIDATE CLASSIFIER ACROSS REALIZATIONS
# ============================================================

N_REALIZATIONS = 20

results = []

success_count = 0
failure_count = 0


print("=" * 80)
print("PHASE 4: VALIDATING PERSISTENT ACTIVITY CLASSIFIER")
print("=" * 80)

print("\nFIXED PARAMETERS")
print("-" * 50)

print("N =", N)
print("p =", P)
print("I_ext =", I_EXT)
print("g_syn =", G_SYN)
print("tau_m =", TAU_M)
print("tau_D =", TAU_D)

print("\nClassification rule:")

print(
    f"SUCCESS if activity exists in "
    f"the final window "
    f"[{T_MAX - FINAL_WINDOW}, {T_MAX}]"
)

print(
    "Number of realizations =",
    N_REALIZATIONS,
)


# ============================================================
# RUN DIFFERENT NETWORK REALIZATIONS
# ============================================================

print("\n")
print("=" * 80)
print("RUNNING REALIZATIONS")
print("=" * 80)


for seed in range(N_REALIZATIONS):

    # --------------------------------------------------------
    # 1. Build the local ring
    # --------------------------------------------------------

    local_network = build_ring_network(N)


    # --------------------------------------------------------
    # 2. Add random shortcuts
    # --------------------------------------------------------

    small_world_network, shortcuts = (
        add_random_shortcuts(
            outgoing_connections=local_network,
            p=P,
            seed=seed,
        )
    )


    # --------------------------------------------------------
    # 3. Apply one stimulus and simulate
    # --------------------------------------------------------

    spike_times, spike_neurons = run_simulation(
        outgoing_connections=small_world_network,
        I_ext=I_EXT,
        g_syn=G_SYN,
        tau_m=TAU_M,
        tau_D=TAU_D,
        dt=DT,
        t_max=T_MAX,
        stimulus_neuron=STIMULUS_NEURON,
        stimulus_time=STIMULUS_TIME,
    )


    # --------------------------------------------------------
    # 4. Classify automatically
    # --------------------------------------------------------

    result = classify_persistent_activity(
        spike_times=spike_times,
        stimulus_time=STIMULUS_TIME,
        t_max=T_MAX,
        final_window=FINAL_WINDOW,
    )


    # --------------------------------------------------------
    # 5. Count outcome
    # --------------------------------------------------------

    if result["persistent"]:

        success_count += 1

    else:

        failure_count += 1


    # --------------------------------------------------------
    # 6. Store result
    # --------------------------------------------------------

    results.append({

        "seed": seed,

        "status": result["status"],

        "total_spikes":
            result["total_spikes"],

        "last_spike_time":
            result["last_spike_time"],

        "persistence_duration":
            result["persistence_duration"],

        "spikes_in_final_window":
            result["spikes_in_final_window"],
    })


    # --------------------------------------------------------
    # 7. Print one-line result
    # --------------------------------------------------------

    print(

        f"Seed {seed:2d} | "

        f"{result['status']:7s} | "

        f"Spikes = "
        f"{result['total_spikes']:5d} | "

        f"Last = "
        f"{result['last_spike_time'] if result['last_spike_time'] is not None else 0.0:7.2f}"

        f"Duration = "
        f"{result['persistence_duration']:7.2f} | "

        f"Late spikes = "
        f"{result['spikes_in_final_window']:4d}"
    )


# ============================================================
# SUMMARY
# ============================================================

success_probability = (
    success_count
    / N_REALIZATIONS
)

failure_probability = (
    failure_count
    / N_REALIZATIONS
)


print("\n")
print("=" * 80)
print("PHASE 4 CLASSIFIER SUMMARY")
print("=" * 80)

print(
    "Total realizations:",
    N_REALIZATIONS,
)

print(
    "Successful realizations:",
    success_count,
)

print(
    "Failed realizations:",
    failure_count,
)

print(
    "Estimated success probability:",
    success_probability,
)

print(
    "Estimated failure probability:",
    failure_probability,
)


# ============================================================
# LIST SUCCESS AND FAILURE SEEDS
# ============================================================

success_seeds = [

    result["seed"]

    for result in results

    if result["status"] == "SUCCESS"
]


failure_seeds = [

    result["seed"]

    for result in results

    if result["status"] == "FAILURE"
]


print("\nSUCCESS SEEDS")

print("-" * 50)

print(success_seeds)


print("\nFAILURE SEEDS")

print("-" * 50)

print(failure_seeds)


# ============================================================
# FINAL CHECK
# ============================================================

print("\n")
print("=" * 80)
print("TASK (e) RESULT")
print("=" * 80)


if success_count > 0 and failure_count > 0:

    print(
        "PASSED:"
    )

    print(
        "The classifier automatically distinguishes "
        "successful and failed realizations."
    )

    print(
        "Persistence duration is measured for "
        "every realization."
    )

else:

    print(
        "Only one dynamical outcome was observed "
        "in this small validation sample."
    )

    print(
        "The classifier still works, but more "
        "realizations may be needed for validation."
    )