"""
phase_9_dynamic_shortcut_activation.py

PHASE 9
-------

Question:

    Are return-oriented shortcuts actually used dynamically
    during successful propagation?

For every shortcut:

    source -> target

we measure:

    1. Does the source neuron fire?
    2. Does the target fire shortly after the source?
    3. How many putative activation events occur?
    4. Are return-oriented shortcuts used more often?
    5. Does dynamic shortcut use differ between
       SUCCESS and FAILURE networks?

IMPORTANT:

    A "putative activation" means:

        source spike at t_source

        followed by

        target spike within:

            MIN_DELAY <=
            t_target - t_source
            <= MAX_DELAY

    This is temporal evidence of shortcut use.

    It is NOT yet strict causal proof because the target
    can also receive local ring inputs.
"""

from pathlib import Path
import csv

import numpy as np
import matplotlib.pyplot as plt

from network import (
    build_ring_network,
    add_random_shortcuts,
)

from simulator import run_simulation


# ============================================================
# PATH SETUP
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent


PHASE6_DIR = (
    PROJECT_DIR
    / "results"
    / "phase6"
)


RESULTS_DIR = (
    PROJECT_DIR
    / "results"
    / "phase9"
)


RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


PHASE6_ALL_FILE = (
    PHASE6_DIR
    / "phase6_all_realizations.csv"
)


PHASE6_PROBABILITY_FILE = (
    PHASE6_DIR
    / "phase6_probability_curve.csv"
)


# ============================================================
# NETWORK PARAMETERS
# ============================================================

N = 100

STIMULUS_NEURON = N // 2


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

T_MAX = 200.0

STIMULUS_TIME = 10.0


# ============================================================
# SHORTCUT ACTIVATION WINDOW
# ============================================================

# IMPORTANT:
#
# These values should eventually be matched to the
# actual temporal behavior of your simulator.
#
# First exploratory window:

MIN_DELAY = 0.0

MAX_DELAY = 2.0


# ============================================================
# p SELECTION
# ============================================================

# None:
#
# automatically select the mixed p closest
# to P_success = 0.5

MANUAL_P = None


# ============================================================
# READ CSV
# ============================================================

def read_csv(file_path):


    if not file_path.exists():


        raise FileNotFoundError(

            f"Required file not found:\n"

            f"{file_path}\n\n"

            "Run Phase 6 first."

        )


    with open(

        file_path,

        "r",

        newline="",

    ) as file:


        return list(

            csv.DictReader(file)

        )


# ============================================================
# CIRCULAR DISTANCE
# ============================================================

def circular_distance(

    neuron_a,

    neuron_b,

    N,

):


    direct_distance = abs(

        neuron_b

        - neuron_a

    )


    return min(

        direct_distance,

        N - direct_distance,

    )


# ============================================================
# SHORTCUT ORIENTATION
# ============================================================

def shortcut_orientation(

    source,

    target,

    stimulus_neuron,

    N,

):


    source_distance = (

        circular_distance(

            source,

            stimulus_neuron,

            N,

        )

    )


    target_distance = (

        circular_distance(

            target,

            stimulus_neuron,

            N,

        )

    )


    delta_d = (

        target_distance

        - source_distance

    )


    if delta_d < 0:


        orientation = "TOWARD"


    elif delta_d > 0:


        orientation = "AWAY"


    else:


        orientation = "NEUTRAL"


    return (

        source_distance,

        target_distance,

        delta_d,

        orientation,

    )


# ============================================================
# SELECT TRANSITION p
# ============================================================

def select_transition_p(

    probability_rows,

):


    if MANUAL_P is not None:


        return float(

            MANUAL_P

        )


    candidates = []


    for row in probability_rows:


        p = float(

            row["p"]

        )


        p_success = float(

            row[

                "probability_success"

            ]

        )


        if (

            p_success > 0.0

            and

            p_success < 1.0

        ):


            candidates.append(

                (

                    abs(

                        p_success

                        - 0.5

                    ),

                    p,

                )

            )


    if len(candidates) == 0:


        raise RuntimeError(

            "No mixed transition p found."

        )


    candidates.sort(

        key=lambda item:

            item[0]

    )


    return candidates[0][1]


# ============================================================
# ORGANIZE SPIKES BY NEURON
# ============================================================

def build_spike_lookup(

    spike_times,

    spike_neurons,

    N,

):


    spike_lookup = [

        []

        for _ in range(N)

    ]


    for time, neuron in zip(

        spike_times,

        spike_neurons,

    ):


        spike_lookup[

            int(neuron)

        ].append(

            float(time)

        )


    return [

        np.asarray(

            times,

            dtype=float,

        )

        for times

        in spike_lookup

    ]


