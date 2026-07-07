"""
phase_11_N2000_time_horizon_control.py

PHASE 11
--------

Goal:

    Determine the correct simulation time horizon for N = 2000.

Problem discovered in Phase 10:

    At T_MAX = 200, every N = 2000 realization
    was classified as SUCCESS.

Possible explanation:

    The initial propagating wave may simply still be travelling
    through the large ring when the simulation ends.

Therefore, before estimating P_failure(p), we must determine:

    1. How long does activity last in a pure ring (p = 0)?
    2. How does lifetime change with 1, 2, and 4 shortcuts?
    3. Is activity still present near T_MAX = 3000?

IMPORTANT:

    This is a time-horizon control experiment.

    Do NOT interpret "reaches T_MAX" as final proof
    of persistent activity yet.
"""


# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path

import csv
import time

import numpy as np
import matplotlib.pyplot as plt


from network import (
    build_ring_network,
    add_random_shortcuts,
)


from simulator import (
    run_simulation,
)


# ============================================================
# PATH SETUP
# ============================================================

PROJECT_DIR = (
    Path(__file__)
    .resolve()
    .parent
)


RESULTS_DIR = (

    PROJECT_DIR

    / "results"

    / "phase11"

)


RESULTS_DIR.mkdir(

    parents=True,

    exist_ok=True,

)


RESULTS_FILE = (

    RESULTS_DIR

    / "phase11_N2000_time_horizon_control.csv"

)


SUMMARY_FILE = (

    RESULTS_DIR

    / "phase11_N2000_time_horizon_summary.csv"

)


FIGURE_FILE = (

    RESULTS_DIR

    / "phase11_N2000_activity_lifetime.png"

)


# ============================================================
# NETWORK PARAMETERS
# ============================================================

N = 2000


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


# Long simulation required for N = 2000

T_MAX = 3000.0


STIMULUS_NEURON = (
    N // 2
)


STIMULUS_TIME = 10.0


# ============================================================
# CONTROL p VALUES
# ============================================================

P_VALUES = np.array([

    0.0,       # pure ring

    0.0005,    # 1 shortcut

    0.001,     # 2 shortcuts

    0.002,     # 4 shortcuts

])


# ============================================================
# NUMBER OF REALIZATIONS
# ============================================================

# Small control experiment only.

NUM_REALIZATIONS = 5


# ============================================================
# FINAL OBSERVATION WINDOW
# ============================================================

FINAL_WINDOW = 200.0


FINAL_WINDOW_START = (

    T_MAX

    - FINAL_WINDOW

)


# ============================================================
# ACTIVITY ANALYSIS
# ============================================================

def analyze_activity(

    spike_times,

):


    spike_times = np.asarray(

        spike_times,

        dtype=float,

    )


    # --------------------------------------------------------
    # NO SPIKES
    # --------------------------------------------------------

    if len(spike_times) == 0:


        return {

            "total_spikes":

                0,


            "first_spike_time":

                np.nan,


            "last_spike_time":

                np.nan,


            "activity_duration":

                0.0,


            "spikes_in_final_window":

                0,


            "reached_tmax":

                False,

        }


    # --------------------------------------------------------
    # FIRST SPIKE
    # --------------------------------------------------------

    first_spike_time = float(

        np.min(

            spike_times

        )

    )


    # --------------------------------------------------------
    # LAST SPIKE
    # --------------------------------------------------------

    last_spike_time = float(

        np.max(

            spike_times

        )

    )


    # --------------------------------------------------------
    # ACTIVITY DURATION
    # --------------------------------------------------------

    activity_duration = (

        last_spike_time

        - STIMULUS_TIME

    )


    # --------------------------------------------------------
    # FINAL WINDOW SPIKES
    # --------------------------------------------------------

    spikes_in_final_window = int(

        np.sum(

            spike_times

            >= FINAL_WINDOW_START

        )

    )


    # --------------------------------------------------------
    # REACHED SIMULATION END?
    # --------------------------------------------------------

    reached_tmax = (

        spikes_in_final_window

        > 0

    )


    return {

        "total_spikes":

            len(spike_times),


        "first_spike_time":

            first_spike_time,


        "last_spike_time":

            last_spike_time,


        "activity_duration":

            activity_duration,


        "spikes_in_final_window":

            spikes_in_final_window,


        "reached_tmax":

            reached_tmax,

    }


