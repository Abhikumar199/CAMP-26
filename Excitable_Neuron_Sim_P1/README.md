# Self-Sustained Activity in Small-World Networks of Excitable Neurons

A computational neuroscience simulation project exploring how network structure, shortcut density, network size, and neuronal excitability affect the emergence of persistent collective activity.

The experiments are inspired by the study **“Self-Sustained Activity in a Small-World Network of Excitable Neurons.”** The goal is to reproduce the qualitative dynamics and investigate additional topology–activity relationships.

## Research question

**When can a brief local stimulus trigger long-lasting activity in a network of excitable neurons?**

The project examines travelling excitation waves, small-world connectivity, persistence versus failure, firing-rate dynamics, network topology, and single-neuron excitability.

## Model overview

Neurons are arranged initially in a local ring. Additional long-range shortcuts can connect distant neurons. A stimulus is applied, and the simulator records spike times and neuron indices.

- **Local connections** support propagation between neighbouring neurons.
- **Long-range shortcuts** can reinject activity into other parts of the network.
- **Persistent activity** occurs when activity continues beyond the initial transient; in other realizations, activity dies out.

The model is a simplified integrate-and-fire network with delayed synaptic events.

## Parameters

| Parameter | Meaning |
|---|---|
| `N` | Number of neurons |
| `p` | Shortcut density/probability used by the network experiments |
| `I_ext` | External input |
| `g_syn` | Synaptic coupling strength |
| `tau_m` | Membrane time constant |
| `tau_D` | Synaptic transmission delay |
| `dt` | Integration time step |
| `t_max` | Simulation end time |
| `stimulus_time` | Time of the initial stimulus |

The baseline configuration in `config.py` defines `I_EXT = 0.85`, `G_SYN = 0.20`, `TAU_M = 10.0`, `TAU_D = 1.0`, `DT = 0.01`, and `T_MAX = 100.0`. Individual experiment scripts may override these values.

## Repository layout

This project lives in `Excitable_Neuron_Sim_P1/` within the repository.

```text
Excitable_Neuron_Sim_P1/
├── config.py
├── neuron.py
├── network.py
├── simulator.py
├── phase_1_neuron_characterization.py
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
├── figures/
│   └── NEURON/
│       └── Learn.ipynb
├── results/
└── README.md
```

The phase scripts are separate experiments. The shared modules provide model configuration, neuron updates, network construction, and simulation logic. The notebook under `figures/NEURON/` is retained for code-based exploration.

## Experimental phases

| Phase | Script | Focus |
|---|---|---|
| 1 | `phase_1_neuron_characterization.py` | Single-neuron response and characterization |
| 2 | `phase_2_local_network.py` | Wave propagation in a local ring |
| 3 | `phase_3_small_world_network.py` | Adding long-range shortcuts |
| 4 | `phase_4_persistent_activity.py` | Persistent activity versus activity failure |
| 5 | `phase_5_failure_classifier.py` | Classifying simulation outcomes |
| 6 | `phase_6_probability_failure.py` | Estimating failure probability across realizations |
| 7 | `phase_7_topology_correlation.py` | Network topology and activity outcomes |
| 8 | `phase_8_shortcut_orientation.py` | Influence of shortcut orientation |
| 9 | `phase_9_dynamic_shortcut_activation.py` | Which shortcuts are activated during dynamics |
| 10 | `phase_10_benchmark_N2000.py` | Benchmarking a network with 2,000 neurons |
| 11 | `phase_11_N2000_time_horizon_control.py` | Checking sensitivity to the simulation time horizon |
| 12 | `phase_12_N2000_failure_probability.py` | Failure probability for a large network |
| 13 | `phase_13_multiN_failure_probability.py` | Comparing multiple network sizes |
| 14 | `phase_14_duration_vs_N.py` | Activity duration versus network size |
| 15 | `phase_15_paper_raster_firing_rate.py` | Spike raster and population firing-rate plots |
| 17 | `phase_17_firing_rate_vs_clustering.py` | Firing rate versus clustering coefficient |
| 18 | `PHASE_18_Firing_rate_vs_density.py` | Firing rate versus shortcut density |
| 19 | `phase_19_all_handwritten_experiments.py` | Combined extended experiments |
| 20 | `phase_20_single_neuron_FI_curve.py` | Single-neuron frequency–current (F–I) curve |
| 21 | `phase_21_firing_rate_vs_p_multi_Iext.py` | Shortcut density across external-input levels |

Phase 16 is not present in the current script set.

## Installation

Use Python 3.10 or newer, then install the core dependencies:

```bash
python -m pip install numpy matplotlib
```

Some experiment scripts may require additional packages depending on the analyses they perform. Install any missing dependency reported by the specific script when running it.

## Running an experiment

From the repository root:

```bash
python Excitable_Neuron_Sim_P1/phase_4_persistent_activity.py
```

Or move into the project directory first:

```bash
cd Excitable_Neuron_Sim_P1
python phase_4_persistent_activity.py
```

Other useful entry points include:

```bash
python phase_15_paper_raster_firing_rate.py
python PHASE_18_Firing_rate_vs_density.py
python phase_20_single_neuron_FI_curve.py
python phase_21_firing_rate_vs_p_multi_Iext.py
```

Run each experiment independently and check its settings and output paths before launching large parameter sweeps.

## Firing-rate definition

For a post-stimulus analysis window, the mean firing rate per neuron is

\[
\bar r = \frac{N_{\mathrm{spikes}}}{N\,T_{\mathrm{analysis}}}
\]

where \(N_{\mathrm{spikes}}\) is the number of spikes counted in the analysis window, \(N\) is the number of neurons, and \(T_{\mathrm{analysis}}\) is the duration of that window. The unit is spikes per neuron per model-time-unit. Convert to hertz only when the model time unit is known to represent a millisecond.

For example, if the analysis starts at \(t_{\mathrm{stimulus}}\) and ends at \(t_{\max}\),

\[
T_{\mathrm{analysis}} = t_{\max} - t_{\mathrm{stimulus}}.
\]

## Outputs

- `figures/` — plots and figure-related files.
- `results/` — numerical results and experiment outputs.

Output filenames and subdirectories can vary by script.

## Interpreting the experiments

The project is designed to test hypotheses rather than assume one outcome for every network. Results can vary with random network realizations, model parameters, and simulation duration. The experiments investigate whether:

- local connectivity alone is sufficient for long-lasting activity;
- shortcuts change the likelihood of activity persistence;
- persistence probability depends on network size;
- structural shortcuts and dynamically activated shortcuts tell different stories;
- firing rate depends on shortcut density, clustering, and external input;
- single-neuron excitability helps explain collective network behaviour.

These are questions to evaluate from the generated results; conclusions should be reported with the relevant parameters, number of realizations, and simulation horizon.

## Scope and possible extensions

This repository is a computational exploration of excitable-neuron network dynamics. Potential extensions include finite-size scaling, persistence maps over \((N,p)\), longer time-horizon controls, topology-conditioned analysis, and comparisons with alternative neuronal models.