# ============================================================
# ANALYZE ONE SHORTCUT
# ============================================================

def analyze_shortcut_activation(

    source,

    target,

    spike_lookup,

    min_delay,

    max_delay,

):


    source_spikes = (

        spike_lookup[source]

    )


    target_spikes = (

        spike_lookup[target]

    )


    # --------------------------------------------------------
    # SOURCE NEVER FIRED
    # --------------------------------------------------------

    if len(source_spikes) == 0:


        return {

            "source_fired":

                False,

            "target_fired":

                len(target_spikes) > 0,

            "activation_count":

                0,

            "activation_fraction":

                0.0,

            "first_source_spike":

                np.nan,

            "first_putative_activation":

                np.nan,

            "mean_activation_delay":

                np.nan,

        }


    # --------------------------------------------------------
    # SEARCH TEMPORAL ACTIVATIONS
    # --------------------------------------------------------

    activation_delays = []

    activation_times = []


    for source_time in source_spikes:


        earliest_target_time = (

            source_time

            + min_delay

        )


        latest_target_time = (

            source_time

            + max_delay

        )


        candidate_targets = (

            target_spikes[

                (

                    target_spikes

                    >= earliest_target_time

                )

                &

                (

                    target_spikes

                    <= latest_target_time

                )

            ]

        )


        if len(candidate_targets) > 0:


            first_target_time = (

                candidate_targets[0]

            )


            delay = (

                first_target_time

                - source_time

            )


            activation_delays.append(

                delay

            )


            activation_times.append(

                source_time

            )


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    activation_count = len(

        activation_delays

    )


    activation_fraction = (

        activation_count

        / len(source_spikes)

    )


    if activation_count > 0:


        first_activation = float(

            activation_times[0]

        )


        mean_delay = float(

            np.mean(

                activation_delays

            )

        )


    else:


        first_activation = np.nan

        mean_delay = np.nan


    return {

        "source_fired":

            True,

        "target_fired":

            len(target_spikes) > 0,

        "activation_count":

            activation_count,

        "activation_fraction":

            activation_fraction,

        "first_source_spike":

            float(

                source_spikes[0]

            ),

        "first_putative_activation":

            first_activation,

        "mean_activation_delay":

            mean_delay,

    }


# ============================================================
# HEADER
# ============================================================

print("=" * 80)


print(

    "PHASE 9: DYNAMIC SHORTCUT ACTIVATION"

)


print("=" * 80)


print(

    "\nQuestion:"

)


print(

    "Are return-oriented shortcuts actually used "

    "during successful propagation?"

)


print(

    "\nPutative activation window:"

)


print(

    f"{MIN_DELAY} <= target delay <= "

    f"{MAX_DELAY}"

)


# ============================================================
# LOAD PHASE 6 RESULTS
# ============================================================

all_phase6_rows = read_csv(

    PHASE6_ALL_FILE

)


probability_rows = read_csv(

    PHASE6_PROBABILITY_FILE

)


# ============================================================
# SELECT p
# ============================================================

selected_p = select_transition_p(

    probability_rows

)


print(

    "\nSelected p =",

    selected_p,

)


# ============================================================
# SELECT NETWORK REALIZATIONS
# ============================================================

selected_rows = [

    row

    for row in all_phase6_rows

    if np.isclose(

        float(

            row["p"]

        ),

        selected_p,

    )

]


success_count = sum(

    row["status"]

    == "SUCCESS"

    for row

    in selected_rows

)


failure_count = sum(

    row["status"]

    == "FAILURE"

    for row

    in selected_rows

)


print(

    "Realizations =",

    len(selected_rows),

)


print(

    "Successes =",

    success_count,

)


print(

    "Failures =",

    failure_count,

)


# ============================================================
# STORAGE
# ============================================================

shortcut_results = []

network_results = []


# ============================================================
# RERUN EXACT NETWORKS
# ============================================================

print("\n")


print("=" * 80)


print(

    "RERUNNING NETWORKS AND TRACKING SHORTCUT USE"

)


print("=" * 80)


