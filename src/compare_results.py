import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

py_data = pd.read_csv("results/simulation_results.csv")
c_data = pd.read_csv("c_version/c_output.csv")

soc_true = py_data["soc_true"].to_numpy()
soc_python = py_data["soc_ekf"].to_numpy()
soc_c = c_data["C_SOC"].to_numpy()

n = min(len(soc_true), len(soc_python), len(soc_c))
time = np.arange(n)

soc_true = soc_true[:n]
soc_python = soc_python[:n]
soc_c = soc_c[:n]

plt.figure(figsize=(10, 5))
plt.plot(time, soc_true, label="True SOC", linewidth=2)
plt.plot(time, soc_python, "--", label="Python EKF")
plt.plot(time, soc_c, ":", label="C EKF")

plt.xlabel("Step")
plt.ylabel("SOC")
plt.title("SOC Comparison: Python vs C")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

error = np.abs(soc_python - soc_c)
print("Max difference:", np.max(error))
print("Mean difference:", np.mean(error))

print("Max difference:", np.max(error))
print("Mean difference:", np.mean(error))
