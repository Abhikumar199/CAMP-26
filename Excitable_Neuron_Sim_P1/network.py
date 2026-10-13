"""
network.py

Network construction for the Roxin, Riecke & Solla (2004) model.

Phase 2:
    Regular 1D ring only.
    No long-range shortcuts yet.
"""


def build_ring_network(N):
    """
    Build a one-dimensional ring of N neurons.

    Each neuron sends excitatory connections to:
        - its left neighbor
        - its right neighbor

    Example for N = 5:

        0 <-> 1 <-> 2 <-> 3 <-> 4
        ^                           |
        |___________________________|

    Parameters
    ----------
    N : int
        Number of neurons.

    Returns
    -------
    outgoing_connections : list of lists

        outgoing_connections[j] contains all neurons
        that receive a spike when neuron j fires.
    """

    if N < 3:
        raise ValueError(
            "A ring network requires at least 3 neurons."
        )

    outgoing_connections = [[] for _ in range(N)]

    for neuron in range(N):

        left_neighbor = (neuron - 1) % N
        right_neighbor = (neuron + 1) % N

        outgoing_connections[neuron].append(left_neighbor)
        outgoing_connections[neuron].append(right_neighbor)

    return outgoing_connections


def print_network(outgoing_connections):
    """
    Print the outgoing connections of every neuron.

    Useful only for debugging small networks.
    """

    print("\nNETWORK CONNECTIONS")
    print("-" * 40)

    for neuron, targets in enumerate(outgoing_connections):

        print(
            f"Neuron {neuron} -> {targets}"
        )


def validate_ring_network(outgoing_connections):
    """
    Check that the network has the expected ring structure.

    Every neuron must have exactly:
        - one left neighbor
        - one right neighbor
    """

    N = len(outgoing_connections)

    for neuron in range(N):

        expected_left = (neuron - 1) % N
        expected_right = (neuron + 1) % N

        actual_targets = set(
            outgoing_connections[neuron]
        )

        expected_targets = {
            expected_left,
            expected_right,
        }

        if actual_targets != expected_targets:

            raise ValueError(
                f"Neuron {neuron} has incorrect "
                f"connections.\n"
                f"Expected: {expected_targets}\n"
                f"Found: {actual_targets}"
            )

    print("\nRing network validation PASSED.")

    print(
        f"N = {N} neurons"
    )

    print(
        f"Directed local edges = {2 * N}"
    )

    print(
        "Every neuron has 2 outgoing local connections."
    )


if __name__ == "__main__":

    # Small network only for testing
    N = 10

    network = build_ring_network(N)

    print_network(network)

    validate_ring_network(network)



# Phase 3

import numpy as np


def add_random_shortcuts(
    outgoing_connections,
    p,
    seed=None,
):
    """
    Add p*N random directed long-range shortcuts.

    Local nearest-neighbor connections are preserved.

    Parameters
    ----------
    outgoing_connections : list of lists
        Existing ring network.

    p : float
        Shortcut density.

    seed : int or None
        Random seed.

    Returns
    -------
    small_world_network : list of lists
        Ring + shortcuts.

    shortcuts : list of tuples
        Added directed edges:
        (source, target)
    """

    if p < 0:
        raise ValueError("p must be >= 0")

    N = len(outgoing_connections)

    rng = np.random.default_rng(seed)

    # Copy the original ring
    small_world_network = [
        list(targets)
        for targets in outgoing_connections
    ]

    n_shortcuts = int(round(p * N))

    shortcuts = []

    while len(shortcuts) < n_shortcuts:

        source = int(rng.integers(0, N))
        target = int(rng.integers(0, N))

        # No self-connections
        if source == target:
            continue

        # Do not duplicate any existing edge
        if target in small_world_network[source]:
            continue

        small_world_network[source].append(target)

        shortcuts.append(
            (source, target)
        )

    return small_world_network, shortcuts

def validate_small_world_network(
    local_network,
    small_world_network,
    shortcuts,
    p,
):
    """
    Validate the small-world network.
    """

    N = len(local_network)

    expected_shortcuts = int(round(p * N))

    # Check shortcut number
    assert len(shortcuts) == expected_shortcuts

    # Check all local edges still exist
    for source in range(N):

        for target in local_network[source]:

            assert (
                target
                in small_world_network[source]
            )

    # Check no self-connections
    for source, target in shortcuts:

        assert source != target

    # Check no duplicate shortcuts
    assert len(shortcuts) == len(set(shortcuts))

    local_edges = sum(
        len(targets)
        for targets in local_network
    )

    total_edges = sum(
        len(targets)
        for targets in small_world_network
    )

    print("\nSMALL-WORLD VALIDATION PASSED.")
    print("-" * 40)

    print("N =", N)
    print("p =", p)

    print(
        "Local directed edges =",
        local_edges
    )

    print(
        "Expected shortcuts =",
        expected_shortcuts
    )

    print(
        "Actual shortcuts =",
        len(shortcuts)
    )

    print(
        "Total directed edges =",
        total_edges
    )