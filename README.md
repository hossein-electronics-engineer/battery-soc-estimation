# 🔋 Battery SOC Estimation using Equivalent Circuit Models, EKF, and Embedded Implementation

## 📌 Overview

This project presents a model-based approach for estimating the **State of Charge (SOC)** of a lithium-ion battery using:

* A **first-order equivalent circuit model (1RC)**
* An **Extended Kalman Filter (EKF)** for SOC estimation
* A lightweight **embedded-oriented implementation**
* A **C-based firmware-style implementation**
* **Python vs C validation** of the estimator

The project demonstrates a complete workflow from battery simulation to embedded-friendly implementation and cross-validation.

---

## 🎯 Objective

* Simulate battery voltage and current behavior under dynamic load conditions
* Estimate SOC using Coulomb counting and EKF
* Compare **true SOC** and **estimated SOC**
* Develop a lightweight embedded-style estimator
* Translate the estimator into C for firmware-oriented deployment
* Validate the C implementation against the Python reference

---

## ⚙️ Methodology

### 1. Battery Modeling

* First-order RC equivalent circuit model
* Nonlinear OCV-SOC relationship

### 2. Python Simulation

* Time-domain current profile
* Terminal voltage response
* SOC propagation using current integration

### 3. EKF-Based SOC Estimation

* Prediction step using system dynamics
* Measurement update using terminal voltage
* Numerical approximation of the OCV derivative

### 4. Embedded-Oriented Implementation

* Step-based estimator update
* Lightweight structure for real-time use
* Reduced computational complexity

### 5. C Firmware-Style Implementation

* Struct-based estimator state
* EKF logic implemented in C
* Test execution on desktop compiler environment

### 6. Validation

* Python EKF output compared with C EKF output
* Matching results confirm correct translation of the estimator logic

---

## 📊 Example Results

### 🔹 Current Profile

![Current](figures/current_profile.png)

### 🔹 SOC Comparison (True vs Python EKF)

![SOC EKF](figures/soc_ekf_comparison.png)

### 🔹 Voltage Response

![Voltage](figures/voltage_response.png)

### 🔹 Embedded-Oriented SOC Comparison

![Embedded SOC](figures/soc_embedded_comparison.png)

### 🔹 Python vs C Validation

![Python vs C Validation](figures/python_c_validation.png)

---

## 📁 Project Structure

```text
battery-soc-estimation/
│
├── src/
│   ├── main.py
│   ├── ekf_soc.py
│   ├── embedded_soc_step.py
│   ├── test_embedded_soc.py
│   └── compare_results.py
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

```bash
pip install numpy matplotlib pandas
```

Run main simulation:

```bash
python src/main.py
```

Run embedded-style simulation:

```bash
python src/test_embedded_soc.py
```

Run Python vs C comparison:

```bash
python src/compare_results.py
```

---

### C Version

Compile:

```bash
gcc main.c ekf_soc.c -o ekf_test -lm
```

Run:

```bash
./ekf_test
```

---

## 📈 Output

The project generates:

* Current profile plot
* Voltage response plot
* SOC comparison between true SOC and Python EKF
* Embedded-style SOC comparison
* Python vs C validation plot
* CSV output files for analysis

---

## ✅ Validation Summary

The final comparison shows that the **C implementation closely matches the Python EKF reference**, confirming that the SOC estimation logic was correctly translated into a firmware-style implementation.

This makes the project suitable as a bridge between:

* simulation and estimation research
* embedded implementation
* future deployment on microcontrollers

---

## 🚀 Features

* Physics-based battery modeling
* EKF-based SOC estimation
* Embedded-oriented algorithm design
* C firmware-style implementation
* Python vs C validation workflow

---

## 🔧 Future Work

* Tune EKF parameters (`Q`, `R`)
* Include temperature effects
* Improve the battery model (e.g. 2RC model)
* Validate against real battery datasets
* Deploy on STM32 / Arduino
* Explore fixed-point implementation for embedded targets

---

## 🧠 Key Takeaway

This project demonstrates how **model-based battery estimation** can be developed in Python, adapted for embedded-oriented execution, translated into C, and validated across implementations.

---

## 👤 Author

Hossein Electronics Engineer