for network_index, phase6_row in enumerate(

    selected_rows

):


    seed = int(

        phase6_row["seed"]

    )


    expected_status = (

        phase6_row["status"]

    )


    # --------------------------------------------------------
    # REBUILD EXACT NETWORK
    # --------------------------------------------------------

    local_network = (

        build_ring_network(N)

    )


    network, shortcuts = (

        add_random_shortcuts(

            outgoing_connections=

                local_network,

            p=selected_p,

            seed=seed,

        )

    )


    # --------------------------------------------------------
    # RERUN SIMULATION
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # BUILD SPIKE LOOKUP
    # --------------------------------------------------------

    spike_lookup = (

        build_spike_lookup(

            spike_times,

            spike_neurons,

            N,

        )

    )


    # --------------------------------------------------------
    # NETWORK COUNTERS
    # --------------------------------------------------------

    active_shortcut_count = 0

    total_activation_events = 0

    toward_activation_events = 0

    away_activation_events = 0

    active_toward_shortcuts = 0

    active_away_shortcuts = 0


    # --------------------------------------------------------
    # ANALYZE EVERY SHORTCUT
    # --------------------------------------------------------

    for shortcut_index, (

        source,

        target,

    ) in enumerate(shortcuts):


        (

            source_distance,

            target_distance,

            delta_d,

            orientation,

        ) = shortcut_orientation(

            source,

            target,

            STIMULUS_NEURON,

            N,

        )


        activation = (

            analyze_shortcut_activation(

                source=

                    source,

                target=

                    target,

                spike_lookup=

                    spike_lookup,

                min_delay=

                    MIN_DELAY,

                max_delay=

                    MAX_DELAY,

            )

        )


        # ----------------------------------------------------
        # COUNT ACTIVE SHORTCUT
        # ----------------------------------------------------

        is_active = (

            activation[

                "activation_count"

            ]

            > 0

        )


        if is_active:


            active_shortcut_count += 1


            if orientation == "TOWARD":


                active_toward_shortcuts += 1


            elif orientation == "AWAY":


                active_away_shortcuts += 1


        # ----------------------------------------------------
        # COUNT EVENTS
        # ----------------------------------------------------

        event_count = (

            activation[

                "activation_count"

            ]

        )


        total_activation_events += (

            event_count

        )


        if orientation == "TOWARD":


            toward_activation_events += (

                event_count

            )


        elif orientation == "AWAY":


            away_activation_events += (

                event_count

            )


        # ----------------------------------------------------
        # STORE SHORTCUT RESULT
        # ----------------------------------------------------

        shortcut_results.append({

            "p":

                selected_p,

            "seed":

                seed,

            "status":

                expected_status,

            "shortcut_index":

                shortcut_index,

            "source":

                source,

            "target":

                target,

            "source_distance":

                source_distance,

            "target_distance":

                target_distance,

            "delta_d":

                delta_d,

            "orientation":

                orientation,

            "source_fired":

                activation[

                    "source_fired"

                ],

            "target_fired":

                activation[

                    "target_fired"

                ],

            "activation_count":

                activation[

                    "activation_count"

                ],

            "activation_fraction":

                activation[

                    "activation_fraction"

                ],

            "first_source_spike":

                activation[

                    "first_source_spike"

                ],

            "first_putative_activation":

                activation[

                    "first_putative_activation"

                ],

            "mean_activation_delay":

                activation[

                    "mean_activation_delay"

                ],

        })


    # --------------------------------------------------------
    # NETWORK SUMMARY
    # --------------------------------------------------------

    total_shortcuts = len(

        shortcuts

    )


    active_fraction = (

        active_shortcut_count

        / total_shortcuts

        if total_shortcuts > 0

        else 0.0

    )


    network_results.append({

        "p":

            selected_p,

        "seed":

            seed,

        "status":

            expected_status,

        "outcome":

            1

            if expected_status == "SUCCESS"

            else 0,

        "total_spikes":

            len(spike_times),

        "total_shortcuts":

            total_shortcuts,

        "active_shortcuts":

            active_shortcut_count,

        "active_shortcut_fraction":

            active_fraction,

        "total_activation_events":

            total_activation_events,

        "active_toward_shortcuts":

            active_toward_shortcuts,

        "active_away_shortcuts":

            active_away_shortcuts,

        "toward_activation_events":

            toward_activation_events,

        "away_activation_events":

            away_activation_events,

        "activation_orientation_balance":

            toward_activation_events

            - away_activation_events,

    })


    # --------------------------------------------------------
    # PRINT NETWORK RESULT
    # --------------------------------------------------------

    print(

        f"{network_index + 1:3d}/"

        f"{len(selected_rows):3d} | "

        f"Seed {seed:3d} | "

        f"{expected_status:7s} | "

        f"Active shortcuts = "

        f"{active_shortcut_count}/"

        f"{total_shortcuts} | "

        f"Toward events = "

        f"{toward_activation_events:3d} | "

        f"Away events = "

        f"{away_activation_events:3d}"

    )


# ============================================================
# SAVE SHORTCUT-LEVEL RESULTS
# ============================================================

shortcut_file = (

    RESULTS_DIR

    / "phase9_shortcut_activation_events.csv"

)


with open(

    shortcut_file,

    "w",

    newline="",

) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=

            list(

                shortcut_results[0].keys()

            ),

    )


    writer.writeheader()


    writer.writerows(

        shortcut_results

    )


