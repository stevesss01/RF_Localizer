# RF Localizer

### Real-Time RF Signal Monitoring & Localization Prototype

> A low-cost embedded RF monitoring system that combines **Arduino, nRF24L01, serial data acquisition, signal processing, and a real-time Python visualization dashboard** to visualize RF activity and estimate source location.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat\&logo=python\&logoColor=white)](#)
[![Arduino](https://img.shields.io/badge/Arduino-Embedded-00979D?style=flat\&logo=arduino\&logoColor=white)](#)
[![PyQt5](https://img.shields.io/badge/PyQt5-GUI-41CD52?style=flat\&logo=qt\&logoColor=white)](#)
[![PyQtGraph](https://img.shields.io/badge/PyQtGraph-Visualization-orange?style=flat)](#)
[![RF](https://img.shields.io/badge/RF-2.4_GHz-blue?style=flat)](#)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](#)

---

## Overview

RF Localizer is an experimental RF monitoring and localization platform designed to demonstrate how wireless signal information can be acquired, processed, and transformed into an intuitive real-time visualization system.

The prototype combines a **two-node Arduino architecture** with nRF24L01 transceivers and a Python desktop dashboard.

Instead of presenting raw signal values alone, the system converts them into multiple visual representations:

* Real-time signal-strength graph
* RF waveform visualization
* Spatial heatmap
* Radar-style tracking display
* Estimated X/Y source coordinates
* Confidence indicator
* Live system-status telemetry

The project was designed with **modularity and future scalability** in mind, allowing the prototype to evolve toward multi-node localization and SDR-based RF analysis.

---

## Why This Project?

RF localization is relevant to several engineering domains including:

* Wireless communication
* Spectrum monitoring
* Interference analysis
* Security systems
* Asset tracking
* Drone detection
* RF research

Commercial RF monitoring systems can be expensive and complex. RF Localizer explores the underlying concepts using accessible embedded hardware and an open software stack.

---

# System Architecture

```text
                 RF LOCALIZER
                      │
          ┌───────────┴───────────┐
          │                       │
    TRANSMITTER NODE         RECEIVER NODE
          │                       │
      Arduino Uno             Arduino Uno
          │                       │
      nRF24L01  ───── RF ───── nRF24L01
                                  │
                                  │ Serial
                                  ▼
                         Python Processing
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
              Signal Analysis              Localization
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                       REAL-TIME DASHBOARD
                                  │
             ┌────────────────────┼───────────────────┐
             │                    │                   │
          Signal Graph         Heatmap             Radar
             │                    │                   │
             └────────────────────┼───────────────────┘
                                  │
                         Source Coordinates
```

---

# Key Features

### 01 — Real-Time Signal Monitoring

The dashboard continuously receives signal data and plots signal-strength variation over time.

### 02 — RF Activity Visualization

A dynamic waveform provides a visual representation of changing RF activity.

### 03 — Spatial Heatmap

Signal intensity is mapped onto a 2D grid to produce a visual representation of the estimated RF source region.

### 04 — Radar Tracking

A radar-style interface provides a directional visualization with:

* Multiple range rings
* Sweeping beam
* Target marker
* Target glow
* Continuous animation

### 05 — Source Localization

The system displays estimated source coordinates:

```text
X : 37
Y : 24
Confidence : 82%
```

### 06 — Live System Telemetry

The dashboard exposes:

```text
RF Link
Signal Level
Signal Quality
Frequency
Node Count
Tracking Status
System Uptime
```

---

# Hardware

| Component               | Quantity | Purpose                            |
| ----------------------- | -------: | ---------------------------------- |
| Arduino Uno             |        2 | Embedded processing / node control |
| nRF24L01 PA+LNA         |        2 | 2.4 GHz RF communication           |
| External Antenna        |        2 | RF transmission/reception          |
| Breadboard              |        2 | Hardware prototyping               |
| 10 µF Capacitor         |        2 | RF power-supply stabilization      |
| AMS1117 3.3 V Regulator |        2 | Stable RF-module supply            |
| Jumper Wires            |        — | Interconnections                   |

### nRF24L01 → Arduino Uno

| nRF24L01 | Arduino Uno   |
| -------- | ------------- |
| VCC      | 3.3V          |
| GND      | GND           |
| CE       | D9            |
| CSN      | D10           |
| SCK      | D13           |
| MOSI     | D11           |
| MISO     | D12           |
| IRQ      | Not connected |

A 10 µF capacitor is connected across **VCC and GND** near the RF module to help handle transient current demand and reduce supply fluctuations.

---

# Software Stack

### Embedded

* Arduino C/C++
* Arduino Uno
* nRF24L01

### Desktop Application

* Python
* PyQt5
* PyQtGraph
* NumPy
* PySerial

### Visualization

* Real-time line plotting
* 2D signal heatmap
* Radar visualization
* Animated RF waveform
* GUI telemetry

---

# Project Structure

```text
RF-Localizer
│
├── arduino/
│   ├── transmitter/
│   │   └── transmitter.ino
│   │
│   └── receiver/
│       └── receiver.ino
│
├── dashboard/
│   └── RF_Localizer_Pro_Final_V3.py
│
├── images/
│   ├── dashboard.png
│   ├── hardware.png
│   ├── transmitter.png
│   └── receiver.png
│
├── report/
│   └── RF_Localizer_Project_Report.pdf
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

# Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/RF-Localizer.git
cd RF-Localizer
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or:

```bash
pip install pyqt5 pyqtgraph pyserial numpy
```

## 3. Upload Arduino Code

Upload:

```text
arduino/transmitter/transmitter.ino
```

to the transmitter Arduino.

Upload:

```text
arduino/receiver/receiver.ino
```

to the receiver Arduino.

## 4. Configure Serial Port

Open:

```text
dashboard/RF_Localizer_Pro_Final_V3.py
```

and change:

```python
COM_PORT = "COM13"
```

to the serial port assigned to your Arduino.

## 5. Run

```bash
python dashboard/RF_Localizer_Pro_Final_V3.py
```

---

# Dashboard

Place your best dashboard screenshot here:

```markdown
![RF Localizer Dashboard](images/dashboard.png)
```

For the README, use the **cleanest full-screen screenshot** you have rather than several nearly identical screenshots.

---

# Engineering Concepts Demonstrated

This project brings together concepts from multiple engineering domains:

### Embedded Systems

Arduino-based node architecture and serial data acquisition.

### Wireless Communication

2.4 GHz RF communication using nRF24L01 transceivers.

### SPI Communication

The nRF24L01 interfaces with Arduino using SPI for data transfer and control.

### Signal Processing

Signal measurements are converted into time-series and spatial representations.

### Data Visualization

Real-time RF telemetry is transformed into graphs, heatmaps, and radar displays.

### Localization

Signal information is used to demonstrate the concept of estimating an RF source position.

---

# Localization Approach

The prototype demonstrates the fundamental idea of signal-strength-based localization.

Conceptually:

```text
Higher received signal strength
            ↓
      closer source

Lower received signal strength
            ↓
      farther source
```

For accurate real-world localization, multiple calibrated receiver nodes would be required.

The current visualization therefore represents a **localization prototype rather than a precision geolocation system**.

---

# Limitations

The current prototype has several deliberate limitations:

* The localization model is experimental.
* Accurate physical positioning requires calibrated RF measurements.
* A single receiver cannot provide precise 2D localization by itself.
* The nRF24L01 is not a general-purpose spectrum analyzer.
* It cannot independently classify arbitrary RF technologies such as Wi-Fi, Bluetooth, or cellular signals.

These limitations define the next stage of development rather than being hidden from the system design.

---

# Scalability & Future Development

The architecture is intentionally modular.

### Stage 1 — Current Prototype

```text
2 RF Nodes
     ↓
Signal Monitoring
     ↓
Visualization
```

### Stage 2 — Multi-Node Localization

```text
        RX 1
         \
          \
           SOURCE
          /     \
       RX 2     RX 3
```

Multiple receivers can provide measurements for triangulation and improved localization accuracy.

### Stage 3 — SDR Integration

An SDR-based receiver can extend the platform beyond a single RF protocol and enable broader spectrum observation.

Potential technologies include:

* Wi-Fi
* Bluetooth
* LoRa
* Remote-control signals
* Other ISM-band transmissions

### Stage 4 — Intelligent RF Classification

Machine-learning models could classify RF signatures and provide outputs such as:

```text
Signal Detected
      ↓
Feature Extraction
      ↓
ML Classifier
      ↓
Signal Classification
      ↓
Localization
```

### Stage 5 — Geographical RF Monitoring

Future versions could integrate:

* GPS
* Digital maps
* Multiple distributed receivers
* Cloud telemetry
* Historical RF datasets
* Automated anomaly detection

---

# Cost

The prototype was designed around low-cost and readily available components.

| Component Group            | Estimated Cost |
| -------------------------- | -------------: |
| Arduino boards             |         ₹1,000 |
| RF modules + antennas      |           ₹800 |
| Breadboards & wiring       |           ₹300 |
| Capacitors & regulation    |           ₹100 |
| Miscellaneous              |           ₹100 |
| **Approx. Prototype Cost** |     **₹2,300** |

Software tools used in the project are open-source.

---

# What I Learned

This project provided practical experience across the complete engineering pipeline:

```text
Hardware
   ↓
Embedded Programming
   ↓
RF Communication
   ↓
Serial Data Acquisition
   ↓
Data Processing
   ↓
Real-Time Visualization
   ↓
System-Level Integration
```

The project also highlighted an important engineering principle:

> A working prototype is only the first step; scalability, measurement accuracy, reliability, and system architecture determine whether it can evolve into a real-world solution.

---

# Future Vision

The long-term direction of RF Localizer is a **distributed RF sensing platform** capable of combining multiple receivers, spectrum analysis, signal classification, and geographical localization into a unified monitoring system.

The current prototype establishes the hardware and visualization foundation for that evolution.

---

# License

This project is released under the MIT License.

---

# Author

**Shyam Saha**

Electronics & Communication Engineering

---

### ⭐ If you found this project interesting, consider starring the repository.
