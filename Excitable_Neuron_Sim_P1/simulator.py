"""
simulator.py

Event-driven network simulator for the
Roxin, Riecke & Solla (2004) model.
"""

import numpy as np


def run_simulation(
    outgoing_connections,
    I_ext=0.85,
    g_syn=0.20,
    tau_m=10.0,
    tau_D=1.0,
    dt=0.01,
    t_max=100.0,
    stimulus_neuron=None,
    stimulus_time=10.0,
):
    """
    Simulate a network of integrate-and-fire neurons.

    Returns
    -------
    spike_times : numpy array
    spike_neurons : numpy array
    """

    N = len(outgoing_connections)

    # --------------------------------------------
    # Time setup
    # --------------------------------------------

    n_steps = int(round(t_max / dt)) + 1

    delay_steps = int(round(tau_D / dt))

    stimulus_step = int(round(stimulus_time / dt))

    # --------------------------------------------
    # State of all neurons
    # --------------------------------------------

    # Start all neurons at their resting fixed point
    V = np.full(N, I_ext, dtype=float)

    # event_buffer[k, i] =
    # number of synaptic inputs arriving at
    # neuron i at time step k

    event_buffer = np.zeros(
        (n_steps + delay_steps + 1, N),
        dtype=np.int16,
    )

    spike_times = []
    spike_neurons = []

    # Exact passive update:
    #
    # V(t + dt) =
    # I_ext + (V(t) - I_ext) exp(-dt/tau_m)

    decay = np.exp(-dt / tau_m)

    # --------------------------------------------
    # Simulation loop
    # --------------------------------------------

    for step in range(n_steps):

        current_time = step * dt

        # 1. Passive membrane evolution

        V = I_ext + (V - I_ext) * decay

        # 2. Apply all delayed synaptic inputs

        arriving_inputs = event_buffer[step]

        V += g_syn * arriving_inputs

        # 3. Initial localized stimulus

        if (
            stimulus_neuron is not None
            and step == stimulus_step
        ):
            # Force one neuron to threshold.
            # This represents the localized
            # transient stimulus in the paper.

            V[stimulus_neuron] = 1.0

        # 4. Find neurons that crossed threshold

        firing_neurons = np.flatnonzero(V >= 1.0)

        # 5. Record spikes

        for neuron in firing_neurons:

            spike_times.append(current_time)
            spike_neurons.append(neuron)

        # 6. Reset fired neurons

        V[firing_neurons] = 0.0

        # 7. Schedule delayed outgoing spikes

        arrival_step = step + delay_steps

        if arrival_step < len(event_buffer):

            for source in firing_neurons:

                for target in outgoing_connections[source]:

                    event_buffer[
                        arrival_step,
                        target
                    ] += 1

    return (
        np.asarray(spike_times),
        np.asarray(spike_neurons),
    )