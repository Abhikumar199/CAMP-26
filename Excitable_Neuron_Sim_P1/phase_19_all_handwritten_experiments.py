

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
    / "phase19_handwritten_experiments"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

TAU_M = 10.0

TAU_D = 2.0

DT = 0.01

RATE_BIN_WIDTH = 1.0

SMOOTH_WINDOW = 5

EXP3_N = 250

EXP3_STIMULUS_TIME = 10.0

EXP3_T_MAX = 2000.0

EXP3_P_VALUES = np.arange(
    0.0,
    1.0001,
    0.05,
)

EXP3_NUM_REALIZATIONS = 100

EXP3_PARAMETER_PAIRS = [

    (0.95, 0.10),

    (0.85, 0.20),

    (0.55, 0.50),

    (0.45, 0.60),

    (0.25, 0.80),

]

CPU_COUNT = os.cpu_count() or 4

MAX_WORKERS = max(
    1,
    CPU_COUNT - 1,
)

def calculate_firing_rate_vs_time(
    spike_times,
    N,
    t_max,
):

    spike_times = np.asarray(
        spike_times,
        dtype=float,
    )

    bin_edges = np.arange(

        0.0,

        t_max + RATE_BIN_WIDTH,

        RATE_BIN_WIDTH,

    )

    spike_counts, _ = np.histogram(

        spike_times,

        bins=bin_edges,

    )

    rate_times = (

        bin_edges[:-1]

        + RATE_BIN_WIDTH / 2.0

    )

    population_rate = (

        spike_counts

        /

        (
            N
            * RATE_BIN_WIDTH
        )

    )

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

        smoothed_rate = population_rate

    return (
        rate_times,
        smoothed_rate,
    )

def run_raster_firing_experiment(

    experiment_name,

    N,

    p,

    stimulus_time,

    I_ext,

    g_syn,

    t_max,

    seed,

):

    print("\n")

    print("=" * 90)

    print(
        experiment_name
    )

    print("=" * 90)

    print(
        "N =",
        N,
    )

    print(
        "p =",
        p,
    )

    print(
        "stimulus time =",
        stimulus_time,
    )

    print(
        "I_ext =",
        I_ext,
    )

    print(
        "g_syn =",
        g_syn,
    )

    print(
        "T_MAX =",
        t_max,
    )

    print(
        "seed =",
        seed,
    )

    local_network = build_ring_network(
        N
    )

    network, shortcuts = add_random_shortcuts(

        outgoing_connections=
            local_network,

        p=p,

        seed=seed,

    )

    print(
        "Number of shortcuts =",
        len(shortcuts),
    )

    print(
        "Running simulation..."
    )

    start_time = time.perf_counter()

    spike_times, spike_neurons = run_simulation(

        outgoing_connections=
            network,

        I_ext=
            I_ext,

        g_syn=
            g_syn,

        tau_m=
            TAU_M,

        tau_D=
            TAU_D,

        dt=
            DT,

        t_max=
            t_max,

        stimulus_neuron=
            N // 2,

        stimulus_time=
            stimulus_time,

    )

    runtime = (

        time.perf_counter()

        - start_time

    )

    spike_times = np.asarray(

        spike_times,

        dtype=float,

    )

    spike_neurons = np.asarray(

        spike_neurons,

        dtype=int,

    )

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

    print(
        "Runtime =",
        f"{runtime:.2f} seconds",
    )

    rate_times, firing_rate = (

        calculate_firing_rate_vs_time(

            spike_times=
                spike_times,

            N=
                N,

            t_max=
                t_max,

        )

    )

    fig, axes = plt.subplots(

        2,

        1,

        figsize=(11, 8),

        sharex=True,

        gridspec_kw={

            "height_ratios": [

                1.0,

                0.8,

            ],

            "hspace": 0.10,

        },

    )

    axes[0].scatter(

        spike_times,

        spike_neurons,

        s=1,

        marker=".",

    )

    axes[0].set_ylabel(
        "Neuron index"
    )

    axes[0].set_ylim(
        0,
        N,
    )

    axes[0].set_title(

        f"{experiment_name}\n"

        f"N={N}, "

        f"p={p}, "

        f"I_ext={I_ext}, "

        f"g_syn={g_syn}, "

        f"stimulus={stimulus_time} ms"

    )

    axes[1].plot(

        rate_times,

        firing_rate,

        linewidth=1.5,

    )

    axes[1].set_xlabel(
        "Time"
    )

    axes[1].set_ylabel(
        "Normalized firing rate"
    )

    axes[1].set_xlim(
        0,
        t_max,
    )

    safe_name = (

        experiment_name

        .lower()

        .replace(" ", "_")

    )

    figure_file = (

        RESULTS_DIR

        / f"{safe_name}.png"

    )

    plt.tight_layout()

    plt.savefig(

        figure_file,

        dpi=300,

        bbox_inches="tight",

    )

    plt.show()

    print(
        "Figure saved to:"
    )

    print(
        figure_file
    )

