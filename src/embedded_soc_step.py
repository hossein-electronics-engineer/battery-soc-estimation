import numpy as np


def ocv_from_soc_scalar(soc: float) -> float:
    soc = max(0.0, min(1.0, soc))
    return 3.0 + 1.2 * soc + 0.1 * np.sin(2 * np.pi * soc)


class EmbeddedSOCEstimator:
    def __init__(self, q_capacity_coulomb: float, r0: float):
        self.q = q_capacity_coulomb
        self.r0 = r0

        self.soc = 0.9
        self.P = 1e-4
        self.Q = 1e-6
        self.R = 1e-3

    def predict(self, current: float, dt: float) -> None:
        self.soc = self.soc - (current * dt) / self.q
        self.soc = max(0.0, min(1.0, self.soc))
        self.P = self.P + self.Q

    def update(self, voltage_measured: float, current: float) -> None:
        soc = self.soc
        v_pred = ocv_from_soc_scalar(soc) - current * self.r0

        eps = 1e-5
        soc_plus = max(0.0, min(1.0, soc + eps))
        soc_minus = max(0.0, min(1.0, soc - eps))

        d_ocv = (
            ocv_from_soc_scalar(soc_plus) - ocv_from_soc_scalar(soc_minus)
        ) / (soc_plus - soc_minus + 1e-12)

        H = d_ocv
        y = voltage_measured - v_pred
        S = H * self.P * H + self.R
        K = (self.P * H) / S

        self.soc = self.soc + K * y
        self.soc = max(0.0, min(1.0, self.soc))

        self.P = (1.0 - K * H) * self.P

    def step(self, current: float, voltage_measured: float, dt: float) -> float:
        self.predict(current, dt)
        self.update(voltage_measured, current)
        return self.soc
