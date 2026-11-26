# Adaptive versus Static Household Sampling of SARS-CoV-2 Viral-Load Trajectories

Project code for a simulation study. This repository provides the pipeline to build a stochastic model of household outbreaks from a SARS-CoV-2 community infection, where each infected individual has a known viral load trajectory. These simulated household outbreaks are used to explore adaptive versus static sampling to construct viral load trajectories.

**STATUS: Within-household outbreak simulation in progress...**

## Stages of construction

| Stage | Description |
| ----- | ----------- |
|   1   | Within-household outbreak giving infectees a viral load trajectory - transmission is a time inhomogeneous Poisson process (TIPP) simulated by a thinning algorithm.
|   2   | Household-size distribution (ONS-CIS); ONS-CIS incidence data into community infection curve to seed index cases into households.
|   3   | Exploring parameters e.g. immunity, vaccination, sweeps of SAR, etc.
|   4   | Static, triggered, and adaptive sampling.

## Model in brief

- Each infected person in a household follows a piecewise-linear log<sub>10</sub> viral load curve. Inputs include: growth rate, decline rate, and peak viral load.
- The limit of detection (LOD) is not part of the curve. The viral load curve provides the truth, while the LOD will provide what can be observed from sampling.
- Transmission rate from person $`i`$ to housemate $`j`$, where $`\tau`$ is infection age:

```math
\lambda_{i \to j}(\tau) = \beta_w \log_{10} L(\tau)
```

- $`\beta_w`$ is set from a secondary attack rate (SAR) based on literature.
- Candidate events come from a thinning algorithm. Each acceptance test uses a new, independent random number.

## Set-up

Developed on Python 3.15.2.

1. Clone the repository:
   `git clone https://github.com/Steph0705/Adaptive-Household-Sampling.git`
2. Create a virtual environment in the project folder: `python -m venv .venv`
3. Activate it:
   - Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`
   - macOS/Linux: `source .venv/bin/activate`
4. Install the packages: `python -m pip install -r requirements.txt`

## Packages

| Package | Use |
| ------- | --- |
| numpy | Viral load curves, random numbers, simulation |
| matplotlib | Figures |
| pytest | Tests in `tests/` |

The exact versions are pinned in `requirements.txt`, and parameter files are read with Python's `tomllib`.

(TBC)

## Project layout

| Folder | Description |
| ------ | ----------- |
| config/ | contains parameters
| results/ | outputs
| scripts/ | points to run the model
| simulation/ | model functions/modules 
| tests/ | tests on model

The .py modules contained in simulation/ include the following:
- `withinhost.py`: Viral load trajectory built from growth rate, decline rate, and viral load peak. 
- `transmission.py`: Rate, $`\beta_w`$ calibration, and thinning loop.
- `households.py`: Distribution of households
- `seeding.py`: ONS-CIS community curve, seeding events of index cases into households.

## Reproducibility

- All parameters are in `config/` (`withinhost.toml`, `transmission.toml`, `run.toml`, TBC). No values are set in the code.
- One random seed (`config/run.toml`) creates one random number generator per run.
- Package versions are pinned in `requirements.txt` (see above).
- Outputs go to `results/`. This folder is not tracked by Git. Re-run the scripts to recreate it and store in own results folder.
- Run commands: TBC (added with `scripts/`).

## Sources
TBC