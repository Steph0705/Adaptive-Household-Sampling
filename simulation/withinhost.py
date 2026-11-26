"""WITHIN-HOST VIRAL LOAD CURVE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The curve is the truth. The limit of detection (LOD) is not used here.
The LOD belongs to the observation step.
"""

import tomllib
from dataclasses import dataclass
from pathlib import Path

import numpy as np

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "withinhost.toml"


@dataclass(frozen=True)
class Trajectory:
    """Piecewise-linear log10 viral-load curve for one variant."""
    vl_peak: float       # log10 copies/mL
    growth_rate: float   # log10 copies/mL per day
    decline_rate: float  # log10 copies/mL per day
    floor: float = 0.0   # log10 copies/mL at infection and at clearance

    def __post_init__(self):
        if self.vl_peak <= self.floor:
            raise ValueError("vl_peak must be above floor")
        if self.growth_rate <= 0 or self.decline_rate <= 0:
            raise ValueError("growth_rate and decline_rate must be positive")

    @property
    def t_peak(self):
        """Time to peak, t_p (days after infection)."""
        return (self.vl_peak - self.floor) / self.growth_rate

    @property
    def t_clear(self):
        """Time to clearance, t_c (days after infection)."""
        return self.t_peak + (self.vl_peak - self.floor) / self.decline_rate

    @property
    def area(self):
        """A_L: area under log10VL from tau = 0 to t_c."""
        return 0.5 * self.t_clear * (self.vl_peak + self.floor)

    def log10_vl(self, tau):
        """log10 viral load at infection age tau (days).

        Gives floor for tau < 0 and tau > t_c.
        If floor is ever above 0, transmission.py must still set the
        rate to 0 outside 0 <= tau <= t_c.
        """
        tau = np.asarray(tau, dtype=float)
        rise = self.floor + self.growth_rate * tau
        fall = self.vl_peak - self.decline_rate * (tau - self.t_peak)
        vl = np.where(tau <= self.t_peak, rise, fall)
        # handles tau < 0, tau > t_c, and rounding at t_c.
        return np.maximum(vl, self.floor)


def load_trajectory(variant, path=CONFIG_PATH):
    """Read one [variant.<name>] table from config/withinhost.toml."""
    with open(path, "rb") as f:
        variants = tomllib.load(f)["variant"]
    if variant not in variants:
        raise KeyError(f"Unknown variant {variant!r}. Options: {sorted(variants)}")
    return Trajectory(**variants[variant])
