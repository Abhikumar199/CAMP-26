from pathlib import Path
import csv
import time
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
import matplotlib.pyplot as plt

from network import build_ring_network, add_random_shortcuts
from simulator import run_simulation


# ============================================================
# PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_DIR / "results" / "phase13_multiN"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

ALL_FILE = RESULTS_DIR / "all_realizations.csv"
CURVE_FILE = RESULTS_DIR / "multiN_probability_curves.csv"
PCR_FILE = RESULTS_DIR / "critical_points.csv"
FIGURE_FILE = RESULTS_DIR / "paper_style_multiN_inset.png"


# ============================================================
# EXPERIMENT PARAMETERS
# ============================================================

N_VALUES = [250, 500, 1000, 2000]

I_EXT = 0.85
G_SYN = 0.20
TAU_M = 10.0
TAU_D = 1.0

DT = 0.01
T_MAX = 3000.0

STIMULUS_TIME = 10.0

FINAL_WINDOW_START = 2800.0
FINAL_WINDOW_END = 3000.0

NUM_REALIZATIONS = 100


# ============================================================
# CPU SETTINGS
# ============================================================

CPU_COUNT = os.cpu_count() or 4

# Use almost all logical CPU cores.
# Leave one core free so Windows remains responsive.
MAX_WORKERS = max(1, CPU_COUNT - 1)


# ============================================================
# P VALUES
# ============================================================

P_VALUES = np.array([
    0.00,
    0.05,
    0.075,
    0.10,
    0.125,
    0.15,
    0.175,
    0.20,
    0.225,
    0.25,
    0.275,
    0.30,
    0.325,
    0.35,
    0.40,
])


# ============================================================
# CLASSIFY ONE REALIZATION
# ============================================================

def classify_realization(spike_times):

    spike_times = np.asarray(spike_times, dtype=float)

    if len(spike_times) == 0:

        return (
            "FAILURE",
            0,
            np.nan,
            0,
        )

    last_spike = float(np.max(spike_times))

    late_spikes = int(
        np.sum(
            (spike_times >= FINAL_WINDOW_START)
            &
            (spike_times <= FINAL_WINDOW_END)
        )
    )

    status = (
        "SUCCESS"
        if late_spikes > 0
        else "FAILURE"
    )

    return (
        status,
        len(spike_times),
        last_spike,
        late_spikes,
    )


# ============================================================
# WORKER FUNCTION
#
# Each CPU process runs ONE independent realization.
#
# IMPORTANT:
# This function must stay outside main().
# Windows multiprocessing needs top-level functions.
# ============================================================

def run_one_realization(task):

    N, p, seed = task

    # Build local ring network inside worker process.
    #
    # This avoids sharing mutable network objects
    # between CPU processes.
    local_network = build_ring_network(N)

    stimulus_neuron = N // 2


    # --------------------------------------------------------
    # Add random shortcuts
    # --------------------------------------------------------

    network, shortcuts = add_random_shortcuts(
        outgoing_connections=local_network,
        p=p,
        seed=seed,
    )


    # --------------------------------------------------------
    # Run simulation
    # --------------------------------------------------------

    run_start = time.perf_counter()

    spike_times, spike_neurons = run_simulation(
        outgoing_connections=network,
        I_ext=I_EXT,
        g_syn=G_SYN,
        tau_m=TAU_M,
        tau_D=TAU_D,
        dt=DT,
        t_max=T_MAX,
        stimulus_neuron=stimulus_neuron,
        stimulus_time=STIMULUS_TIME,
    )

    runtime = time.perf_counter() - run_start


    # --------------------------------------------------------
    # Classify result
    # --------------------------------------------------------

    (
        status,
        total_spikes,
        last_spike,
        late_spikes,
    ) = classify_realization(spike_times)


    # --------------------------------------------------------
    # Return result to main process
    # --------------------------------------------------------

    return {
        "N": N,
        "p": p,
        "seed": seed,
        "number_of_shortcuts": len(shortcuts),
        "status": status,
        "total_spikes": total_spikes,
        "last_spike_time": last_spike,
        "late_spikes": late_spikes,
        "runtime_seconds": runtime,
    }