# ============================================================
# HEADER
# ============================================================

print("=" * 80)


print(

    "PHASE 11: N = 2000 TIME-HORIZON CONTROL"

)


print("=" * 80)


print("\nQUESTION")


print("-" * 50)


print(

    "How long does activity naturally survive "

    "at N = 2000?"

)


print("\nNETWORK")


print("-" * 50)


print(

    "N =",

    N,

)


print("\nSIMULATION")


print("-" * 50)


print(

    "dt =",

    DT,

)


print(

    "T_max =",

    T_MAX,

)


print(

    "Stimulus neuron =",

    STIMULUS_NEURON,

)


print(

    "Stimulus time =",

    STIMULUS_TIME,

)


print(

    "Final observation window =",

    f"{FINAL_WINDOW_START} to {T_MAX}",

)


print("\nCONTROL p VALUES")


print("-" * 50)


for p in P_VALUES:


    print(

        f"p = {p:.4f} | "

        f"shortcuts = "

        f"{int(round(p * N))}"

    )


print(

    "\nRealizations per p =",

    NUM_REALIZATIONS,

)


# ============================================================
# STORAGE
# ============================================================

all_results = []


# ============================================================
# BUILD LOCAL RING ONCE
# ============================================================

print("\n")


print("=" * 80)


print(

    "BUILDING N = 2000 LOCAL RING"

)


print("=" * 80)


local_network = (

    build_ring_network(

        N

    )

)


print(

    "Local ring created."

)


print(

    "Local directed edges =",

    2 * N,

)


# ============================================================
# START TOTAL TIMER
# ============================================================

total_start_time = (

    time.perf_counter()

)


# ============================================================
# RUN CONTROL EXPERIMENT
# ============================================================

for p in P_VALUES:


    p = float(p)


    expected_shortcuts = int(

        round(

            p * N

        )

    )


    print("\n")


    print("=" * 80)


    print(

        f"CONTROL p = {p:.4f}"

    )


    print("=" * 80)


    print(

        "Expected shortcuts =",

        expected_shortcuts,

    )


    # --------------------------------------------------------
    # RUN REALIZATIONS
    # --------------------------------------------------------

    for seed in range(

        NUM_REALIZATIONS

    ):


        # ----------------------------------------------------
        # BUILD NETWORK
        # ----------------------------------------------------

        network, shortcuts = (

            add_random_shortcuts(

                outgoing_connections=

                    local_network,


                p=

                    p,


                seed=

                    seed,

            )

        )


        # ----------------------------------------------------
        # START RUN TIMER
        # ----------------------------------------------------

        run_start_time = (

            time.perf_counter()

        )


        # ----------------------------------------------------
        # RUN LONG SIMULATION
        # ----------------------------------------------------

        spike_times, spike_neurons = (

            run_simulation(

                outgoing_connections=

                    network,


                I_ext=

                    I_EXT,


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

        )


        # ----------------------------------------------------
        # END RUN TIMER
        # ----------------------------------------------------

        runtime_seconds = (

            time.perf_counter()

            - run_start_time

        )


        # ----------------------------------------------------
        # ANALYZE ACTIVITY
        # ----------------------------------------------------

        analysis = (

            analyze_activity(

                spike_times

            )

        )


        # ----------------------------------------------------
        # STORE RESULT
        # ----------------------------------------------------

        result = {


            "N":

                N,


            "p":

                p,


            "seed":

                seed,


            "number_of_shortcuts":

                len(shortcuts),


            "total_spikes":

                analysis[

                    "total_spikes"

                ],


            "first_spike_time":

                analysis[

                    "first_spike_time"

                ],


            "last_spike_time":

                analysis[

                    "last_spike_time"

                ],


            "activity_duration":

                analysis[

                    "activity_duration"

                ],


            "spikes_in_final_window":

                analysis[

                    "spikes_in_final_window"

                ],


            "reached_tmax":

                analysis[

                    "reached_tmax"

                ],


            "runtime_seconds":

                runtime_seconds,

        }


        all_results.append(

            result

        )


        # ----------------------------------------------------
        # PRINT RESULT
        # ----------------------------------------------------

        if analysis["reached_tmax"]:


            end_status = (

                "ACTIVE AT END"

            )


        else:


            end_status = (

                "DIED EARLY"

            )


        print(


            f"Seed {seed:2d} | "


            f"{end_status:13s} | "


            f"Shortcuts = "

            f"{len(shortcuts):2d} | "


            f"Spikes = "

            f"{analysis['total_spikes']:7d} | "


            f"Last = "

            f"{analysis['last_spike_time']:8.2f} | "


            f"Final-window spikes = "

            f"{analysis['spikes_in_final_window']:6d} | "


            f"Runtime = "

            f"{runtime_seconds:6.2f} s"

        )


# ============================================================
# SAVE ALL REALIZATIONS
# ============================================================

with open(

    RESULTS_FILE,

    "w",

    newline="",

) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=[

            "N",

            "p",

            "seed",

            "number_of_shortcuts",

            "total_spikes",

            "first_spike_time",

            "last_spike_time",

            "activity_duration",

            "spikes_in_final_window",

            "reached_tmax",

            "runtime_seconds",

        ],

    )


    writer.writeheader()


    writer.writerows(

        all_results

    )


