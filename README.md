# 🔋 Battery SOC Estimation using Equivalent Circuit Models and EKF

## 📌 Overview

This project presents a model-based approach for estimating the **State of Charge (SOC)** of a lithium-ion battery using:

* A simple **Equivalent Circuit Model (RC model)**
* An **Extended Kalman Filter (EKF)** for state estimation

The implementation demonstrates how battery behavior can be modeled and how SOC can be estimated in real time using system dynamics and measurement updates.

---

## 🎯 Objective

* Simulate battery voltage and current behavior
* Estimate SOC using a physics-based model
* Apply EKF to improve SOC estimation accuracy
* Compare **true SOC vs estimated SOC**

---

## ⚙️ Methodology

### 1. Battery Modeling

* First-order RC equivalent circuit model
* OCV-SOC nonlinear relationship

### 2. Simulation

* Time-based current profile (charge/discharge)
* Voltage response generation

### 3. State Estimation (EKF)

* Predict step based on system model
* Update step using voltage measurements
* Nonlinear measurement handling

---

## 📊 Example Results

### 🔹 Current Profile

![Current](figures/current_profile.png)

### 🔹 SOC Comparison (True vs EKF)

![SOC EKF](figures/soc_ekf_comparison.png)

### 🔹 Voltage Response

![Voltage](figures/voltage_response.png)

---

## 📁 Project Structure

```
battery-soc-estimation/
│
├── src/
│   ├── main.py          # Simulation and plotting
│   └── ekf_soc.py      # EKF implementation
│
├── data/               # Input data (optional)
├── results/            # Simulation outputs (CSV)
├── figures/            # Generated plots
│
├── README.md
└── requirements.txt
```

---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install numpy matplotlib
```

### 2. Run the simulation

```bash
python src/main.py
```

---

## 📈 Output

The simulation generates:

* SOC profile (true vs estimated)
* Battery voltage response
* Current profile
* CSV file with all results

---

## 🚀 Features

* Physics-based battery modeling
* Nonlinear OCV-SOC relationship
* EKF-based SOC estimation
* Visualization of estimation performance

---

## 🔧 Future Work

* Tune EKF parameters (Q, R)
* Add temperature effects
* Improve battery model (2RC model)
* Implement in embedded systems (C / MCU)

---

## 🧠 Key Takeaway

This project shows how **model-based estimation + EKF** can be used to track battery SOC in a realistic and practical way.

---

## 👤 Author

Hossein Electronics Engineer

