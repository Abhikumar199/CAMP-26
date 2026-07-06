import numpy as np


def update_voltage(V, I_ext, tau_m, dt):
    """
    Evolve the membrane voltage for one time step.

    Between synaptic events:

        tau_m * dV/dt = -V + I_ext

    Euler approximation:

        V(t + dt) = V(t)
                    + dt/tau_m * (-V(t) + I_ext)
    """

    dV = (-V + I_ext) / tau_m

    V_new = V + dt * dV

    return V_new


def apply_synaptic_input(V, g_syn, n_inputs=1):
    """
    Apply one or more instantaneous synaptic pulses.

    Each incoming spike increases voltage by g_syn.
    """

    return V + n_inputs * g_syn


def check_and_reset(V, threshold=1.0, reset=0.0):
    """
    Check whether the neuron has crossed threshold.

    Returns
    -------
    V : float
        Reset voltage if spike occurred.

    spiked : bool
        True if neuron fired.
    """

    if V >= threshold:
        return reset, True

    return V, False


def analytical_recovery_time(
    I_ext,
    g_syn,
    tau_m,
    n_inputs=1
):
    """
    Equation (2) from Roxin et al. (2004).

    Minimum recovery time after a previous spike such
    that n synaptic inputs can make the neuron fire again.

    T_R^(n) = tau_m * ln(
        I_ext /
        (I_ext + n*g_syn - 1)
    )
    """

    denominator = I_ext + n_inputs * g_syn - 1.0

    if denominator <= 0:
        return np.inf

    return tau_m * np.log(
        I_ext / denominator
    )