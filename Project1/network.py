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