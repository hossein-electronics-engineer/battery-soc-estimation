# 🔋 Battery SOC Estimation using Equivalent Circuit Models, EKF, and Embedded Implementation

## 📌 Overview

This project presents a model-based approach for estimating the **State of Charge (SOC)** of a lithium-ion battery using:

* A **First-order Equivalent Circuit Model (RC model)**
* An **Extended Kalman Filter (EKF)** for state estimation
* A lightweight **embedded-oriented implementation**
* A **C-based firmware-style implementation** for microcontroller deployment

The project demonstrates the full workflow from simulation to embedded-ready algorithms.

---

## 🎯 Objective

* Simulate battery behavior under dynamic load conditions
* Estimate SOC using Coulomb counting and EKF
* Compare **true SOC vs estimated SOC**
* Develop a **real-time embedded-friendly estimator**
* Translate the algorithm into **C for firmware use**

---

## ⚙️ Methodology

### 1. Battery Modeling

* First-order RC equivalent circuit
* Nonlinear OCV-SOC relationship

### 2. Simulation

* Time-domain current profile
* Voltage response computation

### 3. State Estimation (EKF)

* Prediction based on system model
* Measurement update using voltage
* Nonlinear handling via numerical derivative

### 4. Embedded-Oriented Implementation

* Step-by-step execution (real-time style)
* Lightweight computation
* Suitable for MCU deployment

### 5. C Implementation

* Firmware-style EKF logic
* Struct-based state handling
* Ready for microcontroller integration

---

## 📊 Example Results

### 🔹 Current Profile

![Current](figures/current_profile.png)

### 🔹 SOC Comparison (True vs EKF)

![SOC EKF](figures/soc_ekf_comparison.png)

### 🔹 Voltage Response

![Voltage](figures/voltage_response.png)

### 🔹 Embedded SOC Comparison

![Embedded SOC](figures/soc_embedded_comparison.png)

---

## 📁 Project Structure

```id="8d8ejp"
battery-soc-estimation/
│
├── src/
│   ├── main.py
│   ├── ekf_soc.py
│   ├── embedded_soc_step.py
│   └── test_embedded_soc.py
│
├── c_version/
│   ├── ekf_soc.h
│   ├── ekf_soc.c
│   └── main.c
│
├── data/
├── results/
├── figures/
│
├── README.md
└── requirements.txt
```

---

## ▶️ How to Run

### Python Version

Install dependencies:

```bash id="t6c5wp"
pip install numpy matplotlib
```

Run main simulation:

```bash id="8y0h7g"
python src/main.py
```

Run embedded-style simulation:

```bash id="9r2bzj"
python src/test_embedded_soc.py
```

---

### C Version (Optional)

Compile:

```bash id="o6w3q9"
gcc main.c ekf_soc.c -o ekf_test -lm
```

Run:

```bash id="e8h0c2"
./ekf_test
```

---

## 📈 Output

The project generates:

* SOC estimation (true vs EKF)
* Embedded-style SOC estimation
* Voltage response
* Current profile
* CSV results for analysis

---

## 🚀 Features

* Physics-based battery model
* EKF-based SOC estimation
* Embedded-oriented algorithm design
* C firmware-style implementation
* Visualization of estimation accuracy

---

## 🔧 Future Work

* Tune EKF parameters (Q, R)
* Include temperature effects
* Extend to higher-order battery models (2RC)
* Validate with real-world datasets
* Deploy on STM32 / Arduino

---

## 🧠 Key Takeaway

This project demonstrates how **model-based estimation + EKF** can be transformed into an **embedded-ready algorithm**, bridging the gap between simulation and real-world implementation.

---

## 👤 Author

Hossein Electronics Engineer