# ============================================================
# SAVE NETWORK-LEVEL RESULTS
# ============================================================

network_file = (

    RESULTS_DIR

    / "phase9_network_dynamic_summary.csv"

)


with open(

    network_file,

    "w",

    newline="",

) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=

            list(

                network_results[0].keys()

            ),

    )


    writer.writeheader()


    writer.writerows(

        network_results

    )


# ============================================================
# SUCCESS VS FAILURE COMPARISON
# ============================================================

features = [

    "active_shortcut_fraction",

    "total_activation_events",

    "active_toward_shortcuts",

    "active_away_shortcuts",

    "toward_activation_events",

    "away_activation_events",

    "activation_orientation_balance",

]


print("\n")


print("=" * 80)


print(

    "DYNAMIC SUCCESS VS FAILURE COMPARISON"

)


print("=" * 80)


comparison_results = []


for feature in features:


    success_values = np.array(

        [

            row[feature]

            for row in network_results

            if row["status"]

            == "SUCCESS"

        ],

        dtype=float,

    )


    failure_values = np.array(

        [

            row[feature]

            for row in network_results

            if row["status"]

            == "FAILURE"

        ],

        dtype=float,

    )


    success_mean = float(

        np.mean(

            success_values

        )

    )


    failure_mean = float(

        np.mean(

            failure_values

        )

    )


    difference = (

        success_mean

        - failure_mean

    )


    comparison_results.append({

        "feature":

            feature,

        "success_mean":

            success_mean,

        "failure_mean":

            failure_mean,

        "difference":

            difference,

    })


    print(

        f"{feature:35s} | "

        f"SUCCESS = "

        f"{success_mean:8.3f} | "

        f"FAILURE = "

        f"{failure_mean:8.3f} | "

        f"Difference = "

        f"{difference:+8.3f}"

    )


# ============================================================
# SAVE COMPARISON
# ============================================================

comparison_file = (

    RESULTS_DIR

    / "phase9_dynamic_group_comparison.csv"

)


with open(

    comparison_file,

    "w",

    newline="",

) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=[

            "feature",

            "success_mean",

            "failure_mean",

            "difference",

        ],

    )


    writer.writeheader()


    writer.writerows(

        comparison_results

    )


# ============================================================
# MAIN FIGURE
# ============================================================

success_toward_events = [

    row[

        "toward_activation_events"

    ]

    for row in network_results

    if row["status"]

    == "SUCCESS"

]


failure_toward_events = [

    row[

        "toward_activation_events"

    ]

    for row in network_results

    if row["status"]

    == "FAILURE"

]


plt.figure(

    figsize=(8, 6)

)


plt.boxplot(

    [

        failure_toward_events,

        success_toward_events,

    ],

    tick_labels=[

        "FAILURE",

        "SUCCESS",

    ],

)


plt.ylabel(

    "Putative activation events through\n"

    "return-oriented shortcuts"

)


plt.title(

    "Dynamic Return-Shortcut Use vs Propagation Outcome\n"

    f"p = {selected_p:.2f}"

)


plt.tight_layout()


figure_file = (

    RESULTS_DIR

    / "phase9_dynamic_return_shortcut_use.png"

)


plt.savefig(

    figure_file,

    dpi=300,

    bbox_inches="tight",

)


plt.show()


# ============================================================
# FINAL MECHANISM TEST
# ============================================================

success_mean = float(

    np.mean(

        success_toward_events

    )

)


failure_mean = float(

    np.mean(

        failure_toward_events

    )

)


print("\n")


print("=" * 80)


print(

    "PHASE 9 DYNAMIC MECHANISM TEST"

)


print("=" * 80)


print(

    "Mean return-shortcut events "

    "in SUCCESS =",

    success_mean,

)


print(

    "Mean return-shortcut events "

    "in FAILURE =",

    failure_mean,

)


if success_mean > failure_mean:


    print(

        "\nDYNAMIC HYPOTHESIS SUPPORTED"

    )


    print(

        "Successful networks dynamically use "

        "return-oriented shortcuts more often."

    )


else:


    print(

        "\nDYNAMIC HYPOTHESIS NOT SUPPORTED"

    )


# ============================================================
# OUTPUT FILES
# ============================================================

print("\n")


print("=" * 80)


print("RESULTS SAVED")


print("=" * 80)


print(

    "\nShortcut-level results:"

)


print(

    shortcut_file

)


print(

    "\nNetwork-level summary:"

)


print(

    network_file

)


print(

    "\nGroup comparison:"

)


print(

    comparison_file

)


print(

    "\nFigure:"

)


print(

    figure_file

)


print("\n")


print("=" * 80)


print("PHASE 9 COMPLETE")


print("=" * 80)