"""
phase_8_shortcut_orientation.py

PHASE 8
-------

Test the mechanism suggested by Phase 7:

Do successful networks contain shortcuts that point
back toward the stimulated region?

For each shortcut:

    source -> target

define:

    delta_d =
        distance(target, stimulus)
        - distance(source, stimulus)

Interpretation:

    delta_d < 0
        shortcut points TOWARD stimulus region

    delta_d > 0
        shortcut points AWAY from stimulus region

    delta_d = 0
        no radial orientation relative to stimulus

The script:
    1. Reads Phase 6 outcomes.
    2. Selects mixed p closest to P_success = 0.5.
    3. Reconstructs exact networks using p + seed.
    4. Measures shortcut orientation.
    5. Compares SUCCESS vs FAILURE.
"""

from pathlib import Path
import csv

import numpy as np
import matplotlib.pyplot as plt

from network import (
    build_ring_network,
    add_random_shortcuts,
)


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
    / "phase8"
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
# OPTIONAL MANUAL p
# ============================================================

# None:
# automatically select mixed p closest to 50% success

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


            distance_from_half = abs(
                p_success
                - 0.5
            )


            candidates.append(
                (
                    distance_from_half,
                    p,
                    p_success,
                )
            )


    if len(candidates) == 0:

        raise RuntimeError(

            "No mixed transition p found.\n"

            "Phase 6 must contain at least one p "
            "with both SUCCESS and FAILURE."
        )


    candidates.sort(
        key=lambda item:
            item[0]
    )


    return candidates[0][1]


# ============================================================
# SHORTCUT ORIENTATION FEATURES
# ============================================================

def calculate_orientation_features(
    shortcuts,
    stimulus_neuron,
    N,
):


    delta_values = []


    for source, target in shortcuts:


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


        delta_values.append(
            delta_d
        )


    delta_values = np.array(
        delta_values,
        dtype=float,
    )


    # --------------------------------------------------------
    # HANDLE ZERO SHORTCUTS
    # --------------------------------------------------------

    if len(delta_values) == 0:

        return {

            "mean_delta_d": 0.0,

            "min_delta_d": 0.0,

            "max_delta_d": 0.0,

            "std_delta_d": 0.0,

            "toward_count": 0,

            "away_count": 0,

            "neutral_count": 0,

            "toward_fraction": 0.0,

            "away_fraction": 0.0,

            "strongest_return":
                0.0,

            "net_orientation":
                0.0,
        }


    # --------------------------------------------------------
    # COUNTS
    # --------------------------------------------------------

    toward_count = int(
        np.sum(
            delta_values < 0
        )
    )


    away_count = int(
        np.sum(
            delta_values > 0
        )
    )


    neutral_count = int(
        np.sum(
            delta_values == 0
        )
    )


    total_shortcuts = len(
        delta_values
    )


    # --------------------------------------------------------
    # RETURN FEATURES
    # --------------------------------------------------------

    return {

        "mean_delta_d":

            float(
                np.mean(
                    delta_values
                )
            ),


        "min_delta_d":

            float(
                np.min(
                    delta_values
                )
            ),


        "max_delta_d":

            float(
                np.max(
                    delta_values
                )
            ),


        "std_delta_d":

            float(
                np.std(
                    delta_values
                )
            ),


        "toward_count":

            toward_count,


        "away_count":

            away_count,


        "neutral_count":

            neutral_count,


        "toward_fraction":

            toward_count
            / total_shortcuts,


        "away_fraction":

            away_count
            / total_shortcuts,


        # More positive means stronger
        # return toward stimulus

        "strongest_return":

            float(
                -np.min(
                    delta_values
                )
            ),


        # Positive:
        # more shortcuts point toward stimulus

        # Negative:
        # more shortcuts point away

        "net_orientation":

            (
                toward_count
                - away_count
            )
            / total_shortcuts,
    }


# ============================================================
# HEADER
# ============================================================

print("=" * 80)


print(
    "PHASE 8: SHORTCUT ORIENTATION MECHANISM"
)


print("=" * 80)


print(

    "\nHypothesis:\n"

    "Successful networks contain shortcuts that "
    "return activity toward the stimulated region."

)


print(

    "\ndelta_d = "
    "target distance - source distance"

)


