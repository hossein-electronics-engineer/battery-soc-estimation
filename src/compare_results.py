import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


def compute_metrics(reference, estimate):
    error = estimate - reference
    mae = np.mean(np.abs(error))
    rmse = np.sqrt(np.mean(error ** 2))
    return mae, rmse


def main():
    os.makedirs("figures", exist_ok=True)

    # Python 2-state results
    py_data = pd.read_csv("results/simulation_results.csv")

    # C 2-state results
    c_data = pd.read_csv("c_version/c_output.csv")

    # Extract arrays
    soc_true = py_data["soc_true"].to_numpy()
    soc_python = py_data["soc_ekf"].to_numpy()
    vrc_true = py_data["vrc_true"].to_numpy()
    vrc_python = py_data["vrc_ekf"].to_numpy()

    soc_c = c_data["C_SOC"].to_numpy()
    vrc_c = c_data["C_VRC"].to_numpy()

    # Use common length
    n = min(
        len(soc_true),
        len(soc_python),
        len(vrc_true),
        len(vrc_python),
        len(soc_c),
        len(vrc_c)
    )

    t = np.arange(n)

    soc_true = soc_true[:n]
    soc_python = soc_python[:n]
    vrc_true = vrc_true[:n]
    vrc_python = vrc_python[:n]
    soc_c = soc_c[:n]
    vrc_c = vrc_c[:n]

    # =========================
    # Plot SOC validation
    # =========================
    plt.figure(figsize=(11, 5))
    plt.plot(t, soc_true, label="True SOC", linewidth=2)
    plt.plot(t, soc_python, "--", label="Python 2-State EKF")
    plt.plot(t, soc_c, ":", label="C 2-State EKF", linewidth=2)

    plt.xlabel("Step")
    plt.ylabel("SOC")
    plt.title("2-State EKF Validation: Python vs C (SOC)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("figures/python_c_2state_soc_validation.png", dpi=200)
    plt.close()

    # =========================
    # Plot VRC validation
    # =========================
    plt.figure(figsize=(11, 5))
    plt.plot(t, vrc_true, label="True V_RC", linewidth=2)
    plt.plot(t, vrc_python, "--", label="Python 2-State EKF")
    plt.plot(t, vrc_c, ":", label="C 2-State EKF", linewidth=2)

    plt.xlabel("Step")
    plt.ylabel("V_RC [V]")
    plt.title("2-State EKF Validation: Python vs C (V_RC)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("figures/python_c_2state_vrc_validation.png", dpi=200)
    plt.close()

    # =========================
    # Error plots
    # =========================
    soc_error = soc_python - soc_c
    vrc_error = vrc_python - vrc_c

    plt.figure(figsize=(11, 4))
    plt.plot(t, soc_error, label="SOC Error (Python - C)")
    plt.axhline(0, color="black", linewidth=1)
    plt.xlabel("Step")
    plt.ylabel("SOC Error")
    plt.title("Python vs C 2-State EKF Error (SOC)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("figures/python_c_2state_soc_error.png", dpi=200)
    plt.close()

    plt.figure(figsize=(11, 4))
    plt.plot(t, vrc_error, label="V_RC Error (Python - C)")
    plt.axhline(0, color="black", linewidth=1)
    plt.xlabel("Step")
    plt.ylabel("V_RC Error [V]")
    plt.title("Python vs C 2-State EKF Error (V_RC)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("figures/python_c_2state_vrc_error.png", dpi=200)
    plt.close()

    # Metrics
    soc_mae, soc_rmse = compute_metrics(soc_python, soc_c)
    vrc_mae, vrc_rmse = compute_metrics(vrc_python, vrc_c)

    print("2-State Python vs C validation completed.")
    print(f"SOC  -> MAE: {soc_mae:.8f}, RMSE: {soc_rmse:.8f}")
    print(f"V_RC -> MAE: {vrc_mae:.8f}, RMSE: {vrc_rmse:.8f}")
    print("\nGenerated figures:")
    print("- figures/python_c_2state_soc_validation.png")
    print("- figures/python_c_2state_vrc_validation.png")
    print("- figures/python_c_2state_soc_error.png")
    print("- figures/python_c_2state_vrc_error.png")


if __name__ == "__main__":
    main()
