# Pybricks Multi-Program Tape Controller for ATUM (Atumated tape collecting ultramicrotomy)

This project implements a multi-program control system for the LEGO® PrimeHub (LEGO Education SPIKE Prime / Mindstorms Robot Inventor) using the Pybricks MicroPython API.  
It provides three motor-based control programs for tape movement and winding mechanics: Collection, Tension, and Rewind.

---

## Features

- Interactive menu system using hub buttons or force sensor fallback.
- Three programmable modes:
  1. Collection Mode — Moves tape segments when a red color is detected. Red colored sticker or similar should be attached to the sample holder at an appropriate position.
  2. Tension Mode — Maintains tape tension at constant speed.
  3. Rewind Mode — Rewinds tape at controlled speed.
- Dynamic display icons for C, T, and R menu entries.
- Smart tape radius estimation based on reel geometry and gear ratios.
- Force sensor-based start and exit control.
- Error fallback for button API issues.

---

## Hardware Setup

| Component | Port | Notes |
|------------|------|-------|
| Motor B | B | Counterclockwise direction |
| Motor D | D | Counterclockwise direction |
| Color Sensor | F | Detects red markers |
| Force Sensor | E | Used for start/exit/menu fallback |

---

## Configuration Parameters

| Parameter | Description | Default |
|------------|-------------|----------|
| `TAPE_THICKNESS` | Thickness of tape layer (mm) | 0.05 |
| `REEL_START_RADIUS_D` | Starting radius of motor D reel (mm) | 20.5 |
| `REEL_START_RADIUS_B` | Starting radius of motor B reel (mm) | 29.0 |
| `GEAR_RATIO_D` | Gear ratio for motor D | 9 |
| `GEAR_RATIO_B` | Gear ratio for motor B | 3 |

---

## Installation and Setup

To run this program on your LEGO PrimeHub, you need to install **Pybricks firmware** and the **Pybricks Code editor**.

### 1. Install Pybricks Firmware
1. Visit the official Pybricks website: [https://pybricks.com](https://pybricks.com)
2. Open the **Pybricks Code** web app in Google Chrome or Microsoft Edge:  
   [https://code.pybricks.com](https://code.pybricks.com)
3. Connect your LEGO PrimeHub via USB to your computer.
4. In the Pybricks web app, click the **Firmware** tab and follow the on-screen instructions to install the firmware on your hub.
5. Wait until the installation finishes and your hub restarts.

### 2. Load the Script
1. In the Pybricks Code editor, create a new project.
2. Copy and paste the contents of the provided script (`ATUM_tape_collector_control.py`) into the editor. Measure your tape reel diameters (including the tape on the reel) and adjust the variables in script.
3. Click the **Run** button to download and execute the program on your hub.
4. After loading the script to your hub, it will be acessible without connection to your computer.

---

## Running the Program

1. Upload the script to your Pybricks environment.
2. Run the program on your PrimeHub.
3. Use the menu to select a mode:
   - Use the force sensor to cycle/select. Long press (>3s selects subprocess, short press cycles through options)

---

## Program Descriptions

### 1. Collection Program
- Moves a fixed tape segment whenever a red color is detected.
- Adjustable parameters for movement time, delay, and overshoot.
- Displays event count on the hub. Top two rows indicate ones, rows 3 and 4 indicate tens and last rows indicate hundreds.

### 2. Tension Program
- Use prior to collection mode to set the correct tape tension.
- Runs until the force sensor is pressed again to stop.

### 3. Rewind Program
- Rewinds the tape back onto the lower reel. Mostly for testing purposes, to not have to manually rewind tape to the bottom reel.
- Controlled, consistent rewind motion.

---

## Internal Functions

| Function | Purpose |
|-----------|----------|
| `estimate_radius()` | Estimates changing reel radius as tape wraps. |
| `wait_for_force_start()` | Waits for the user to press force sensor to start. |
| `check_force_exit()` | Detects exit condition via force sensor. |

---

## Notes

- The menu system automatically returns after each program finishes.
- The force sensor can fully replace hub buttons for accessibility or hardware issues.
- Color detection relies on HSV thresholds for red (H < 30° or H > 330°).

---

## File Info

- Filename: `ATUM_tape_collector_control.py`
- Language: Python (Pybricks MicroPython)
- Compatible with: LEGO® PrimeHub (SPIKE Prime / Mindstorms Robot Inventor)

---

## Author

Created by Georg Kislinger, Deutsches Zentrum für Neurodegenerative Erkrankungen (DZNE).

---

## License

This script is provided for educational and research purposes.  
Free to use and modify with attribution.
