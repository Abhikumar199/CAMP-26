"""
phase_2_local_network.py

Validate traveling-wave propagation on the
regular nearest-neighbor ring at p = 0.
"""

import os
import matplotlib.pyplot as plt

from network import (
    build_ring_network,
    validate_ring_network,
)

from simulator import run_simulation


os.makedirs("figures", exist_ok=True)


# --------------------------------------------
# Parameters
# --------------------------------------------

N = 100

I_EXT = 0.85
G_SYN = 0.20
TAU_M = 10.0
TAU_D = 1.0

DT = 0.01
T_MAX = 70.0

STIMULUS_NEURON = N // 2
STIMULUS_TIME = 10.0


# --------------------------------------------
# Build p = 0 local ring
# --------------------------------------------

network = build_ring_network(N)

validate_ring_network(network)


# --------------------------------------------
# Run simulation
# --------------------------------------------

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


# --------------------------------------------
# Print basic results
# --------------------------------------------

print("\nPHASE 2 RESULTS")
print("-" * 40)

print("Total spikes:", len(spike_times))

print(
    "First spike time:",
    spike_times[0] if len(spike_times) else None
)

print(
    "Last spike time:",
    spike_times[-1] if len(spike_times) else None
)


# --------------------------------------------
# Raster plot
# --------------------------------------------

plt.figure(figsize=(10, 6))

plt.scatter(
    spike_times,
    spike_neurons,
    s=8,
)

plt.xlabel("Time")
plt.ylabel("Neuron index")

plt.title(
    "Phase 2: Traveling Waves on Local Ring (p = 0)"
)

plt.tight_layout()

plt.savefig(
    "figures/phase2_local_wave_raster.png",
    dpi=300,
)

plt.show()
