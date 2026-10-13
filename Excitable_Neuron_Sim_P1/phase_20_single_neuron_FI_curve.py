

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from phase_1_neuron_characterization import (
    simulate_neuron,
)

PROJECT_DIR = Path(__file__).resolve().parent

RESULTS_DIR = (
    PROJECT_DIR
    / "results"
    / "phase20_single_neuron_FI"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

FIGURE_FILE = (
    RESULTS_DIR
    / "single_neuron_FI_curve.png"
)

I_VALUES = np.linspace(
    0.0,
    2.0,
    101,
)

def main():

    print("=" * 80)

    print(
        "PHASE 20: SINGLE-NEURON F-I CURVE"
    )

    print("=" * 80)

    firing_rates = []

    for I_ext in I_VALUES:

        times, voltage, spike_times = simulate_neuron(

            I_ext=
                float(I_ext),

            input_times=
                [],

        )

        duration = (

            times[-1]

            - times[0]

        )

        firing_rate = (

            len(spike_times)

            / duration

        )

        firing_rates.append(
            firing_rate
        )

        print(

            f"I_ext = {I_ext:.3f}"

            f" | spikes = {len(spike_times):4d}"

            f" | firing rate = "
            f"{firing_rate:.6f}"

        )

    firing_rates = np.asarray(

        firing_rates,

        dtype=float,

    )

    plt.figure(
        figsize=(8, 6)
    )

    plt.plot(

        I_VALUES,

        firing_rates,

        linewidth=2.0,

    )

    plt.xlabel(
        "External current, $I_{ext}$"
    )

    plt.ylabel(
        "Firing rate"
    )

    plt.title(
        "Single-Neuron F-I Curve"
    )

    plt.xlim(
        I_VALUES[0],
        I_VALUES[-1],
    )

    plt.grid(
        alpha=0.25
    )

    plt.tight_layout()

    plt.savefig(

        FIGURE_FILE,

        dpi=300,

        bbox_inches="tight",

    )

    plt.show()

    print("\n")

    print(
        "Figure saved to:"
    )

    print(
        FIGURE_FILE
    )

if __name__ == "__main__":

    main()
