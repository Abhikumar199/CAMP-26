"""
phase_3_small_world_network.py

PHASE 3
-------

Study how different random shortcut realizations
produce different dynamical outcomes.

For fixed:
    N
    p
    neuron parameters
    initial stimulus

we vary only:
    random seed -> shortcut topology

Outputs:
    1. Terminal summary
    2. CSV of realization-level results
    3. CSV of shortcut-level data
    4. Persistence-duration plot
    5. Total-spikes plot

Scientific question:
    Why do some network realizations sustain activity
    while others fail?
"""

from pathlib import Path
import csv

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from network import (
    build_ring_network,
    validate_ring_network,
    add_random_shortcuts,
    validate_small_world_network,
)

from simulator import run_simulation


# ============================================================
# PATH SETUP
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent

RESULTS_DIR = PROJECT_DIR / "results" / "phase3"
FIGURES_DIR = PROJECT_DIR / "figures" / "phase3"

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

FIGURES_DIR.mkdir(
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
# TEMPORARY PERSISTENCE RULE
# ============================================================

# If activity reaches this final time window,
# temporarily classify it as persistent.
#
# A more rigorous classifier will be Phase 5.

FINAL_WINDOW = 5.0


# ============================================================
# HELPER FUNCTION:
# CIRCULAR SHORTCUT LENGTH
# ============================================================

def circular_distance(source, target, N):
    """
    Shortest distance between two neurons on a ring.

    Example:
        On N = 100,

        distance(5, 10) = 5

        distance(2, 98) = 4
        because the ring wraps around.
    """

    direct_distance = abs(target - source)

    wrapped_distance = N - direct_distance

    return min(
        direct_distance,
        wrapped_distance,
    )


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("PHASE 3: SMALL-WORLD REALIZATION STUDY")
print("=" * 70)

print("\nFIXED PARAMETERS")
print("-" * 50)

print("Network size N:", N)
print("Shortcut density p:", P)

print(
    "Shortcuts per realization:",
    int(round(P * N)),
)

print("Number of realizations:", N_REALIZATIONS)

print("\nNeuron parameters:")

print("I_ext =", I_EXT)
print("g_syn =", G_SYN)
print("tau_m =", TAU_M)
print("tau_D =", TAU_D)

print("\nSimulation parameters:")

print("dt =", DT)
print("t_max =", T_MAX)

print(
    "Stimulus neuron =",
    STIMULUS_NEURON,
)

print(
    "Stimulus time =",
    STIMULUS_TIME,
)


# ============================================================
# VALIDATE ONE NETWORK BEFORE THE FULL EXPERIMENT
# ============================================================

print("\n")
print("=" * 70)
print("NETWORK CONSTRUCTION VALIDATION")
print("=" * 70)

validation_seed = 42


# Build ring

validation_ring = build_ring_network(N)

validate_ring_network(
    validation_ring
)


# Add shortcuts

validation_network, validation_shortcuts = (
    add_random_shortcuts(
        outgoing_connections=validation_ring,
        p=P,
        seed=validation_seed,
    )
)


# Validate

validate_small_world_network(
    local_network=validation_ring,
    small_world_network=validation_network,
    shortcuts=validation_shortcuts,
    p=P,
)


# Print example shortcuts

print("\nEXAMPLE SHORTCUTS FOR SEED 42")
print("-" * 50)

for source, target in validation_shortcuts:

    distance = circular_distance(
        source,
        target,
        N,
    )

    print(
        f"{source:3d} -> {target:3d}"
        f"    ring distance = {distance}"
    )


# ============================================================
# STORAGE
# ============================================================

realization_results = []

shortcut_results = []


# ============================================================
# RUN MULTIPLE RANDOM REALIZATIONS
# ============================================================

print("\n")
print("=" * 70)
print("RUNNING RANDOM NETWORK REALIZATIONS")
print("=" * 70)


for seed in range(N_REALIZATIONS):

    # --------------------------------------------------------
    # 1. Build fresh local ring
    # --------------------------------------------------------

    local_network = build_ring_network(N)


    # --------------------------------------------------------
    # 2. Add new random shortcuts
    # --------------------------------------------------------

    small_world_network, shortcuts = (
        add_random_shortcuts(
            outgoing_connections=local_network,
            p=P,
            seed=seed,
        )
    )


    # --------------------------------------------------------
    # 3. Calculate shortcut statistics
    # --------------------------------------------------------

    shortcut_lengths = []

    for source, target in shortcuts:

        length = circular_distance(
            source,
            target,
            N,
        )

        shortcut_lengths.append(length)

        shortcut_results.append({
            "seed": seed,
            "source": source,
            "target": target,
            "ring_distance": length,
        })


    mean_shortcut_length = (
        sum(shortcut_lengths)
        / len(shortcut_lengths)
    )

    max_shortcut_length = max(
        shortcut_lengths
    )


    # --------------------------------------------------------
    # 4. Run neuronal dynamics
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
    # 5. Extract dynamical results
    # --------------------------------------------------------

    total_spikes = len(spike_times)


    if total_spikes > 0:

        first_spike_time = float(
            spike_times[0]
        )

        last_spike_time = float(
            spike_times[-1]
        )

    else:

        first_spike_time = 0.0
        last_spike_time = 0.0


    # --------------------------------------------------------
    # 6. Temporary persistence classification
    # --------------------------------------------------------

    persisted = (
        last_spike_time
        >= T_MAX - FINAL_WINDOW
    )


    if persisted:

        status = "PERSISTENT"

    else:

        status = "FAILED"


    # --------------------------------------------------------
    # 7. Store realization result
    # --------------------------------------------------------

    realization_results.append({

        "seed": seed,

        "N": N,

        "p": P,

        "n_shortcuts": len(shortcuts),

        "total_spikes": total_spikes,

        "first_spike_time": first_spike_time,

        "last_spike_time": last_spike_time,

        "persistence_duration":
            last_spike_time - STIMULUS_TIME,

        "mean_shortcut_length":
            mean_shortcut_length,

        "max_shortcut_length":
            max_shortcut_length,

        "status": status,
    })


    # --------------------------------------------------------
    # 8. Print result
    # --------------------------------------------------------

    print(

        f"Seed {seed:3d} | "

        f"Spikes = {total_spikes:6d} | "

        f"Last = {last_spike_time:7.2f} | "

        f"Mean L = {mean_shortcut_length:6.2f} | "

        f"{status}"
    )


# ============================================================
# SUMMARY STATISTICS
# ============================================================

persistent_results = [

    result

    for result in realization_results

    if result["status"] == "PERSISTENT"
]


failed_results = [

    result

    for result in realization_results

    if result["status"] == "FAILED"
]


n_persistent = len(
    persistent_results
)

n_failed = len(
    failed_results
)


probability_persistent = (
    n_persistent
    / N_REALIZATIONS
)


probability_failure = (
    n_failed
    / N_REALIZATIONS
)


# ============================================================
# PRINT SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("PHASE 3 SUMMARY")
print("=" * 70)

print(
    "Total realizations:",
    N_REALIZATIONS
)

print(
    "Persistent:",
    n_persistent
)

print(
    "Failed:",
    n_failed
)

print(
    "Estimated probability of persistence:",
    round(probability_persistent, 3)
)

print(
    "Estimated probability of failure:",
    round(probability_failure, 3)
)


# ============================================================
# PRINT INTERESTING SEEDS
# ============================================================

print("\nINTERESTING SEEDS")
print("-" * 50)


if persistent_results:

    first_persistent_seed = (
        persistent_results[0]["seed"]
    )

    print(
        "First persistent seed:",
        first_persistent_seed
    )

else:

    print(
        "No persistent seed found."
    )


if failed_results:

    shortest_failure = min(
        failed_results,
        key=lambda x: x["last_spike_time"],
    )

    longest_failure = max(
        failed_results,
        key=lambda x: x["last_spike_time"],
    )

    print(
        "Fastest failure seed:",
        shortest_failure["seed"],
        "| last spike =",
        shortest_failure["last_spike_time"],
    )

    print(
        "Longest failed transient seed:",
        longest_failure["seed"],
        "| last spike =",
        longest_failure["last_spike_time"],
    )


# ============================================================
# SAVE REALIZATION-LEVEL CSV
# ============================================================

realization_file = (
    RESULTS_DIR
    / "phase3_realization_results.csv"
)


fieldnames = [

    "seed",

    "N",

    "p",

    "n_shortcuts",

    "total_spikes",

    "first_spike_time",

    "last_spike_time",

    "persistence_duration",

    "mean_shortcut_length",

    "max_shortcut_length",

    "status",
]


with open(
    realization_file,
    "w",
    newline="",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames,
    )

    writer.writeheader()

    writer.writerows(
        realization_results
    )


print("\nRealization results saved to:")

print(realization_file)


# ============================================================
# SAVE SHORTCUT-LEVEL CSV
# ============================================================

shortcut_file = (
    RESULTS_DIR
    / "phase3_shortcuts.csv"
)


with open(
    shortcut_file,
    "w",
    newline="",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "seed",
            "source",
            "target",
            "ring_distance",
        ],
    )

    writer.writeheader()

    writer.writerows(
        shortcut_results
    )