# ============================================================
# BUILD SUMMARY
# ============================================================

summary_results = []


print("\n")


print("=" * 80)


print(

    "PHASE 11 TIME-HORIZON SUMMARY"

)


print("=" * 80)


for p in P_VALUES:


    p = float(p)


    p_rows = [

        row

        for row in all_results

        if np.isclose(

            row["p"],

            p,

        )

    ]


    # --------------------------------------------------------
    # EXTRACT VALUES
    # --------------------------------------------------------

    last_spike_times = np.array(

        [

            row["last_spike_time"]

            for row in p_rows

        ],

        dtype=float,

    )


    total_spikes = np.array(

        [

            row["total_spikes"]

            for row in p_rows

        ],

        dtype=float,

    )


    runtimes = np.array(

        [

            row["runtime_seconds"]

            for row in p_rows

        ],

        dtype=float,

    )


    # --------------------------------------------------------
    # COUNT RUNS ACTIVE AT END
    # --------------------------------------------------------

    active_at_end_count = sum(

        row["reached_tmax"]

        for row in p_rows

    )


    died_early_count = (

        len(p_rows)

        - active_at_end_count

    )


    # --------------------------------------------------------
    # SUMMARY STATISTICS
    # --------------------------------------------------------

    mean_last_spike_time = float(

        np.mean(

            last_spike_times

        )

    )


    min_last_spike_time = float(

        np.min(

            last_spike_times

        )

    )


    max_last_spike_time = float(

        np.max(

            last_spike_times

        )

    )


    mean_total_spikes = float(

        np.mean(

            total_spikes

        )

    )


    mean_runtime = float(

        np.mean(

            runtimes

        )

    )


    # --------------------------------------------------------
    # STORE SUMMARY
    # --------------------------------------------------------

    summary_row = {


        "p":

            p,


        "number_of_shortcuts":

            int(

                round(

                    p * N

                )

            ),


        "realizations":

            len(p_rows),


        "active_at_end":

            active_at_end_count,


        "died_early":

            died_early_count,


        "mean_last_spike_time":

            mean_last_spike_time,


        "min_last_spike_time":

            min_last_spike_time,


        "max_last_spike_time":

            max_last_spike_time,


        "mean_total_spikes":

            mean_total_spikes,


        "mean_runtime_seconds":

            mean_runtime,

    }


    summary_results.append(

        summary_row

    )


    # --------------------------------------------------------
    # PRINT SUMMARY
    # --------------------------------------------------------

    print(


        f"p = {p:7.4f} | "


        f"Shortcuts = "

        f"{int(round(p * N)):2d} | "


        f"Active at end = "

        f"{active_at_end_count}/{len(p_rows)} | "


        f"Died early = "

        f"{died_early_count}/{len(p_rows)} | "


        f"Mean last spike = "

        f"{mean_last_spike_time:8.2f} | "


        f"Range = "

        f"[{min_last_spike_time:8.2f}, "


        f"{max_last_spike_time:8.2f}]"

    )


# ============================================================
# SAVE SUMMARY
# ============================================================

with open(

    SUMMARY_FILE,

    "w",

    newline="",

) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=

            list(

                summary_results[0].keys()

            ),

    )


    writer.writeheader()


    writer.writerows(

        summary_results

    )


