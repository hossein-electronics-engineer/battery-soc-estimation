import os
import numpy as np
import matplotlib.pyplot as plt
from ekf_soc import SimpleEKF


def ocv_from_soc(soc: np.ndarray) -> np.ndarray:
    soc = np.clip(soc, 0.0, 1.0)
    return 3.0 + 1.2 * soc + 0.1 * np.sin(2 * np.pi * soc)


def generate_current_profile(t: np.ndarray) -> np.ndarray:
    current = np.zeros_like(t)

    current[(t >= 50) & (t < 250)] = 2.0
    current[(t >= 300) & (t < 500)] = 1.0
    current[(t >= 600) & (t < 750)] = -1.5
    current[(t >= 800) & (t < 1000)] = 2.5

    return current


def simulate_battery():
    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

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
        v_rc[k] = alpha * v_rc[k - 1] + r1 * (1.0 - alpha) * current[k - 1]

        ocv[k] = ocv_from_soc(np.array([soc[k]]))[0]
        v_terminal[k] = ocv[k] - current[k] * r0 - v_rc[k]

    return t, current, soc, ocv, v_rc, v_terminal, q_coulomb, r0, r1, c1


def estimate_soc_with_2state_ekf(
    t,
    current,
    voltage_measured,
    q_coulomb,
    r0,
    r1,
    c1,
    q_noise_soc=1e-6,
    q_noise_vrc=1e-5,
    r_noise=1e-2
):
    dt = t[1] - t[0]

    ekf = SimpleEKF(
        q_capacity=q_coulomb,
        r0=r0,
        r1=r1,
        c1=c1,
        q_noise_soc=q_noise_soc,
        q_noise_vrc=q_noise_vrc,
        r_noise=r_noise
    )

    soc_ekf = np.zeros_like(t)
    vrc_ekf = np.zeros_like(t)

    soc_ekf[0] = ekf.get_soc()
    vrc_ekf[0] = ekf.get_vrc()

    for k in range(1, len(t)):
        ekf.predict(current=current[k - 1], dt=dt)
        ekf.update(
            voltage_measured=voltage_measured[k],
            current=current[k],
            ocv_function=ocv_from_soc
        )
        soc_ekf[k] = ekf.get_soc()
        vrc_ekf[k] = ekf.get_vrc()

    return soc_ekf, vrc_ekf


def save_results(t, current, soc, soc_ekf, v_rc, vrc_ekf, ocv, v_terminal):
    data = np.column_stack((t, current, soc, soc_ekf, v_rc, vrc_ekf, ocv, v_terminal))
    header = "time_s,current_A,soc_true,soc_ekf,vrc_true,vrc_ekf,ocv_V,v_terminal_V"
    np.savetxt("results/simulation_results.csv", data, delimiter=",", header=header, comments="")


def plot_base_results(t, current, ocv, v_terminal):
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


def plot_noisy_measurement(t, v_terminal, v_measured_noisy):
    plt.figure(figsize=(11, 4))
    plt.plot(t, v_terminal, label="Ideal Terminal Voltage")
    plt.plot(t, v_measured_noisy, label="Noisy Measured Voltage", alpha=0.7)
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.title("Measured Voltage with Noise")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/noisy_voltage_measurement.png", dpi=200)
    plt.close()


def plot_soc_comparison(t, soc_true, soc_ekf):
    plt.figure(figsize=(11, 5))
    plt.plot(t, soc_true, label="True SOC", linewidth=2)
    plt.plot(t, soc_ekf, "--", label="2-State EKF SOC")
    plt.xlabel("Time [s]")
    plt.ylabel("SOC [-]")
    plt.title("SOC Comparison: True vs 2-State EKF")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/soc_2state_ekf_comparison.png", dpi=200)
    plt.close()


def plot_vrc_comparison(t, vrc_true, vrc_ekf):
    plt.figure(figsize=(11, 5))
    plt.plot(t, vrc_true, label="True V_RC", linewidth=2)
    plt.plot(t, vrc_ekf, "--", label="Estimated V_RC")
    plt.xlabel("Time [s]")
    plt.ylabel("V_RC [V]")
    plt.title("V_RC Comparison: True vs 2-State EKF")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/vrc_2state_ekf_comparison.png", dpi=200)
    plt.close()


def plot_soc_error(t, soc_true, soc_ekf):
    error = soc_ekf - soc_true

    plt.figure(figsize=(11, 4))
    plt.plot(t, error, label="SOC Estimation Error")
    plt.axhline(0, color="black", linewidth=1)
    plt.xlabel("Time [s]")
    plt.ylabel("SOC Error")
    plt.title("2-State EKF SOC Error")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/soc_2state_ekf_error.png", dpi=200)
    plt.close()


def compute_metrics(soc_true, soc_est):
    error = soc_est - soc_true
    mae = np.mean(np.abs(error))
    rmse = np.sqrt(np.mean(error ** 2))
    return mae, rmse


def main():
    np.random.seed(42)

    t, current, soc, ocv, v_rc, v_terminal, q_coulomb, r0, r1, c1 = simulate_battery()

    # Noisy voltage measurement
    noise_std = 0.01
    noise = np.random.normal(0.0, noise_std, size=v_terminal.shape)
    v_measured_noisy = v_terminal + noise

    # Best tuning from previous stage
    q_noise_soc = 1e-6
    q_noise_vrc = 1e-5
    r_noise = 1e-2

    soc_ekf, vrc_ekf = estimate_soc_with_2state_ekf(
        t=t,
        current=current,
        voltage_measured=v_measured_noisy,
        q_coulomb=q_coulomb,
        r0=r0,
        r1=r1,
        c1=c1,
        q_noise_soc=q_noise_soc,
        q_noise_vrc=q_noise_vrc,
        r_noise=r_noise
    )

    save_results(t, current, soc, soc_ekf, v_rc, vrc_ekf, ocv, v_terminal)

    plot_base_results(t, current, ocv, v_terminal)
    plot_noisy_measurement(t, v_terminal, v_measured_noisy)
    plot_soc_comparison(t, soc, soc_ekf)
    plot_vrc_comparison(t, v_rc, vrc_ekf)
    plot_soc_error(t, soc, soc_ekf)

    mae, rmse = compute_metrics(soc, soc_ekf)

    print("2-State EKF simulation completed successfully.")
    print(f"MAE:  {mae:.6f}")
    print(f"RMSE: {rmse:.6f}")
    print("\nResults saved in: results/")
    print("Figures saved in: figures/")
    print("Generated figures:")
    print("- current_profile.png")
    print("- voltage_response.png")
    print("- noisy_voltage_measurement.png")
    print("- soc_2state_ekf_comparison.png")
    print("- vrc_2state_ekf_comparison.png")
    print("- soc_2state_ekf_error.png")


if __name__ == "__main__":
    main()