print("\nShortcut data saved to:")

print(shortcut_file)


# ============================================================
# FIGURE 1:
# PERSISTENCE DURATION BY SEED
# ============================================================

seeds = [

    result["seed"]

    for result in realization_results
]


durations = [

    result["persistence_duration"]

    for result in realization_results
]


plt.figure(
    figsize=(12, 6)
)


plt.bar(
    seeds,
    durations,
)


plt.axhline(
    T_MAX - STIMULUS_TIME,
    linestyle="--",
    label="Simulation limit",
)


plt.xlabel(
    "Random network seed"
)

plt.ylabel(
    "Activity duration"
)

plt.title(
    "Phase 3: Activity Duration Across "
    "Random Small-World Realizations"
)

plt.legend()


duration_figure = (
    FIGURES_DIR
    / "phase3_duration_by_seed.png"
)


plt.savefig(
    duration_figure,
    dpi=150,
)

plt.close()


print("\nDuration figure saved to:")

print(duration_figure)


# ============================================================
# FIGURE 2:
# TOTAL SPIKES BY SEED
# ============================================================

total_spike_values = [

    result["total_spikes"]

    for result in realization_results
]


plt.figure(
    figsize=(12, 6)
)


plt.bar(
    seeds,
    total_spike_values,
)


plt.xlabel(
    "Random network seed"
)