print(

    "\ndelta_d < 0 : TOWARD stimulus"

)


print(

    "delta_d > 0 : AWAY from stimulus"

)


# ============================================================
# LOAD PHASE 6
# ============================================================

all_rows = read_csv(
    PHASE6_ALL_FILE
)


probability_rows = read_csv(
    PHASE6_PROBABILITY_FILE
)


# ============================================================
# SELECT p
# ============================================================

selected_p = (
    select_transition_p(
        probability_rows
    )
)


print("\nSELECTED p")


print("-" * 50)


print(
    "p =",
    selected_p,
)


# ============================================================
# SELECT REALIZATIONS
# ============================================================

selected_rows = [


    row


    for row in all_rows


    if np.isclose(

        float(
            row["p"]
        ),

        selected_p,

    )

]


success_count = sum(

    row["status"] == "SUCCESS"

    for row in selected_rows

)


failure_count = sum(

    row["status"] == "FAILURE"

    for row in selected_rows

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
# VALIDATION
# ============================================================

if (
    success_count == 0
    or
    failure_count == 0
):


    raise RuntimeError(

        "Selected p must contain both "
        "SUCCESS and FAILURE."
    )


# ============================================================
# RECONSTRUCT NETWORKS
# ============================================================

print("\n")


print("=" * 80)


print(
    "ANALYZING SHORTCUT ORIENTATION"
)


print("=" * 80)


results = []


for row in selected_rows:


    seed = int(
        row["seed"]
    )


    status = (
        row["status"]
    )


    # --------------------------------------------------------
    # BUILD EXACT NETWORK
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
    # ORIENTATION FEATURES
    # --------------------------------------------------------

    features = (
        calculate_orientation_features(

            shortcuts=
                shortcuts,

            stimulus_neuron=
                STIMULUS_NEURON,

            N=N,
        )
    )


    result_row = {

        "p":
            selected_p,

        "seed":
            seed,

        "status":
            status,

        "outcome":
            1
            if status == "SUCCESS"
            else 0,

        **features,
    }


    results.append(
        result_row
    )


    print(

        f"Seed {seed:3d} | "

        f"{status:7s} | "

        f"Mean Δd = "
        f"{features['mean_delta_d']:+6.2f} | "

        f"Toward = "
        f"{features['toward_count']:2d} | "

        f"Away = "
        f"{features['away_count']:2d} | "

        f"Strongest return = "
        f"{features['strongest_return']:5.1f}"
    )


# ============================================================
# SAVE ALL RESULTS
# ============================================================

results_file = (

    RESULTS_DIR

    / "phase8_orientation_features.csv"
)


with open(
    results_file,
    "w",
    newline="",
) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=
            list(
                results[0].keys()
            ),
    )


    writer.writeheader()


    writer.writerows(
        results
    )


# ============================================================
# FEATURE LIST
# ============================================================

feature_names = [

    "mean_delta_d",

    "min_delta_d",

    "max_delta_d",

    "std_delta_d",

    "toward_count",

    "away_count",

    "neutral_count",

    "toward_fraction",

    "away_fraction",

    "strongest_return",

    "net_orientation",
]


# ============================================================
# GROUP COMPARISON
# ============================================================

group_results = []


print("\n")


print("=" * 80)


print(
    "SUCCESS VS FAILURE"
)


print("=" * 80)


for feature in feature_names:


    success_values = np.array(

        [

            float(
                row[feature]
            )

            for row in results

            if row["status"]
            == "SUCCESS"
        ]
    )


    failure_values = np.array(

        [

            float(
                row[feature]
            )

            for row in results

            if row["status"]
            == "FAILURE"
        ]
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


    group_results.append({

        "feature":
            feature,

        "success_mean":
            success_mean,

        "failure_mean":
            failure_mean,

        "difference_success_minus_failure":
            difference,
    })


    print(

        f"{feature:25s} | "

        f"SUCCESS = "
        f"{success_mean:+7.3f} | "

        f"FAILURE = "
        f"{failure_mean:+7.3f} | "

        f"Difference = "
        f"{difference:+7.3f}"
    )


# ============================================================
# SAVE GROUP COMPARISON
# ============================================================

group_file = (

    RESULTS_DIR

    / "phase8_group_comparison.csv"
)


with open(
    group_file,
    "w",
    newline="",
) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=[
            "feature",
            "success_mean",
            "failure_mean",
            "difference_success_minus_failure",
        ],
    )


    writer.writeheader()


    writer.writerows(
        group_results
    )