def calculate_mean_firing_rate(

    spike_times,

    N,

    stimulus_time,

    t_max,

):

    spike_times = np.asarray(

        spike_times,

        dtype=float,

    )

    analysis_spikes = spike_times[

        spike_times

        >= stimulus_time

    ]

    analysis_duration = (

        t_max

        - stimulus_time

    )

    firing_rate = (

        len(
            analysis_spikes
        )

        /

        (
            N

            * analysis_duration
        )

    )

    return float(
        firing_rate
    )

def run_experiment_3_realization(
    task,
):

    (
        pair_index,
        I_ext,
        g_syn,
        p,
        realization,

    ) = task

    seed = (

        pair_index
        * 10_000_000

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
        EXP3_N
    )

    network, shortcuts = add_random_shortcuts(

        outgoing_connections=
            local_network,

        p=
            p,

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
            g_syn,

        tau_m=
            TAU_M,

        tau_D=
            TAU_D,

        dt=
            DT,

        t_max=
            EXP3_T_MAX,

        stimulus_neuron=
            EXP3_N // 2,

        stimulus_time=
            EXP3_STIMULUS_TIME,

    )

    runtime = (

        time.perf_counter()

        - start_time

    )

    firing_rate = calculate_mean_firing_rate(

        spike_times=
            spike_times,

        N=
            EXP3_N,

        stimulus_time=
            EXP3_STIMULUS_TIME,

        t_max=
            EXP3_T_MAX,

    )

    return {

        "pair_index":
            pair_index,

        "N":
            EXP3_N,

        "I_ext":
            I_ext,

        "g_syn":
            g_syn,

        "p":
            p,

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

def run_experiment_3():

    print("\n")

    print("=" * 90)

    print(
        "EXPERIMENT III"
    )

    print("=" * 90)

    print(
        "N =",
        EXP3_N,
    )

    print(
        "p values =",
        EXP3_P_VALUES,
    )

    print(
        "Realizations per p =",
        EXP3_NUM_REALIZATIONS,
    )

    print(
        "Parameter pairs ="
    )

    for pair_index, (
        I_ext,
        g_syn,

    ) in enumerate(
        EXP3_PARAMETER_PAIRS
    ):

        print(

            f"Pair {pair_index + 1}: "

            f"I_ext = {I_ext}, "

            f"g_syn = {g_syn}"

        )

    print(
        "CPU workers =",
        MAX_WORKERS,
    )

    tasks = []

    for pair_index, (

        I_ext,

        g_syn,

    ) in enumerate(
        EXP3_PARAMETER_PAIRS
    ):

        for p in EXP3_P_VALUES:

            for realization in range(

                EXP3_NUM_REALIZATIONS

            ):

                tasks.append(

                    (

                        pair_index,

                        I_ext,

                        g_syn,

                        float(p),

                        realization,

                    )

                )

    print(
        "\nTotal simulations =",
        len(tasks),
    )

    print(
        "\nThis is a large experiment:"
    )

    print(

        f"{len(EXP3_PARAMETER_PAIRS)} parameter pairs"

        f" × {len(EXP3_P_VALUES)} p values"

        f" × {EXP3_NUM_REALIZATIONS} realizations"

    )

    print(
        "=" * 90
    )

    all_results = []

    completed = 0

    start_time = time.perf_counter()

    with ProcessPoolExecutor(

        max_workers=
            MAX_WORKERS

    ) as executor:

        future_to_task = {

            executor.submit(

                run_experiment_3_realization,

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

                    f"\r"

                    f"Completed "

                    f"{completed:5d}/"

                    f"{len(tasks):5d}",

                    end="",

                    flush=True,

                )

            except Exception as error:

                print(
                    "\nERROR"
                )

                print(
                    "Task =",
                    task,
                )

                print(
                    error
                )

    print()

    all_results.sort(

        key=lambda row:

            (

                row["pair_index"],

                row["p"],

                row["realization"],

            )

    )

    all_file = (

        RESULTS_DIR

        / "experiment_3_all_realizations.csv"

    )

    with open(

        all_file,

        "w",

        newline="",

    ) as file:

        fieldnames = [

            "pair_index",

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
        "EXPERIMENT III SUMMARY"
    )

    print("=" * 90)

    for pair_index, (

        I_ext,

        g_syn,

    ) in enumerate(
        EXP3_PARAMETER_PAIRS
    ):

        print("\n")

        print(

            f"I_ext = {I_ext}, "

            f"g_syn = {g_syn}"

        )

        print(
            "-" * 70
        )

        for p in EXP3_P_VALUES:

            p = float(p)

            rows = [

                row

                for row in all_results

                if (

                    row["pair_index"]
                    == pair_index

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

                "pair_index":
                    pair_index,

                "N":
                    EXP3_N,

                "I_ext":
                    I_ext,

                "g_syn":
                    g_syn,

                "p":
                    p,

                "realizations":
                    len(rows),

                "mean_firing_rate":
                    mean_fr,

                "std_firing_rate":
                    std_fr,

            })

            print(

                f"p = {p:4.2f}"

                f" | mean FR = "
                f"{mean_fr:.8f}"

                f" | SD = "
                f"{std_fr:.8f}"

            )

    summary_file = (

        RESULTS_DIR

        / "experiment_3_summary.csv"

    )

    with open(

        summary_file,

        "w",

        newline="",

    ) as file:

        fieldnames = [

            "pair_index",

            "N",

            "I_ext",

            "g_syn",

            "p",

            "realizations",

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

    for pair_index, (

        I_ext,

        g_syn,

    ) in enumerate(
        EXP3_PARAMETER_PAIRS
    ):

        rows = sorted(

            [

                row

                for row in summary_results

                if row["pair_index"]
                == pair_index

            ],

            key=lambda row:
                row["p"],

        )

        p_values = np.asarray(

            [

                row["p"]

                for row in rows

            ],

            dtype=float,

        )

        mean_rates = np.asarray(

            [

                row[
                    "mean_firing_rate"
                ]

                for row in rows

            ],

            dtype=float,

        )

        std_rates = np.asarray(

            [

                row[
                    "std_firing_rate"
                ]

                for row in rows

            ],

            dtype=float,

        )

        plt.plot(

            p_values,

            mean_rates,

            marker=
                markers[pair_index],

            linewidth=
                2.0,

            markersize=
                5,

            label=(

                f"I_ext={I_ext}, "

                f"g_syn={g_syn}"

            ),

        )

        plt.fill_between(

            p_values,

            mean_rates
            - std_rates,

            mean_rates
            + std_rates,

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

        "N = 250, 100 Realizations per p"

    )

    plt.xlim(
        0.0,
        1.0,
    )

    plt.legend()

    plt.grid(
        alpha=0.25
    )

    plt.tight_layout()

    figure_file = (

        RESULTS_DIR

        / "experiment_3_firing_rate_vs_p.png"

    )

    plt.savefig(

        figure_file,

        dpi=300,

        bbox_inches="tight",

    )

    plt.show()

    runtime = (

        time.perf_counter()

        - start_time

    )

    print("\n")

    print("=" * 90)

    print(
        "EXPERIMENT III COMPLETE"
    )

    print("=" * 90)

    print(
        "Runtime =",
        f"{runtime:.2f} seconds",
    )

    print(
        "All realizations:"
    )

    print(
        all_file
    )

    print(
        "Summary:"
    )

    print(
        summary_file
    )

    print(
        "Figure:"
    )

    print(
        figure_file
    )

def main():

    total_start = time.perf_counter()

    print("=" * 90)

    print(
        "PHASE 19: ALL HANDWRITTEN EXPERIMENTS"
    )

    print("=" * 90)

    run_raster_firing_experiment(

        experiment_name=
            "Experiment I",

        N=
            1000,

        p=
            0.10,

        stimulus_time=
            10.0,

        I_ext=
            0.85,

        g_syn=
            0.20,

        t_max=
            2000.0,

        seed=
            3,

    )

    run_raster_firing_experiment(

        experiment_name=
            "Experiment II",

        N=
            1000,

        p=
            0.0,

        stimulus_time=
            10.0,

        I_ext=
            0.85,

        g_syn=
            0.20,

        t_max=
            2000.0,

        seed=
            3,

    )

    run_experiment_3()

    run_raster_firing_experiment(

        experiment_name=
            "Experiment IV",

        N=
            1000,

        p=
            0.10,

        stimulus_time=
            10.0,

        I_ext=
            0.85,

        g_syn=
            -0.20,

        t_max=
            2000.0,

        seed=
            3,

    )

    total_runtime = (

        time.perf_counter()

        - total_start

    )

    print("\n")

    print("=" * 90)

    print(
        "ALL EXPERIMENTS COMPLETE"
    )

    print("=" * 90)

    print(
        "Total runtime =",
        f"{total_runtime:.2f} seconds",
    )

    print(
        "Results directory:"
    )

    print(
        RESULTS_DIR
    )

if __name__ == "__main__":

    main()
