# 🏠 Smart Home Automation System

This project is a Python-based simulation of a smart home automation system that controls and monitors IoT devices like smart lights, thermostats, and security cameras. It features a graphical user interface built with Tkinter and supports both **manual control** and **randomized automation**.

## 📌 Features

- **Device Simulation**: Emulates Smart Lights, Thermostats, and Security Cameras.
- **Manual vs. Random Control**: Toggle between hands-on device control and random automation.
- **Automation Rules**: Define logic-based automation (e.g., turn on lights if motion is detected).
- **Dynamic UI**: Interactive GUI with sliders and buttons for controlling device state and behavior.
- **Threaded Updates**: Background loop updates device states and applies automation rules.

## 🧠 Technologies Used

- `Python`
- `Tkinter` – for GUI
- `Threading` – for real-time simulation loop
- `Random` – to simulate sensor input and motion detection

## 🔧 How It Works

- **Device Classes**: Includes `SmartLight`, `Thermostat`, and `SecurityCamera`, all inheriting from a common `SmartDevice` base.
- **Automation System**: Centralized controller for adding devices and automation rules.
- **Automation Rule Engine**: Each rule has a `condition` and an `action`. When the condition is met, the action is executed.
- **Dashboard**: Tkinter interface showing current device states, allowing manual interaction and rule creation.

## 🚀 Enhancements & Custom Logic

- Added a **toggle switch** to flip between manual and automated control modes.
- Implemented **sliders** for brightness (lights) and temperature (thermostats).
- Added **motion simulation** to security cameras.
- Designed a rule: **"Turn on lights when motion is detected"**.

## 🖥️ Getting Started

```bash
git clone https://github.com/sareh24/smart-home-automation.git
cd smart-home-automation
python smart-home-automation.py