# ============================================================
# CORRELATION WITH SUCCESS
# ============================================================

outcomes = np.array(

    [
        row["outcome"]
        for row in results
    ],

    dtype=float,
)


correlation_results = []


for feature in feature_names:


    values = np.array(

        [
            float(
                row[feature]
            )

            for row in results
        ],

        dtype=float,
    )


    if np.std(values) == 0:

        correlation = 0.0


    else:

        correlation = float(

            np.corrcoef(

                values,

                outcomes,

            )[0, 1]

        )


    correlation_results.append({

        "feature":
            feature,

        "correlation_with_success":
            correlation,

        "absolute_correlation":
            abs(correlation),
    })


correlation_results.sort(

    key=lambda row:

        row[
            "absolute_correlation"
        ],

    reverse=True,
)


# ============================================================
# SAVE CORRELATIONS
# ============================================================

correlation_file = (

    RESULTS_DIR

    / "phase8_orientation_correlations.csv"
)


with open(
    correlation_file,
    "w",
    newline="",
) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=[
            "feature",
            "correlation_with_success",
            "absolute_correlation",
        ],
    )


    writer.writeheader()


    writer.writerows(
        correlation_results
    )


# ============================================================
# PRINT CORRELATIONS
# ============================================================

print("\n")


print("=" * 80)


print(
    "ORIENTATION CORRELATION WITH SUCCESS"
)


print("=" * 80)


for row in correlation_results:


    print(

        f"{row['feature']:25s} | "

        f"r = "

        f"{row['correlation_with_success']:+.3f}"
    )


# ============================================================
# MAIN FIGURE
# ============================================================

success_delta = [

    row["mean_delta_d"]

    for row in results

    if row["status"]
    == "SUCCESS"
]


failure_delta = [

    row["mean_delta_d"]

    for row in results

    if row["status"]
    == "FAILURE"
]


plt.figure(
    figsize=(8, 6)
)


plt.boxplot(

    [
        failure_delta,
        success_delta,
    ],

    tick_labels=[
        "FAILURE",
        "SUCCESS",
    ],
)


plt.axhline(
    0.0,
    linewidth=1,
)


plt.ylabel(
    "Mean shortcut orientation Δd"
)


plt.title(

    "Shortcut Orientation vs Propagation Outcome\n"

    f"p = {selected_p:.2f}"

)


plt.tight_layout()


figure_file = (

    RESULTS_DIR

    / "phase8_orientation_outcome.png"
)


plt.savefig(
    figure_file,
    dpi=300,
    bbox_inches="tight",
)


plt.show()


# ============================================================
# FINAL HYPOTHESIS TEST
# ============================================================

success_mean_delta = float(

    np.mean(
        success_delta
    )
)


failure_mean_delta = float(

    np.mean(
        failure_delta
    )
)


print("\n")


print("=" * 80)


print(
    "PHASE 8 MECHANISM TEST"
)


print("=" * 80)


print(

    "Mean Δd for SUCCESS =",

    success_mean_delta,
)


print(

    "Mean Δd for FAILURE =",

    failure_mean_delta,
)


if (
    success_mean_delta
    <
    failure_mean_delta
):


    print("\nHYPOTHESIS SUPPORTED")


    print(

        "Successful networks have shortcuts "

        "that point more strongly toward "

        "the stimulated region."

    )


else:


    print("\nHYPOTHESIS NOT SUPPORTED")


    print(

        "Successful networks do not show "

        "stronger return orientation."

    )


# ============================================================
# OUTPUT FILES
# ============================================================

print("\n")


print("=" * 80)


print("RESULTS SAVED")


print("=" * 80)


print(
    "\nOrientation features:"
)


print(
    results_file
)


print(
    "\nGroup comparison:"
)


print(
    group_file
)


print(
    "\nCorrelations:"
)


print(
    correlation_file
)


print(
    "\nFigure:"
)


print(
    figure_file
)


print("\n")


print("=" * 80)


print("PHASE 8 COMPLETE")


print("=" * 80)