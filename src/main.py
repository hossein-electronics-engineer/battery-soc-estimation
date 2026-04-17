import os
import numpy as np
import matplotlib.pyplot as plt
from ekf_soc import SimpleEKF


def ocv_from_soc(soc: np.ndarray) -> np.ndarray:
    """
    Simple approximate OCV-SOC relationship for demonstration purposes.
    soc must be in [0, 1].
    """
    soc = np.clip(soc, 0.0, 1.0)
    return 3.0 + 1.2 * soc + 0.1 * np.sin(2 * np.pi * soc)


def generate_current_profile(t: np.ndarray) -> np.ndarray:
    """
    Create a simple piecewise current profile.
    Positive current = discharge
    Negative current = charge
    """
    current = np.zeros_like(t)

    current[(t >= 50) & (t < 250)] = 2.0
    current[(t >= 300) & (t < 500)] = 1.0
    current[(t >= 600) & (t < 750)] = -1.5
    current[(t >= 800) & (t < 1000)] = 2.5

    return current


def simulate_battery():
    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    # Simulation settings
    dt = 1.0
    t_end = 1200
    t = np.arange(0, t_end + dt, dt)

    # Battery parameters
    q_ah = 2.3
    q_coulomb = q_ah * 3600.0

    r0 = 0.05
    r1 = 0.02
    c1 = 2000.0
    tau1 = r1 * c1

    # Initial conditions
    soc = np.zeros_like(t)
    v_rc = np.zeros_like(t)
    v_terminal = np.zeros_like(t)
    ocv = np.zeros_like(t)

    soc[0] = 0.9
    current = generate_current_profile(t)
    ocv[0] = ocv_from_soc(np.array([soc[0]]))[0]
    v_terminal[0] = ocv[0] - current[0] * r0 - v_rc[0]

    # Discrete-time simulation
    for k in range(1, len(t)):
        # SOC update using coulomb counting
        soc[k] = soc[k - 1] - (current[k - 1] * dt) / q_coulomb
        soc[k] = np.clip(soc[k], 0.0, 1.0)

        # RC voltage update
        alpha = np.exp(-dt / tau1)
        v_rc[k] = alpha * v_rc[k - 1] + r1 * (1 - alpha) * current[k - 1]

        # OCV from SOC
        ocv[k] = ocv_from_soc(np.array([soc[k]]))[0]

        # Terminal voltage
        v_terminal[k] = ocv[k] - current[k] * r0 - v_rc[k]

    return t, current, soc, ocv, v_rc, v_terminal, q_coulomb, r0


def estimate_soc_with_ekf(t, current, voltage_measured, q_coulomb, r0):
    dt = t[1] - t[0]
    ekf = SimpleEKF(q_capacity=q_coulomb, r0=r0)

    soc_ekf = np.zeros_like(t)
    soc_ekf[0] = ekf.get_soc()

    for k in range(1, len(t)):
        ekf.predict(current=current[k - 1], dt=dt)
        ekf.update(
            voltage_measured=voltage_measured[k],
            current=current[k],
            ocv_function=ocv_from_soc
        )
        soc_ekf[k] = ekf.get_soc()

    return soc_ekf


def save_results(t, current, soc, soc_ekf, ocv, v_rc, v_terminal):
    data = np.column_stack((t, current, soc, soc_ekf, ocv, v_rc, v_terminal))
    header = "time_s,current_A,soc_true,soc_ekf,ocv_V,v_rc_V,v_terminal_V"
    np.savetxt("results/simulation_results.csv", data, delimiter=",", header=header, comments="")


def plot_results(t, current, soc, soc_ekf, ocv, v_terminal):
    plt.figure(figsize=(10, 4))
    plt.plot(t, current)
    plt.xlabel("Time [s]")
    plt.ylabel("Current [A]")
    plt.title("Battery Current Profile")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/current_profile.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(t, soc, label="True SOC")
    plt.plot(t, soc_ekf, label="EKF Estimated SOC", linestyle="--")
    plt.xlabel("Time [s]")
    plt.ylabel("SOC [-]")
    plt.title("SOC Comparison: True vs EKF")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/soc_ekf_comparison.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(t, ocv, label="OCV")
    plt.plot(t, v_terminal, label="Terminal Voltage")
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.title("Battery Voltage Response")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/voltage_response.png", dpi=200)
    plt.close()


def main():
    t, current, soc, ocv, v_rc, v_terminal, q_coulomb, r0 = simulate_battery()

    soc_ekf = estimate_soc_with_ekf(
        t=t,
        current=current,
        voltage_measured=v_terminal,
        q_coulomb=q_coulomb,
        r0=r0
    )

    save_results(t, current, soc, soc_ekf, ocv, v_rc, v_terminal)
    plot_results(t, current, soc, soc_ekf, ocv, v_terminal)

    print("Simulation completed successfully.")
    print("Results saved in: results/")
    print("Figures saved in: figures/")


if __name__ == "__main__":
    main()