plt.ylabel(
    "Total number of spikes"
)

plt.title(
    "Phase 3: Total Network Activity "
    "Across Random Realizations"
)


spike_figure = (
    FIGURES_DIR
    / "phase3_total_spikes_by_seed.png"
)


plt.savefig(
    spike_figure,
    dpi=150,
)

plt.close()


print("\nSpike-count figure saved to:")

print(spike_figure)


# ============================================================
# FIGURE 3:
# SHORTCUT LENGTH VS ACTIVITY DURATION
# ============================================================

mean_lengths = [

    result["mean_shortcut_length"]

    for result in realization_results
]


plt.figure(
    figsize=(8, 6)
)


plt.scatter(
    mean_lengths,
    durations,
    s=60,
)


plt.xlabel(
    "Mean shortcut length"
)

plt.ylabel(
    "Activity duration"
)

plt.title(
    "Phase 3: Shortcut Length vs Activity Duration"
)


relationship_figure = (
    FIGURES_DIR
    / "phase3_shortcut_length_vs_duration.png"
)


plt.savefig(
    relationship_figure,
    dpi=150,
)

plt.close()


print("\nRelationship figure saved to:")

print(relationship_figure)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n")
print("=" * 70)
print("PHASE 3 COMPLETED")
print("=" * 70)

print(
    "Next scientific question:"
)

print(
    "Which topological properties distinguish "
    "persistent networks from failed networks?"
)