# ============================================================
# PLOT ACTIVITY LIFETIME
# ============================================================

plt.figure(

    figsize=(9, 6)

)


for p in P_VALUES:


    p = float(p)


    p_rows = [

        row

        for row in all_results

        if np.isclose(

            row["p"],

            p,

        )

    ]


    x_values = [

        p

        for _ in p_rows

    ]


    y_values = [

        row["last_spike_time"]

        for row in p_rows

    ]


    plt.scatter(

        x_values,

        y_values,

        s=70,

    )


# ------------------------------------------------------------
# SIMULATION END LINE
# ------------------------------------------------------------

plt.axhline(

    T_MAX,

    linestyle="--",

    linewidth=1.5,

    label="Simulation end",

)


# ------------------------------------------------------------
# FINAL WINDOW START
# ------------------------------------------------------------

plt.axhline(

    FINAL_WINDOW_START,

    linestyle=":",

    linewidth=1.5,

    label="Final-window start",

)


plt.xlabel(

    "Shortcut density p"

)


plt.ylabel(

    "Last spike time"

)


plt.title(

    "Activity Lifetime Control at N = 2000"

)


plt.legend()


plt.grid(

    True,

    alpha=0.3,

)


plt.tight_layout()


plt.savefig(

    FIGURE_FILE,

    dpi=300,

    bbox_inches="tight",

)


plt.show()


# ============================================================
# PURE RING CONTROL INTERPRETATION
# ============================================================

pure_ring_rows = [

    row

    for row in all_results

    if np.isclose(

        row["p"],

        0.0,

    )

]


pure_ring_active_at_end = sum(

    row["reached_tmax"]

    for row in pure_ring_rows

)


pure_ring_last_spikes = [

    row["last_spike_time"]

    for row in pure_ring_rows

]


print("\n")


print("=" * 80)


print(

    "PURE RING CONTROL"

)


print("=" * 80)


print(

    "p = 0"

)


print(

    "Shortcuts = 0"

)


print(

    "Active at simulation end =",

    f"{pure_ring_active_at_end}/"

    f"{len(pure_ring_rows)}",

)


print(

    "Last spike times =",

    [

        round(

            value,

            2,

        )

        for value in pure_ring_last_spikes

    ],

)


# ============================================================
# AUTOMATIC INTERPRETATION
# ============================================================

print("\n")


print("=" * 80)


print(

    "TIME-HORIZON INTERPRETATION"

)


print("=" * 80)


if pure_ring_active_at_end == 0:


    pure_ring_max_lifetime = max(

        pure_ring_last_spikes

    )


    print(

        "GOOD: The pure ring dies before T_MAX."

    )


    print(

        "Maximum pure-ring last spike time =",

        pure_ring_max_lifetime,

    )


    print(

        "\nT_MAX =",

        T_MAX,

        "is longer than the natural "

        "pure-ring transient."

    )


    print(

        "\nThe next phase can use this control "

        "to define a valid persistence criterion."

    )


else:


    print(

        "WARNING: The pure ring is still active "

        "near T_MAX."

    )


    print(

        "\nT_MAX =",

        T_MAX,

        "is still too short to distinguish "

        "transient propagation from persistence."

    )


    print(

        "\nIncrease T_MAX before running "

        "the N = 2000 probability sweep."

    )


# ============================================================
# RUNTIME SUMMARY
# ============================================================

total_runtime = (

    time.perf_counter()

    - total_start_time

)


mean_runtime = float(

    np.mean(

        [

            row["runtime_seconds"]

            for row in all_results

        ]

    )

)


print("\n")


print("=" * 80)


print(

    "RUNTIME SUMMARY"

)


print("=" * 80)


print(

    "Total simulations =",

    len(all_results),

)


print(

    "Mean runtime per simulation =",

    f"{mean_runtime:.2f} seconds",

)


print(

    "Total Phase 11 runtime =",

    f"{total_runtime:.2f} seconds",

)


# ============================================================
# OUTPUT FILES
# ============================================================

print("\n")


print("=" * 80)


print(

    "RESULTS SAVED"

)


print("=" * 80)


print(

    "\nAll realizations:"

)


print(

    RESULTS_FILE

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


print("\n")


print("=" * 80)


print(

    "PHASE 11 COMPLETE"

)


print("=" * 80)