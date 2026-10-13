"""
phase_15_paper_raster_firing_rate.py

Replicate Fig. 1 of the paper qualitatively.

TOP:
    Raster plot of ALL neurons
    x-axis = time
    y-axis = neuron index

BOTTOM:
    Normalized instantaneous firing rate
    of the WHOLE NETWORK

Parameters follow the paper figure:
    N = 1000
    I_ext = 0.85
    g_syn = 0.2
    tau_m = 10
    tau_D = 1
    p = 0.1
"""


from pathlib import Path

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
    / "phase15_paper_raster"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

FIGURE_FILE = (
    RESULTS_DIR
    / "paper_style_raster_and_firing_rate.png"
)


# ============================================================
# NETWORK PARAMETERS
# ============================================================

N = 1000

P = 0.10

SEED = 3


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

T_MAX = 400.0

STIMULUS_TIME = 10.0

STIMULUS_NEURON = (
    N // 2
)


# ============================================================
# FIRING-RATE PARAMETERS
# ============================================================

# Width of each time bin.

RATE_BIN_WIDTH = 1.0


# Moving-average window.

SMOOTH_WINDOW = 5


# ============================================================
# BUILD NETWORK
# ============================================================

print("=" * 80)

print(
    "PHASE 15: PAPER FIGURE 1 REPLICATION"
)

print("=" * 80)


print("\nNETWORK")

print("-" * 50)

print("N =", N)

print("p =", P)

print("seed =", SEED)

print("I_ext =", I_EXT)

print("g_syn =", G_SYN)

print("tau_m =", TAU_M)

print("tau_D =", TAU_D)


local_network = build_ring_network(
    N
)


network, shortcuts = add_random_shortcuts(

    outgoing_connections=local_network,

    p=P,

    seed=SEED,

)


print(
    "Number of shortcuts =",
    len(shortcuts),
)


# ============================================================
# RUN SIMULATION
# ============================================================

print("\nRUNNING SIMULATION...")


spike_times, spike_neurons = run_simulation(

    outgoing_connections=network,

    I_ext=I_EXT,

    g_syn=G_SYN,

    tau_m=TAU_M,

    tau_D=TAU_D,

    dt=DT,

    t_max=T_MAX,

    stimulus_neuron=STIMULUS_NEURON,

    stimulus_time=STIMULUS_TIME,

)


# ============================================================
# CONVERT TO NUMPY ARRAYS
# ============================================================

spike_times = np.asarray(
    spike_times,
    dtype=float,
)


spike_neurons = np.asarray(
    spike_neurons,
    dtype=int,
)


# ============================================================
# BASIC RESULTS
# ============================================================

print("\nRESULTS")

print("-" * 50)


print(
    "Total spikes =",
    len(spike_times),
)


if len(spike_times) > 0:

    print(
        "First spike =",
        f"{np.min(spike_times):.2f}",
    )

    print(
        "Last spike =",
        f"{np.max(spike_times):.2f}",
    )


# ============================================================
# CALCULATE WHOLE-NETWORK FIRING RATE
# ============================================================

# ------------------------------------------------------------
# STEP 1:
# CREATE TIME BINS
# ------------------------------------------------------------

rate_bin_edges = np.arange(

    0.0,

    T_MAX + RATE_BIN_WIDTH,

    RATE_BIN_WIDTH,

)


# ------------------------------------------------------------
# STEP 2:
# COUNT SPIKES FROM ALL N NEURONS
# ------------------------------------------------------------

spike_counts, _ = np.histogram(

    spike_times,

    bins=rate_bin_edges,

)


# ------------------------------------------------------------
# STEP 3:
# CALCULATE BIN CENTRES
# ------------------------------------------------------------

rate_times = (

    rate_bin_edges[:-1]

    + RATE_BIN_WIDTH / 2.0

)


