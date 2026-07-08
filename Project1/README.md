# Self-Sustained Activity in Small-World Networks of Excitable Neurons

A computational neuroscience project investigating how network topology, shortcut density, network size, and neuronal excitability influence the emergence of persistent collective activity in networks of excitable neurons.

This project qualitatively reproduces and extends the computational experiments from the study **“Self-Sustained Activity in a Small-World Network of Excitable Neurons.”**

## Objective

The central research question is:

> **Under what structural and dynamical conditions can a brief local stimulus generate long-lasting activity in a network of excitable neurons?**

The project investigates:

- Local wave propagation
- Small-world network formation
- Persistent neuronal activity
- Failure and success of activity propagation
- Probability of persistent activity
- Effects of network size
- Effects of shortcut density
- Topology–dynamics relationships
- Population firing-rate dynamics
- Single-neuron excitability
- Extensions beyond the original experiments

---

## Core Model

The system consists of `N` excitable neurons initially arranged in a local ring network.

Random long-range connections are then added to create a small-world-like network.

The network therefore contains:

1. **Local connections** for wave propagation
2. **Long-range shortcuts** for activity reinjection

A brief stimulus is applied to one neuron.

The main question is whether the resulting activity:

- dies out quickly, or
- continues circulating through the network as persistent activity

---

## Main Parameters

| Parameter         | Meaning                         |
| ----------------- | ------------------------------- |
| `N`             | Number of neurons               |
| `p`             | Shortcut density                |
| `I_ext`         | External input/current          |
| `g_syn`         | Synaptic coupling strength      |
| `tau_m`         | Membrane time constant          |
| `tau_D`         | Synaptic transmission delay     |
| `dt`            | Numerical integration time step |
| `t_max`         | Simulation end time             |
| `stimulus_time` | Time of initial stimulation     |

A commonly used paper-style parameter set is:

```text
N       = 1000
I_ext   = 0.85
g_syn   = 0.20
tau_m   = 10.0
tau_D   = 1.0
p       = 0.10
```

---

## Project Structure

```text
Project1/
│
├── config.py
├── network.py
├── neuron.py
├── simulator.py
│
├── phase_2_local_network.py
├── phase_3_small_world_network.py
├── phase_4_persistent_activity.py
├── phase_5_failure_classifier.py
├── phase_6_probability_failure.py
├── phase_7_topology_correlation.py
├── phase_8_shortcut_orientation.py
├── phase_9_dynamic_shortcut_activation.py
├── phase_10_benchmark_N2000.py
├── phase_11_N2000_time_horizon_control.py
├── phase_12_N2000_failure_probability.py
├── phase_13_multiN_failure_probability.py
├── phase_14_duration_vs_N.py
├── phase_15_paper_raster_firing_rate.py
├── phase_17_firing_rate_vs_clustering.py
├── PHASE_18_Firing_rate_vs_density.py
├── phase_19_all_handwritten_experiments.py
├── phase_20_single_neuron_FI_curve.py
├── phase_21_firing_rate_vs_p_multi_Iext.py
│
├── figures/
├── results/
└── README.md
```

---

# Experimental Phases

## Phase 2 — Local Network Wave Propagation

**File:** `phase_2_local_network.py`

### Objective

Construct a purely local ring network and determine whether a brief stimulus produces a travelling wave of neuronal activity.

### Main Idea

Local connectivity allows activity to propagate spatially through neighbouring neurons. However, without long-range connections, the activity eventually disappears.

---

## Phase 3 — Small-World Network

**File:** `phase_3_small_world_network.py`

### Objective

Add random long-range shortcuts to the local ring network and study their effect on activity propagation.

The network contains:

```text
Local propagation
        +
Long-range shortcuts
        ↓
Possible activity reinjection
```

Different random network realizations can produce very different dynamical outcomes.

---

## Phase 4 — Persistent Activity

**File:** `phase_4_persistent_activity.py`

### Objective

Identify network realizations in which activity persists for long periods.

Two main outcomes are observed.

### Failure

```text
Stimulus
   ↓
Wave propagation
   ↓
Activity disappears
```

### Success

```text
Stimulus
   ↓
Wave propagation
   ↓
Shortcut activation
   ↓
Activity reinjection
   ↓
Repeated propagation
   ↓
Persistent activity
```

---

## Phase 5 — Failure vs Success Classification

**File:** `phase_5_failure_classifier.py`

### Objective

Automatically classify each simulation as:

- **Failure**
- **Success**

The classification is based on whether network activity survives sufficiently long after the initial stimulus.