# ============================================================
# ESTIMATE CRITICAL p
# ============================================================

def estimate_p_cr(rows):

    # Exclude p=0 because the pure-ring case
    # is treated separately.

    rows = sorted(
        [
            r
            for r in rows
            if r["p"] > 0
        ],
        key=lambda r: r["p"],
    )


    # Search for crossing of probability = 0.5

    for a, b in zip(
        rows[:-1],
        rows[1:],
    ):

        y1 = a["probability_failure"]
        y2 = b["probability_failure"]

        if y1 <= 0.5 <= y2:

            p1 = a["p"]
            p2 = b["p"]

            if np.isclose(y1, y2):

                return 0.5 * (p1 + p2)

            return (
                p1
                +
                (0.5 - y1)
                *
                (p2 - p1)
                /
                (y2 - y1)
            )


    # Fallback:
    # choose point closest to 50% failure.

    return min(
        rows,
        key=lambda r:
            abs(
                r["probability_failure"]
                - 0.5
            ),
    )["p"]


# ============================================================
# SAVE CSV FILES
# ============================================================

def save_results(
    all_rows,
    curve_rows,
    critical_rows,
):

    # --------------------------------------------------------
    # All individual realizations
    # --------------------------------------------------------

    with open(
        ALL_FILE,
        "w",
        newline="",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=list(
                all_rows[0].keys()
            ),
        )

        writer.writeheader()
        writer.writerows(all_rows)


    # --------------------------------------------------------
    # Probability curves
    # --------------------------------------------------------

    with open(
        CURVE_FILE,
        "w",
        newline="",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=list(
                curve_rows[0].keys()
            ),
        )

        writer.writeheader()
        writer.writerows(curve_rows)


    # --------------------------------------------------------
    # Critical points
    # --------------------------------------------------------

    with open(
        PCR_FILE,
        "w",
        newline="",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "N",
                "p_critical",
            ],
        )

        writer.writeheader()
        writer.writerows(
            critical_rows
        )


# ============================================================
# PLOT PAPER-STYLE MULTI-N CURVES
# ============================================================