# ------------------------------------------------------------
# STEP 4:
# NORMALIZED WHOLE-NETWORK FIRING RATE
# ------------------------------------------------------------

# This uses spikes from ALL N neurons.
#
# Formula:
#
#               spikes in time bin
# r(t) = ----------------------------------
#          N neurons × time-bin width
#
#
# Example:
#
# If:
#
#     N = 1000
#
# and:
#
#     50 spikes occur in a 1-unit bin
#
# then:
#
#     r(t) = 50 / 1000
#
#          = 0.05
#
#
# This gives the same numerical scale
# shown in the paper:
#
# approximately 0.00 to 0.07.


population_rate = (

    spike_counts

    /

    (
        N

        * RATE_BIN_WIDTH
    )

)


# ============================================================
# SMOOTH FIRING RATE
# ============================================================

if SMOOTH_WINDOW > 1:

    kernel = (

        np.ones(
            SMOOTH_WINDOW
        )

        / SMOOTH_WINDOW

    )


    smoothed_rate = np.convolve(

        population_rate,

        kernel,

        mode="same",

    )


else:

    smoothed_rate = (

        population_rate

    )


# ============================================================
# CREATE PAPER-STYLE FIGURE
# ============================================================

fig, axes = plt.subplots(

    2,

    1,

    figsize=(10, 7),

    sharex=True,

    gridspec_kw={

        "height_ratios": [
            1.0,
            0.8,
        ],

        "hspace": 0.08,

    },

)


# ============================================================
# TOP PANEL
#
# RASTER OF THE WHOLE NETWORK
# ============================================================

ax_raster = axes[0]


# Every point represents:
#
# x = time when a spike occurred
#
# y = index of the neuron that fired


ax_raster.scatter(

    spike_times,

    spike_neurons,

    s=1,

    marker=".",

)


ax_raster.set_ylabel(

    "Neuron Index",

    fontsize=13,

)


ax_raster.set_xlim(

    0,

    T_MAX,

)


ax_raster.set_ylim(

    0,

    N,

)


ax_raster.set_yticks(

    [
        0,
        200,
        400,
        600,
        800,
        1000,
    ]

)


ax_raster.tick_params(

    axis="both",

    labelsize=11,

)


# ============================================================
# BOTTOM PANEL
#
# WHOLE-NETWORK FIRING RATE
# ============================================================

ax_rate = axes[1]


ax_rate.plot(

    rate_times,

    smoothed_rate,

    linewidth=1.5,

)


ax_rate.set_xlabel(

    "Time",

    fontsize=13,

)


ax_rate.set_ylabel(

    "Firing Rate",

    fontsize=13,

)


ax_rate.set_xlim(

    0,

    T_MAX,

)


# Same y-axis scale as paper figure.

ax_rate.set_ylim(

    0,

    0.07,

)


ax_rate.set_yticks(

    np.arange(
        0.00,
        0.071,
        0.01,
    )

)


ax_rate.tick_params(

    axis="both",

    labelsize=11,

)


# ============================================================
# X-AXIS TICKS
# ============================================================

ax_rate.set_xticks(

    [
        0,
        100,
        200,
        300,
        400,
    ]

)


# ============================================================
# TITLE
# ============================================================

fig.suptitle(

    (
        "Persistent Activity in a Small-World "
        "Excitable Neuron Network\n"

        f"N = {N}, "
        f"p = {P}, "
        f"seed = {SEED}"
    ),

    fontsize=14,

)


# ============================================================
# FINALIZE FIGURE
# ============================================================

plt.tight_layout(

    rect=[
        0,
        0,
        1,
        0.93,
    ]

)


# ============================================================
# SAVE FIGURE
# ============================================================

plt.savefig(

    FIGURE_FILE,

    dpi=300,

    bbox_inches="tight",

)


print("\nFIGURE SAVED TO:")

print(
    FIGURE_FILE
)


# ============================================================
# SHOW FIGURE
# ============================================================

plt.show()