---

## Phase 6 — Probability of Failure

**File:** `phase_6_probability_failure.py`

### Objective

Estimate the probability that network activity fails for a given set of parameters.

For multiple random network realizations:

\[
P_}
===

\frac{\text{Number of failed realizations}}
{\text{Total number of realizations}}
\]

and:

\[
P_}
===

1-P_{\mathrm{failure}}
\]

---

## Phase 7 — Topology–Dynamics Correlation

**File:** `phase_7_topology_correlation.py`

### Objective

Investigate which structural properties of a random shortcut network are associated with persistent activity.

This phase explores whether network topology can explain why some random realizations succeed while others fail.

---

## Phase 8 — Shortcut Orientation

**File:** `phase_8_shortcut_orientation.py`

### Objective

Study whether the direction and arrangement of shortcuts influence activity propagation and persistence.

Not all shortcuts are equally useful. A shortcut contributes to persistent activity only when it is activated at the appropriate time and delivers excitation to a region capable of responding.

---

## Phase 9 — Dynamic Shortcut Activation

**File:** `phase_9_dynamic_shortcut_activation.py`

### Objective

Examine which shortcuts are actually activated during network dynamics.

This distinguishes between:

- **Structural shortcuts** — connections present in the network
- **Dynamically active shortcuts** — connections that actually transmit activity during the simulation

A network may contain many shortcuts while only a subset contributes to persistent activity.

---

## Phase 10 — Large-N Benchmark

**File:** `phase_10_benchmark_N2000.py`

### Objective

Test computational performance and network dynamics for:

\[
N=2000
\]

This phase evaluates whether larger neuronal networks can be simulated efficiently.

---

## Phase 11 — Time-Horizon Control

**File:** `phase_11_N2000_time_horizon_control.py`

### Objective

Determine whether apparent persistent activity is a genuine dynamical effect or simply a consequence of the simulation ending too early.

Longer simulation horizons are used as a control.

---

## Phase 12 — Failure Probability for N = 2000

**File:** `phase_12_N2000_failure_probability.py`

### Objective

Estimate the probability of failure for a larger network.

This experiment tests whether increasing network size makes persistent activity more reliable.

---

## Phase 13 — Failure Probability for Multiple Network Sizes

**File:** `phase_13_multiN_failure_probability.py`

### Objective

Study how persistence probability depends on network size.

Different values of `N` are compared under the same network and neuronal parameters.

The main question is:

> **Does increasing the number of neurons make persistent activity more likely?**

---

## Phase 14 — Activity Duration vs Network Size

**File:** `phase_14_duration_vs_N.py`

### Objective

Measure:

\[
\text{Activity duration}
\quad \text{vs} \quad
N
\]

at fixed shortcut density.

### Main Observation

The results reveal two major populations:

1. Networks in which activity dies early
2. Networks in which activity survives until the observation limit

This suggests that increasing network size primarily changes the **probability of entering persistent activity**, rather than smoothly increasing activity lifetime.

---

## Phase 15 — Paper-Style Raster and Population Firing Rate

**File:** `phase_15_paper_raster_firing_rate.py`

### Objective

Qualitatively reproduce the main structure of the paper figure.

The output contains two panels.

### Top Panel — Spike Raster

\[
\text{Neuron index vs time}
\]

The raster shows the spatiotemporal propagation of activity through the network.

### Bottom Panel — Population Firing Rate

\[
\text{Whole-network firing activity vs time}
\]

The firing-rate curve reveals periodic collective activity associated with travelling and recurrent excitation waves.

---

## Phase 17 — Firing Rate vs Clustering Coefficient

**File:** `phase_17_firing_rate_vs_clustering.py`

### Objective

Investigate whether whole-network firing activity is associated with network clustering.

For neuron \(i\), the local clustering coefficient is:

\[
C_i
===

\frac{2e_i}
{k_i(k_i-1)}
\]

where:

- \(k_i\) is the degree of neuron \(i\)
- \(e_i\) is the number of connections among its neighbours

The whole-network mean clustering coefficient is:

\[
C
=

\frac{1}{N}
\sum_{i=1}^{N} C_i
\]

with:

\[
0\leq C\leq1
\]

The final experiment compares:

\[
\text{Mean firing rate}
\quad \text{vs} \quad
C
\]

---

## Phase 18 — Firing Rate vs Shortcut Density

**File:** `PHASE_18_Firing_rate_vs_density.py`

### Objective

For a fixed network size:

\[
N=1000
\]

measure how whole-network firing activity changes as shortcut density varies:

