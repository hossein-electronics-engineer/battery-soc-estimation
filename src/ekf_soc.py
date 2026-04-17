import numpy as np


class SimpleEKF:
    def __init__(self, q_capacity, r0):
        self.q = q_capacity
        self.r0 = r0

        # State: SOC
        self.x = np.array([0.9], dtype=float)

        # Covariance
        self.P = np.array([[1e-4]], dtype=float)

        # Process and measurement noise
        self.Q = np.array([[1e-6]], dtype=float)
        self.R = np.array([[1e-3]], dtype=float)

    def predict(self, current, dt):
        # SOC prediction from current integration
        self.x[0] = self.x[0] - (current * dt) / self.q
        self.x[0] = np.clip(self.x[0], 0.0, 1.0)

        F = np.array([[1.0]])
        self.P = F @ self.P @ F.T + self.Q

    def update(self, voltage_measured, current, ocv_function):
        soc = self.x[0]

        # Predicted terminal voltage
        v_pred = ocv_function(np.array([soc]))[0] - current * self.r0

        # Numerical derivative dOCV/dSOC
        eps = 1e-5
        soc_plus = np.clip(soc + eps, 0.0, 1.0)
        soc_minus = np.clip(soc - eps, 0.0, 1.0)
        d_ocv = (
            ocv_function(np.array([soc_plus]))[0]
            - ocv_function(np.array([soc_minus]))[0]
        ) / (soc_plus - soc_minus + 1e-12)

        H = np.array([[d_ocv]])

        y = np.array([[voltage_measured - v_pred]])
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)

        self.x = self.x + (K @ y).flatten()
        self.x[0] = np.clip(self.x[0], 0.0, 1.0)

        I = np.eye(1)
        self.P = (I - K @ H) @ self.P

    def get_soc(self):
        return self.x[0]
