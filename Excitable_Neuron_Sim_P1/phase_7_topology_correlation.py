"""
phase_7_topology_correlation.py

PHASE 7
-------

Question:

    At the SAME p and SAME neuron parameters,
    why do some network realizations SUCCEED
    while others FAIL?

Method:

    Phase 6 results
            ↓
    Select mixed p closest to P_success = 0.5
            ↓
    Reconstruct exact networks using same p and seed
            ↓
    Extract topology features
            ↓
    Compare SUCCESS vs FAILURE
            ↓
    Correlate topology with propagation outcome

IMPORTANT:

    Phase 7 does NOT rerun neural simulations.

    It uses:

        results/phase6/
        phase6_all_realizations.csv

        results/phase6/
        phase6_probability_curve.csv
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
    / "phase7"
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
# p SELECTION
# ============================================================

# None:
#
#     automatically choose mixed p closest
#     to P_success = 0.5
#
# Example manual selection:
#
#     MANUAL_P = 0.10

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


        rows = list(

            csv.DictReader(file)

        )


    return rows


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
# DIRECTED SHORTEST PATH
# ============================================================

def directed_shortest_paths(

    outgoing_connections,

    source,

):

    N = len(

        outgoing_connections

    )


    distances = np.full(

        N,

        np.inf,

    )


    distances[source] = 0


    queue = [source]


    queue_index = 0


    while queue_index < len(queue):


        current = queue[

            queue_index

        ]


        queue_index += 1


        for target in (

            outgoing_connections[current]

        ):


            if np.isinf(

                distances[target]

            ):


                distances[target] = (

                    distances[current]

                    + 1

                )


                queue.append(

                    target

                )


    return distances


# ============================================================
# GLOBAL PATH METRICS
# ============================================================

def calculate_path_metrics(

    outgoing_connections,

):

    N = len(

        outgoing_connections

    )


    path_lengths = []

    inverse_distances = []


    for source in range(N):


        distances = (

            directed_shortest_paths(

                outgoing_connections,

                source,

            )

        )


        for target in range(N):


            if source == target:

                continue


            distance = (

                distances[target]

            )


            if np.isfinite(distance):


                path_lengths.append(

                    distance

                )


                inverse_distances.append(

                    1.0 / distance

                )


            else:


                inverse_distances.append(

                    0.0

                )


    mean_path_length = float(

        np.mean(

            path_lengths

        )

    )


    global_efficiency = float(

        np.mean(

            inverse_distances

        )

    )


    return (

        mean_path_length,

        global_efficiency,

    )


# ============================================================
# STIMULUS PATH METRICS
# ============================================================

def stimulus_path_metrics(

    outgoing_connections,

    stimulus_neuron,

):


    distances = (

        directed_shortest_paths(

            outgoing_connections,

            stimulus_neuron,

        )

    )


    finite_distances = distances[

        np.isfinite(distances)

    ]


    finite_distances = (

        finite_distances[

            finite_distances > 0

        ]

    )


    if len(finite_distances) == 0:


        return (

            np.nan,

            np.nan,

        )


    mean_distance = float(

        np.mean(

            finite_distances

        )

    )


    max_distance = float(

        np.max(

            finite_distances

        )

    )


    return (

        mean_distance,

        max_distance,

    )


# ============================================================
# RECIPROCAL SHORTCUTS
# ============================================================

def count_reciprocal_shortcuts(

    shortcuts,

):


    shortcut_set = set(

        shortcuts

    )


    reciprocal_count = 0


    for source, target in shortcuts:


        reverse_edge = (

            target,

            source,

        )


        if reverse_edge in shortcut_set:


            if source < target:


                reciprocal_count += 1


    return reciprocal_count


# ============================================================
# EXTRACT TOPOLOGY FEATURES
# ============================================================

def extract_topology_features(

    network,

    shortcuts,

    stimulus_neuron,

):


    N = len(network)


    # --------------------------------------------------------
    # SHORTCUT LENGTHS
    # --------------------------------------------------------

    shortcut_lengths = [

        circular_distance(

            source,

            target,

            N,

        )

        for source, target

        in shortcuts

    ]


    # --------------------------------------------------------
    # SHORTCUT SOURCES
    # --------------------------------------------------------

    shortcut_sources = [

        source

        for source, target

        in shortcuts

    ]


    # --------------------------------------------------------
    # SHORTCUT TARGETS
    # --------------------------------------------------------

    shortcut_targets = [

        target

        for source, target

        in shortcuts

    ]


    # --------------------------------------------------------
    # DISTANCE OF SOURCES FROM STIMULUS
    # --------------------------------------------------------

    source_distances = [

        circular_distance(

            stimulus_neuron,

            source,

            N,

        )

        for source

        in shortcut_sources

    ]


    # --------------------------------------------------------
    # DISTANCE OF TARGETS FROM STIMULUS
    # --------------------------------------------------------

    target_distances = [

        circular_distance(

            stimulus_neuron,

            target,

            N,

        )

        for target

        in shortcut_targets

    ]


    # --------------------------------------------------------
    # DEGREE STATISTICS
    # --------------------------------------------------------

    out_degrees = np.array(

        [

            len(targets)

            for targets

            in network

        ],

        dtype=float,

    )


    in_degrees = np.zeros(

        N,

        dtype=float,

    )


    for source in range(N):


        for target in network[source]:


            in_degrees[target] += 1


    # --------------------------------------------------------
    # GLOBAL PATH METRICS
    # --------------------------------------------------------

    (

        mean_path_length,

        global_efficiency,

    ) = calculate_path_metrics(

        network

    )


    # --------------------------------------------------------
    # STIMULUS PATH METRICS
    # --------------------------------------------------------

    (

        mean_stimulus_path,

        max_stimulus_path,

    ) = stimulus_path_metrics(

        network,

        stimulus_neuron,

    )


    # --------------------------------------------------------
    # RETURN FEATURES
    # --------------------------------------------------------

    return {


        "number_of_shortcuts":

            len(shortcuts),


        "mean_shortcut_length":

            float(

                np.mean(

                    shortcut_lengths

                )

            ),


        "std_shortcut_length":

            float(

                np.std(

                    shortcut_lengths

                )

            ),


        "max_shortcut_length":

            float(

                np.max(

                    shortcut_lengths

                )

            ),


        "unique_shortcut_sources":

            len(

                set(

                    shortcut_sources

                )

            ),


        "unique_shortcut_targets":

            len(

                set(

                    shortcut_targets

                )

            ),


        "mean_source_distance_from_stimulus":

            float(

                np.mean(

                    source_distances

                )

            ),


        "min_source_distance_from_stimulus":

            float(

                np.min(

                    source_distances

                )

            ),


        "mean_target_distance_from_stimulus":

            float(

                np.mean(

                    target_distances

                )

            ),


        "min_target_distance_from_stimulus":

            float(

                np.min(

                    target_distances

                )

            ),


        "std_out_degree":

            float(

                np.std(

                    out_degrees

                )

            ),


        "max_out_degree":

            float(

                np.max(

                    out_degrees

                )

            ),


        "std_in_degree":

            float(

                np.std(

                    in_degrees

                )

            ),


        "max_in_degree":

            float(

                np.max(

                    in_degrees

                )

            ),


        "reciprocal_shortcuts":

            count_reciprocal_shortcuts(

                shortcuts

            ),


        "mean_path_length":

            mean_path_length,


        "global_efficiency":

            global_efficiency,


        "mean_distance_from_stimulus":

            mean_stimulus_path,


        "max_distance_from_stimulus":

            max_stimulus_path,

    }


# ============================================================
# HEADER
# ============================================================

print("=" * 80)


print(

    "PHASE 7: TOPOLOGY-OUTCOME CORRELATION"

)


print("=" * 80)


# ============================================================
# LOAD PHASE 6 RESULTS
# ============================================================

all_phase6_results = read_csv(

    PHASE6_ALL_FILE

)


probability_results = read_csv(

    PHASE6_PROBABILITY_FILE

)


# ============================================================
# SELECT TRANSITION p
# ============================================================

if MANUAL_P is not None:


    selected_p = float(

        MANUAL_P

    )


    selection_method = (

        "MANUAL"

    )


else:


    mixed_p_values = []


    for row in probability_results:


        p = float(

            row["p"]

        )


        probability_success = float(

            row[

                "probability_success"

            ]

        )


        if (

            probability_success > 0.0

            and

            probability_success < 1.0

        ):


            distance_from_half = abs(

                probability_success

                - 0.5

            )


            mixed_p_values.append(

                (

                    distance_from_half,

                    p,

                    probability_success,

                )

            )


    if len(mixed_p_values) == 0:


        raise RuntimeError(

            "No transition region found.\n"

            "Phase 6 needs at least one p "

            "with both SUCCESS and FAILURE."

        )


    mixed_p_values.sort()


    (

        distance_from_half,

        selected_p,

        selected_probability,

    ) = mixed_p_values[0]


    selection_method = (

        "AUTOMATIC"

    )


# ============================================================
# PRINT SELECTED p
# ============================================================

print("\nSELECTED TRANSITION POINT")


print("-" * 50)


print(

    "Selection method =",

    selection_method,

)


print(

    "Selected p =",

    selected_p,

)


# ============================================================
# SELECT REALIZATIONS AT p
# ============================================================

selected_realizations = []


for row in all_phase6_results:


    row_p = float(

        row["p"]

    )


    if np.isclose(

        row_p,

        selected_p,

    ):


        selected_realizations.append(

            row

        )


# ============================================================
# COUNT OUTCOMES
# ============================================================

success_count = sum(

    row["status"] == "SUCCESS"

    for row

    in selected_realizations

)


failure_count = sum(

    row["status"] == "FAILURE"

    for row

    in selected_realizations

)


print(

    "Total realizations =",

    len(selected_realizations),

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
# VALIDATE MIXED OUTCOMES
# ============================================================

if (

    success_count == 0

    or

    failure_count == 0

):


    raise RuntimeError(

        "Selected p does not contain "

        "both SUCCESS and FAILURE."

    )


# ============================================================
# RECONSTRUCT NETWORKS
# ============================================================

print("\n")


print("=" * 80)


print(

    "EXTRACTING TOPOLOGY FEATURES"

)


print("=" * 80)


topology_results = []


for index, row in enumerate(

    selected_realizations

):


    seed = int(

        row["seed"]

    )


    status = (

        row["status"]

    )


    # --------------------------------------------------------
    # BINARY OUTCOME
    # --------------------------------------------------------

    if status == "SUCCESS":


        outcome = 1


    else:


        outcome = 0


    # --------------------------------------------------------
    # BUILD EXACT SAME RING
    # --------------------------------------------------------

    local_network = (

        build_ring_network(N)

    )


    # --------------------------------------------------------
    # RECREATE EXACT SAME SHORTCUTS
    # --------------------------------------------------------

    network, shortcuts = (

        add_random_shortcuts(

            outgoing_connections=

                local_network,

            p=selected_p,

            seed=seed,

        )

    )


    # --------------------------------------------------------
    # EXTRACT FEATURES
    # --------------------------------------------------------

    features = (

        extract_topology_features(

            network=

                network,

            shortcuts=

                shortcuts,

            stimulus_neuron=

                STIMULUS_NEURON,

        )

    )


    # --------------------------------------------------------
    # STORE RESULT
    # --------------------------------------------------------

    topology_row = {


        "p":

            selected_p,


        "seed":

            seed,


        "status":

            status,


        "outcome":

            outcome,


        **features,

    }


    topology_results.append(

        topology_row

    )


    # --------------------------------------------------------
    # PRINT PROGRESS
    # --------------------------------------------------------

    print(


        f"{index + 1:3d}/"

        f"{len(selected_realizations):3d} | "


        f"Seed {seed:3d} | "


        f"{status:7s} | "


        f"Shortcut length = "

        f"{features['mean_shortcut_length']:.2f} | "


        f"Path length = "

        f"{features['mean_path_length']:.3f} | "


        f"Efficiency = "

        f"{features['global_efficiency']:.3f}"

    )


# ============================================================
# SAVE TOPOLOGY FEATURES
# ============================================================

topology_file = (

    RESULTS_DIR

    / "phase7_topology_features.csv"

)


with open(

    topology_file,

    "w",

    newline="",

) as file:


    writer = csv.DictWriter(

        file,

        fieldnames=

            list(

                topology_results[0].keys()

            ),

    )


    writer.writeheader()


    writer.writerows(

        topology_results

    )


# ============================================================
# IDENTIFY FEATURE COLUMNS
# ============================================================

metadata_columns = {

    "p",

    "seed",

    "status",

    "outcome",

}


feature_names = [

    column

    for column

    in topology_results[0].keys()

    if column

    not in metadata_columns

]


# ============================================================
# CORRELATION WITH SUCCESS
# ============================================================

outcomes = np.array(

    [

        row["outcome"]

        for row

        in topology_results

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

            for row

            in topology_results

        ],

        dtype=float,

    )


    # --------------------------------------------------------
    # CONSTANT FEATURE
    # --------------------------------------------------------

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


# ============================================================
# SORT CORRELATIONS
# ============================================================

correlation_results.sort(

    key=lambda row:

        row["absolute_correlation"],

    reverse=True,

)


# ============================================================
# SAVE CORRELATIONS
# ============================================================

correlation_file = (

    RESULTS_DIR

    / "phase7_correlations.csv"

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
# SUCCESS VS FAILURE GROUP COMPARISON
# ============================================================

group_results = []


for feature in feature_names:


    success_values = np.array(

        [

            float(

                row[feature]

            )

            for row

            in topology_results

            if row["status"]

            == "SUCCESS"

        ]

    )


    failure_values = np.array(

        [

            float(

                row[feature]

            )

            for row

            in topology_results

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


# ============================================================
# SAVE GROUP COMPARISON
# ============================================================

group_file = (

    RESULTS_DIR

    / "phase7_group_comparison.csv"

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
# PRINT TOP CORRELATIONS
# ============================================================

print("\n")


print("=" * 80)


print(

    "TOP TOPOLOGY FEATURES CORRELATED WITH SUCCESS"

)


print("=" * 80)


for row in correlation_results[:10]:


    print(


        f"{row['feature']:40s} | "


        f"r = "


        f"{row['correlation_with_success']:+.3f}"

    )


# ============================================================
# PLOT TOP CORRELATIONS
# ============================================================

top_results = (

    correlation_results[:10]

)


plot_features = [

    row["feature"]

    for row

    in top_results

]


plot_correlations = [

    row["correlation_with_success"]

    for row

    in top_results

]


y_positions = np.arange(

    len(plot_features)

)


plt.figure(

    figsize=(10, 7)

)


plt.barh(

    y_positions,

    plot_correlations,

)


plt.yticks(

    y_positions,

    plot_features,

)


plt.axvline(

    0.0,

    linewidth=1,

)


plt.xlabel(

    "Correlation with propagation success"

)


plt.title(

    f"Topology Features vs Propagation Outcome\n"

    f"p = {selected_p:.2f}"

)


plt.gca().invert_yaxis()


plt.tight_layout()


figure_file = (

    RESULTS_DIR

    / "phase7_topology_correlations.png"

)


plt.savefig(

    figure_file,

    dpi=300,

    bbox_inches="tight",

)


plt.show()


# ============================================================
# VALIDATION
# ============================================================

print("\n")


print("=" * 80)


print(

    "PHASE 7 VALIDATION"

)


print("=" * 80)


if (

    len(topology_results)

    == len(selected_realizations)

    and

    success_count > 0

    and

    failure_count > 0

):


    print("PASSED")


    print(

        "Exact Phase 6 networks were reconstructed."

    )


    print(

        "Both SUCCESS and FAILURE networks were analyzed."

    )


else:


    print("FAILED")


# ============================================================
# OUTPUT FILES
# ============================================================

print("\n")


print("=" * 80)


print("RESULTS SAVED")


print("=" * 80)


print(

    "\nTopology features:"

)


print(

    topology_file

)


print(

    "\nCorrelations:"

)


print(

    correlation_file

)


print(

    "\nGroup comparison:"

)


print(

    group_file

)


print(

    "\nFigure:"

)


print(

    figure_file

)


print("\n")


print("=" * 80)


print("PHASE 7 COMPLETE")


print("=" * 80)