\[
p:0\rightarrow1
\]

The mean firing rate is calculated as:

\[
\bar r
======

\frac{\text{Total post-stimulus spikes}}
{N(T_{\max}-T_{\mathrm{stimulus}})}
\]

The final graph is:

\[
\text{Mean whole-network firing rate}
\quad \text{vs} \quad
p
\]

The main research question is:

> **Is there an optimal shortcut-density regime for sustained collective activity?**

---

## Phase 19 — Combined Extended Experiments

**File:** `phase_19_all_handwritten_experiments.py`

### Objective

Combine additional topology and dynamics experiments developed during the project.

This phase extends the investigation beyond direct qualitative reproduction of the original study.

---

## Phase 20 — Single-Neuron F–I Curve

**File:** `phase_20_single_neuron_FI_curve.py`

### Objective

Characterize the intrinsic response of an individual neuron before interpreting whole-network behaviour.

The experiment measures:

\[
\text{Firing rate}
\quad \text{vs} \quad
I_{\mathrm{ext}}
\]

This produces the single-neuron frequency–current or **F–I curve**.

The purpose is to distinguish:

- single-neuron excitability
- collective network effects

---

## Phase 21 — Firing Rate vs Shortcut Density for Multiple External Inputs

**File:** `phase_21_firing_rate_vs_p_multi_Iext.py`

### Objective

Extend the firing-rate experiment by varying both:

\[
p
\]

and:

\[
I_{\mathrm{ext}}
\]

The final result compares multiple curves:

\[
\bar r(p)
\]

for different external-input levels.

This experiment determines whether the effect of network topology depends on neuronal excitability.

---

# Firing Rate Calculation

The mean whole-network firing rate is calculated as:

\[
\bar r
======

\frac{N_{\mathrm{spikes}}}
{N\,T_{\mathrm{analysis}}}
\]

where:

\[
T_}
===

T_
--

T_{\mathrm{stimulus}}
\]

For example, with:

```text
N = 1000
T_max = 400
Stimulus time = 10
```

the post-stimulus analysis duration is:

\[
400-10=390
\]

Therefore:

\[
\bar r
======

\frac{\text{Post-stimulus spike count}}
{1000\times390}
\]

The default unit is:

```text
spikes / neuron / model-time-unit
```

If one model time unit is explicitly interpreted as one millisecond, the value can be converted to Hz by multiplying by `1000`.

---

# Main Findings So Far

The simulations suggest that:

1. Local connectivity supports travelling excitation waves.
2. Local propagation alone is generally insufficient for indefinite activity.
3. Long-range shortcuts can reinject excitation into recovered network regions.
4. Persistent activity depends strongly on the exact random network realization.
5. Increasing network size increases the probability of persistent activity.
6. Activity duration often shows two regimes: rapid failure or persistence to the observation limit.
7. Intermediate shortcut densities may support stronger collective activity than very low or very high shortcut densities.
8. Static topology alone may not fully explain persistence.
9. Dynamically activated shortcuts may be more informative than the total number of structural shortcuts.
10. Network topology and neuronal excitability jointly control collective firing dynamics.

---

# Running the Project

Install the required packages:

```bash
pip install numpy matplotlib
```

Run any experiment independently:

```bash
python phase_4_persistent_activity.py
```

For the paper-style raster and firing-rate figure:

```bash
python phase_15_paper_raster_firing_rate.py
```

For firing rate vs shortcut density:

```bash
python PHASE_18_Firing_rate_vs_density.py
```

For the single-neuron F–I curve:

```bash
python phase_20_single_neuron_FI_curve.py
```

For firing rate vs shortcut density at multiple external inputs:

```bash
python phase_21_firing_rate_vs_p_multi_Iext.py
```

---

# Output

Generated numerical results are stored in:

```text
results/
```

Generated figures are stored in:

```text
figures/
```

Some experiments also create their own phase-specific output directories.

---

# Research Extensions

Possible future extensions include:

- Critical network-size estimation
- Finite-size scaling
- Transition boundaries in the \((N,p)\) parameter space
- Longer time-horizon controls
- Topology-conditioned persistence analysis
- Dynamically active shortcut networks
- Clustering and path-length analysis
- Firing-rate phase diagrams
- Multiple neuronal excitability regimes
- Comparison with alternative excitable-neuron models

---

# Scientific Scope

This repository is a computational exploration and qualitative extension of small-world excitable neuronal network dynamics.

The central goal is to understand:

> **How does network structure control the transition from transient travelling waves to self-sustained collective neuronal activity?**

---
