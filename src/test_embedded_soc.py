import os
import numpy as np
import matplotlib.pyplot as plt

from embedded_soc_step import EmbeddedSOCEstimator


def ocv_from_soc(soc):
    soc = np.clip(soc, 0.0, 1.0)
    return 3.0 + 1.2 * soc + 0.1 * np.sin(2 * np.pi * soc)


def generate_current_profile(t):
    current = np.zeros_like(t)
    current[(t >= 50) & (t < 250)] = 2.0
    current[(t >= 300) & (t < 500)] = 1.0
    current[(t >= 600) & (t < 750)] = -1.5
    current[(t >= 800) & (t < 1000)] = 2.5
    return current


def simulate_reference():
    dt = 1.0
    t_end = 1200
    t = np.arange(0, t_end + dt, dt)

    q_ah = 2.3
    q_coulomb = q_ah * 3600.0

    r0 = 0.05
    r1 = 0.02
    c1 = 2000.0
    tau1 = r1 * c1

    soc = np.zeros_like(t)
    v_rc = np.zeros_like(t)
    v_terminal = np.zeros_like(t)
    ocv = np.zeros_like(t)

    soc[0] = 0.9
    current = generate_current_profile(t)
    ocv[0] = ocv_from_soc(np.array([soc[0]]))[0]
    v_terminal[0] = ocv[0] - current[0] * r0 - v_rc[0]

    for k in range(1, len(t)):
        soc[k] = soc[k - 1] - (current[k - 1] * dt) / q_coulomb
        soc[k] = np.clip(soc[k], 0.0, 1.0)

        alpha = np.exp(-dt / tau1)
        v_rc[k] = alpha * v_rc[k - 1] + r1 * (1 - alpha) * current[k - 1]

        ocv[k] = ocv_from_soc(np.array([soc[k]]))[0]
        v_terminal[k] = ocv[k] - current[k] * r0 - v_rc[k]

    return t, current, soc, v_terminal, q_coulomb, r0


def main():
    os.makedirs("figures", exist_ok=True)

    t, current, soc_true, v_terminal, q_coulomb, r0 = simulate_reference()

    estimator = EmbeddedSOCEstimator(q_capacity_coulomb=q_coulomb, r0=r0)

    soc_embedded = np.zeros_like(t)
    soc_embedded[0] = estimator.soc

    dt = t[1] - t[0]

    for k in range(1, len(t)):
        soc_embedded[k] = estimator.step(
            current=float(current[k]),
            voltage_measured=float(v_terminal[k]),
            dt=float(dt)
        )

    plt.figure(figsize=(10, 4))
    plt.plot(t, soc_true, label="True SOC")
    plt.plot(t, soc_embedded, label="Embedded-style EKF", linestyle="--")
    plt.xlabel("Time [s]")
    plt.ylabel("SOC [-]")
    plt.title("SOC Comparison: True vs Embedded-style EKF")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/soc_embedded_comparison.png", dpi=200)
    plt.close()

    print("Embedded-style SOC estimation completed.")
    print("Figure saved: figures/soc_embedded_comparison.png")


if __name__ == "__main__":
    main()