def make_plot(curve_rows):

    plt.figure(
        figsize=(8, 6)
    )

    markers = {
        250: "^",
        500: "D",
        1000: "s",
        2000: "o",
    }


    for N in N_VALUES:

        # Exclude p=0 from connected curve.

        rows = sorted(
            [
                r
                for r in curve_rows
                if (
                    r["N"] == N
                    and
                    r["p"] > 0
                )
            ],
            key=lambda r: r["p"],
        )


        x = np.array([
            r["p"]
            for r in rows
        ])

        y = np.array([
            r["percent_failure"]
            for r in rows
        ])


        plt.plot(
            x,
            y,
            marker=markers[N],
            linewidth=1.8,
            markersize=6,
            label=f"N={N}",
        )


    plt.xlabel("p")
    plt.ylabel("% Failure")

    plt.xlim(0.0, 0.42)
    plt.ylim(-2, 102)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        FIGURE_FILE,
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def main():

    all_rows = []
    curve_rows = []
    critical_rows = []

    total_start = time.perf_counter()


    print("=" * 80)
    print(
        "MULTI-N FAILURE PROBABILITY EXPERIMENT"
    )
    print("=" * 80)

    print(
        f"Logical CPU cores available : {CPU_COUNT}"
    )

    print(
        f"Parallel workers used        : {MAX_WORKERS}"
    )

    print(
        f"N values                     : {N_VALUES}"
    )

    print(
        f"Realizations per (N, p)      : "
        f"{NUM_REALIZATIONS}"
    )

    print(
        f"p values                     : "
        f"{P_VALUES}"
    )


    # ========================================================
    # LOOP OVER NETWORK SIZES
    # ========================================================

    for N in N_VALUES:

        print("\n" + "=" * 80)

        print(
            f"RUNNING N = {N}"
        )

        print("=" * 80)


        rows_for_N = []


        # ====================================================
        # LOOP OVER p VALUES
        # ====================================================

        for p_index, p in enumerate(
            P_VALUES,
            start=1,
        ):

            p = float(p)

            success_count = 0
            failure_count = 0

            p_start = time.perf_counter()


            print(
                f"\nN={N} | "
                f"p={p:.3f} | "
                f"shortcuts={int(round(p*N))} | "
                f"{p_index}/{len(P_VALUES)}"
            )


            # ================================================
            # CREATE 100 INDEPENDENT TASKS
            # ================================================

            tasks = [
                (
                    N,
                    p,
                    seed,
                )
                for seed
                in range(NUM_REALIZATIONS)
            ]


            # ================================================
            # RUN TASKS ON ALL CPU CORES
            # ================================================

            completed = 0


            with ProcessPoolExecutor(
                max_workers=MAX_WORKERS
            ) as executor:


                futures = [

                    executor.submit(
                        run_one_realization,
                        task,
                    )

                    for task in tasks

                ]


                # ============================================
                # COLLECT RESULTS AS THEY FINISH
                # ============================================

                for future in as_completed(
                    futures
                ):

                    result = future.result()

                    all_rows.append(result)


                    if (
                        result["status"]
                        == "SUCCESS"
                    ):

                        success_count += 1

                    else:

                        failure_count += 1


                    completed += 1


                    print(
                        f"\rCompleted "
                        f"{completed:3d}/"
                        f"{NUM_REALIZATIONS:3d}"
                        f" | "
                        f"Success="
                        f"{success_count:3d}"
                        f" | "
                        f"Failure="
                        f"{failure_count:3d}",
                        end="",
                        flush=True,
                    )


            print()


            # ================================================
            # FAILURE PROBABILITY
            # ================================================

            pf = (
                failure_count
                /
                NUM_REALIZATIONS
            )


            se = np.sqrt(
                pf
                *
                (1.0 - pf)
                /
                NUM_REALIZATIONS
            )


            row = {

                "N":
                    N,

                "p":
                    p,

                "number_of_shortcuts":
                    int(round(p * N)),

                "realizations":
                    NUM_REALIZATIONS,

                "success_count":
                    success_count,

                "failure_count":
                    failure_count,

                "probability_failure":
                    pf,

                "percent_failure":
                    100.0 * pf,

                "percent_standard_error":
                    100.0 * se,

                "runtime_seconds":
                    time.perf_counter()
                    -
                    p_start,
            }


            curve_rows.append(row)
            rows_for_N.append(row)


            print(
                f"% Failure = "
                f"{100 * pf:.1f}"
            )

            print(
                f"Time for this p = "
                f"{row['runtime_seconds']:.2f} s"
            )


        # ====================================================
        # ESTIMATE CRITICAL POINT
        # ====================================================

        p_cr = estimate_p_cr(
            rows_for_N
        )


        critical_rows.append({

            "N":
                N,

            "p_critical":
                p_cr,

        })


        print(
            f"\nEstimated p_cr "
            f"for N={N}: "
            f"{p_cr:.5f}"
        )


        # ====================================================
        # SAVE AFTER EACH N
        #
        # Prevents losing hours of work if something crashes.
        # ====================================================

        save_results(
            all_rows,
            curve_rows,
            critical_rows,
        )

        print(
            f"Checkpoint saved after N={N}"
        )


    # ========================================================
    # FINAL SAVE
    # ========================================================

    save_results(
        all_rows,
        curve_rows,
        critical_rows,
    )


    # ========================================================
    # PLOT
    # ========================================================

    make_plot(
        curve_rows
    )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print("\n" + "=" * 80)

    print(
        "ESTIMATED CRITICAL POINTS"
    )

    print("=" * 80)


    for row in critical_rows:

        print(
            f"N={row['N']:4d} | "
            f"p_cr="
            f"{row['p_critical']:.5f}"
        )


    print("\nSaved:")

    print(ALL_FILE)
    print(CURVE_FILE)
    print(PCR_FILE)
    print(FIGURE_FILE)


    total_runtime = (
        time.perf_counter()
        -
        total_start
    )


    print(
        f"\nTotal runtime: "
        f"{total_runtime:.2f} s"
    )


# ============================================================
# WINDOWS MULTIPROCESSING GUARD
# ============================================================

if __name__ == "__main__":

    main()