import numpy as np

class SimpleEKF:
    def __init__(self, q_capacity, r0):
        self.q = q_capacity  # battery capacity (Coulomb)
        self.r0 = r0

        # State: SOC
        self.x = np.array([0.9])  # initial SOC

        # Covariance
        self.P = np.array([[1e-4]])

        # Noise
        self.Q = np.array([[1e-6]])  # process noise
        self.R = np.array([[1e-3]])  # measurement noise

    def predict(self, current, dt):
        # State prediction (Coulomb counting)
        self.x = self.x - (current * dt) / self.q

        # Jacobian = 1 (linear approx)
        F = np.array([[1]])

        # Covariance prediction
        self.P = F @ self.P @ F.T + self.Q

    def update(self, voltage_measured, ocv_function):
        # Predicted voltage
        soc = self.x[0]
        v_pred = ocv_function(np.array([soc]))[0] - self.r0 * 0

        # Measurement Jacobian (approx derivative)
        H = np.array([[1.0]])  # simplified

        # Innovation
        y = voltage_measured - v_pred

        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)

        # Update state
        self.x = self.x + K @ y

        # Update covariance
        I = np.eye(1)
        self.P = (I - K @ H) @ self.P

    def get_soc(self):
        return self.x[0]
