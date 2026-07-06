import os
import numpy as np
import matplotlib.pyplot as plt

from config import (
    I_EXT,
    G_SYN,
    TAU_M,
    V_THRESHOLD,
    V_RESET,
    DT,
    T_MAX,
)

from neuron import (
    update_voltage,
    apply_synaptic_input,
    check_and_reset,
    analytical_recovery_time,
)


# --------------------------------------------------
# Create output folders
# --------------------------------------------------

os.makedirs("figures", exist_ok=True)
os.makedirs("results", exist_ok=True)


# ==================================================
# CORE SINGLE-NEURON SIMULATOR
# ==================================================

def simulate_neuron(
    I_ext=I_EXT,
    g_syn=G_SYN,
    tau_m=TAU_M,
    input_times=None,
    t_max=T_MAX,
    dt=DT,
):
    """
    Simulate one integrate-and-fire neuron.

    Parameters
    ----------
    I_ext : float
        Constant external current.

    g_syn : float
        Voltage jump caused by one incoming spike.

    tau_m : float
        Membrane time constant.

    input_times : list
        Times at which synaptic inputs arrive.

    t_max : float
        Total simulation duration.

    dt : float
        Numerical time step.
    """

    if input_times is None:
        input_times = []

    times = np.arange(0, t_max + dt, dt)

    voltage = np.zeros(len(times))

    spike_times = []

    V = V_RESET

    for k, t in enumerate(times):

        # ------------------------------------------
        # 1. Passive membrane evolution
        # ------------------------------------------

        V = update_voltage(
            V=V,
            I_ext=I_ext,
            tau_m=tau_m,
            dt=dt,
        )

        # ------------------------------------------
        # 2. Check for incoming synaptic events
        # ------------------------------------------

        for input_time in input_times:

            if abs(t - input_time) < dt / 2:

                V = apply_synaptic_input(
                    V=V,
                    g_syn=g_syn,
                )

        # Store voltage before reset
        voltage[k] = V

        # ------------------------------------------
        # 3. Threshold and reset
        # ------------------------------------------

        V, spiked = check_and_reset(
            V=V,
            threshold=V_THRESHOLD,
            reset=V_RESET,
        )

        if spiked:
            spike_times.append(t)

    return times, voltage, spike_times




# 1. Resting behaviour
# 2. Response to one synaptic input
# 3. Effect of I_ext
# 4. Effect of g_syn
# 5. Effect of tau_m
# 6. Validation of analytical recovery time