

from pathlib import Path
import csv
import time
import os

from concurrent.futures import (
    ProcessPoolExecutor,
    as_completed,
)

import numpy as np
import matplotlib.pyplot as plt

from network import (
    build_ring_network,
    add_random_shortcuts,
)

from simulator import run_simulation

PROJECT_DIR = Path(__file__).resolve().parent

RESULTS_DIR = (
    PROJECT_DIR
    / "results"
    / "phase21_firing_rate_vs_p_multi_Iext"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

ALL_FILE = (
    RESULTS_DIR
    / "all_realizations.csv"
)

SUMMARY_FILE = (
    RESULTS_DIR
    / "firing_rate_vs_p_summary.csv"
)

FIGURE_FILE = (
    RESULTS_DIR
    / "firing_rate_vs_p_multi_Iext.png"
)

N = 250

G_SYN = 0.4

I_EXT_VALUES = [

    0.50,

    0.75,

    1.00,

    1.25,

    1.50,

]

P_VALUES = np.arange(

    0.0,

    1.0001,

    0.2,

)

NUM_REALIZATIONS = 3

TAU_M = 10.0

TAU_D = 1.0

DT = 0.01

T_MAX = 2000.0

STIMULUS_TIME = 10.0

STIMULUS_NEURON = N // 2

CPU_COUNT = os.cpu_count() or 4

MAX_WORKERS = max(

    1,

    CPU_COUNT - 1,

)

def calculate_mean_firing_rate(
    spike_times,
):

    spike_times = np.asarray(

        spike_times,

        dtype=float,

    )

    post_stimulus_spikes = spike_times[

        spike_times

        >= STIMULUS_TIME

    ]

    observation_duration = (

        T_MAX

        - STIMULUS_TIME

    )

    firing_rate = (

        len(
            post_stimulus_spikes
        )

        /

        (
            N

            * observation_duration

        )

    )

    return float(
        firing_rate
    )

def run_one_realization(
    task,
):

    (
        current_index,
        I_ext,
        p,
        realization,

    ) = task

    seed = (

        current_index
        * 1_000_000

        +

        int(
            round(
                p * 100
            )
        )
        * 1000

        +

        realization

    )

    local_network = build_ring_network(
        N
    )

    network, shortcuts = add_random_shortcuts(

        outgoing_connections=
            local_network,

        p=
            float(p),

        seed=
            seed,

    )

    start_time = time.perf_counter()

    spike_times, spike_neurons = run_simulation(

        outgoing_connections=
            network,

        I_ext=
            I_ext,

        g_syn=
            G_SYN,

        tau_m=
            TAU_M,

        tau_D=
            TAU_D,

        dt=
            DT,

        t_max=
            T_MAX,

        stimulus_neuron=
            STIMULUS_NEURON,

        stimulus_time=
            STIMULUS_TIME,

    )

    runtime = (

        time.perf_counter()

        - start_time

    )

    firing_rate = calculate_mean_firing_rate(

        spike_times

    )

    return {

        "current_index":
            current_index,

        "N":
            N,

        "I_ext":
            I_ext,

        "g_syn":
            G_SYN,

        "p":
            float(p),

        "realization":
            realization,

        "seed":
            seed,

        "number_of_shortcuts":
            len(shortcuts),

        "total_spikes":
            len(spike_times),

        "mean_firing_rate":
            firing_rate,

        "runtime_seconds":
            runtime,

    }

def main():

    print("=" * 90)

    print(
        "PHASE 21: FIRING RATE VS p FOR DIFFERENT I_ext"
    )

    print("=" * 90)

    print(
        "\nN =",
        N,
    )

    print(
        "g_syn =",
        G_SYN,
    )

    print(
        "Stimulus time =",
        STIMULUS_TIME,
    )

    print(
        "I_ext values =",
        I_EXT_VALUES,
    )

    print(
        "p values =",
        P_VALUES,
    )

    print(
        "Realizations per condition =",
        NUM_REALIZATIONS,
    )

    print(
        "CPU workers =",
        MAX_WORKERS,
    )

    tasks = []

    for current_index, I_ext in enumerate(

        I_EXT_VALUES

    ):

        for p in P_VALUES:

            for realization in range(

                NUM_REALIZATIONS

            ):

                tasks.append(

                    (

                        current_index,

                        I_ext,

                        float(p),

                        realization,

                    )

                )

    print(
        "\nTotal simulations =",
        len(tasks),
    )

    all_results = []

    completed = 0

    total_start = time.perf_counter()

    print("\nRUNNING SIMULATIONS")

    print("-" * 90)

    with ProcessPoolExecutor(

        max_workers=
            MAX_WORKERS

    ) as executor:

        future_to_task = {

            executor.submit(

                run_one_realization,

                task,

            ):

            task

            for task in tasks

        }

        for future in as_completed(

            future_to_task

        ):

            task = future_to_task[
                future
            ]

            try:

                result = future.result()

                all_results.append(
                    result
                )

                completed += 1

                print(

                    f"[{completed:3d}/"

                    f"{len(tasks):3d}]"

                    f"  I_ext="

                    f"{result['I_ext']:.2f}"

                    f"  p="

                    f"{result['p']:.1f}"

                    f"  realization="

                    f"{result['realization']}"

                    f"  shortcuts="

                    f"{result['number_of_shortcuts']:3d}"

                    f"  FR="

                    f"{result['mean_firing_rate']:.8f}"

                )

            except Exception as error:

                print(
                    "\nERROR:"
                )

                print(
                    "Task =",
                    task,
                )

                print(
                    error
                )

    all_results.sort(

        key=lambda row:

            (

                row["current_index"],

                row["p"],

                row["realization"],

            )

    )

    with open(

        ALL_FILE,

        "w",

        newline="",

    ) as file:

        fieldnames = [

            "current_index",

            "N",

            "I_ext",

            "g_syn",

            "p",

            "realization",

            "seed",

            "number_of_shortcuts",

            "total_spikes",

            "mean_firing_rate",

            "runtime_seconds",

        ]

        writer = csv.DictWriter(

            file,

            fieldnames=
                fieldnames,

        )

        writer.writeheader()

        writer.writerows(
            all_results
        )

    summary_results = []

    print("\n")

    print("=" * 90)

    print(
        "SUMMARY"
    )

    print("=" * 90)

    for current_index, I_ext in enumerate(

        I_EXT_VALUES

    ):

        print("\n")

        print(

            f"I_ext = {I_ext:.2f}"

        )

        print(
            "-" * 70
        )

        for p in P_VALUES:

            p = float(p)

            rows = [

                row

                for row in all_results

                if (

                    row["current_index"]
                    == current_index

                    and

                    np.isclose(

                        row["p"],

                        p,

                    )

                )

            ]

            firing_rates = np.asarray(

                [

                    row[
                        "mean_firing_rate"
                    ]

                    for row in rows

                ],

                dtype=float,

            )

            mean_fr = float(

                np.mean(
                    firing_rates
                )

            )

            std_fr = float(

                np.std(

                    firing_rates,

                    ddof=1,

                )

            ) if len(
                firing_rates
            ) > 1 else 0.0

            summary_results.append({

                "current_index":
                    current_index,

                "N":
                    N,

                "I_ext":
                    I_ext,

                "g_syn":
                    G_SYN,

                "p":
                    p,

                "number_of_realizations":
                    len(rows),

                "mean_firing_rate":
                    mean_fr,

                "std_firing_rate":
                    std_fr,

            })

            print(

                f"p = {p:.1f}"

                f" | mean FR = "

                f"{mean_fr:.8f}"

                f" | SD = "

                f"{std_fr:.8f}"

            )

    with open(

        SUMMARY_FILE,

        "w",

        newline="",

    ) as file:

        fieldnames = [

            "current_index",

            "N",

            "I_ext",

            "g_syn",

            "p",

            "number_of_realizations",

            "mean_firing_rate",

            "std_firing_rate",

        ]

        writer = csv.DictWriter(

            file,

            fieldnames=
                fieldnames,

        )

        writer.writeheader()

        writer.writerows(
            summary_results
        )

    plt.figure(
        figsize=(10, 7)
    )

    markers = [

        "o",

        "s",

        "^",

        "D",

        "v",

    ]

    for current_index, I_ext in enumerate(

        I_EXT_VALUES

    ):

        rows = sorted(

            [

                row

                for row in summary_results

                if row["current_index"]
                == current_index

            ],

            key=lambda row:
                row["p"],

        )

        p_plot = np.asarray(

            [

                row["p"]

                for row in rows

            ],

            dtype=float,

        )

        mean_fr_plot = np.asarray(

            [

                row[
                    "mean_firing_rate"
                ]

                for row in rows

            ],

            dtype=float,

        )

        std_fr_plot = np.asarray(

            [

                row[
                    "std_firing_rate"
                ]

                for row in rows

            ],

            dtype=float,

        )

        plt.plot(

            p_plot,

            mean_fr_plot,

            marker=
                markers[current_index],

            linewidth=
                2.0,

            markersize=
                6,

            label=(

                f"$I_{{ext}}$ = "

                f"{I_ext:.2f}"

            ),

        )

        plt.fill_between(

            p_plot,

            mean_fr_plot
            - std_fr_plot,

            mean_fr_plot
            + std_fr_plot,

            alpha=0.10,

        )

    plt.xlabel(
        "Shortcut density, p"
    )

    plt.ylabel(
        "Mean whole-network firing rate"
    )

    plt.title(

        "Firing Rate vs Shortcut Density\n"

        "$N=250$, "

        "$g_{syn}=0.4$, "

        "3 Realizations per Condition"

    )

    plt.xlim(
        0.0,
        1.0,
    )

    plt.xticks(
        P_VALUES
    )

    plt.legend(
        title="External current"
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

    total_runtime = (

        time.perf_counter()

        - total_start

    )

    print("\n")

    print("=" * 90)

    print(
        "EXPERIMENT COMPLETE"
    )

    print("=" * 90)

    print(
        "Total simulations =",
        len(all_results),
    )

    print(
        "Total runtime =",
        f"{total_runtime:.2f} seconds",
    )

    print(
        "\nAll realizations:"
    )

    print(
        ALL_FILE
    )

    print(
        "\nSummary:"
    )

    print(
        SUMMARY_FILE
    )

    print(
        "\nFigure:"
    )

    print(
        FIGURE_FILE
    )

if __name__ == "__main__":

    main()
