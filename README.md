# Pybricks Multi-Program Tape Controller for ATUM (Automated Tape Collecting Ultramicrotomy)

This project implements a multi-program control system for the LEGO® PrimeHub (LEGO Education SPIKE Prime / Mindstorms Robot Inventor) using the Pybricks MicroPython API.  
It provides three motor-based control programs for tape movement and winding mechanics: Collection, Tension, and Rewind.

---

## Features

- Interactive menu system using force sensor.
- Three programmable modes:
  1. Collection Mode — Moves tape segments when a red color is detected. Red colored sticker or similar should be attached to the sample holder at an appropriate position.
  2. Tension Mode — To set initial tape tension at constant speed.
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
| Force Sensor | E | Used for start/exit/menu |

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
4. After loading the script to your hub, it will be accessible without connection to your computer.

---

## Running the Program

1. Upload the script to your Pybricks environment.
2. Run the program on your PrimeHub.
3. Use the menu to select a mode:
   - Use the force sensor to cycle/select. Long press (>3s selects subprocess, short press cycles through options)

---

## Program Descriptions

### 1. Collection Program
- Moves tape a defined distance over a defined period of time whenever red color is detected.
- Adjustable parameters for movement time, delay, and overshoot.
- Displays event count on the hub. Top two rows indicate ones, rows 3 and 4 indicate tens and last rows indicate hundreds.

### 2. Tension Program
- Use prior to collection mode to set the correct tape tension.
- Runs until the force sensor is pressed again to stop.

### 3. Rewind Program
- Rewinds the tape back onto the lower reel. Mostly for testing purposes, to not have to manually rewind tape to the bottom reel.
- Controlled, consistent rewind motion.

---

## HOW TO OPERATE ATUM

### Before Starting
Place a red sticker on the sample holder in a way that it is detected during the cutting movement of the microtome arm. Avoid permanent detection.  
Eyeball this initially, then start PrimeHub and cycle to **C** and confirm by long press. Let the microtome arm 'cut' and check whether the collector moves the tape after each cut.  
Appropriate delay depends on the placement of the sticker; appropriate distance and time to run the distance depend on sectioning speed and blockface size.  
Exit **C (Collection mode)** by restarting the hub.

Measure your tape reel diameters and set them in the software. Standard values might work.  
If you are not happy with when the collector collects, you can set collection movement distance and delay to better coordinate it with your cutting process.  
If changes were or have to be made, reupload the changed script to the hub.

Now insert the knife into the system and adjust the tape arm so that it is approximately **1.5 sections (or blockface lengths)** away from the knife edge and fix it in place by tightening the collector arm screw.  
The arm with tape should be sufficiently submerged into the waterbath but not touch the knife edge or boat.

Start PrimeHub by pressing the main button. Once started, cycle through programs to reach **T**.  
Run the program until the tape is sufficiently taut (should not bend the plastic arm but should also not have visible slack).  
Exit **T** program by pressing the force sensor. Cycle to **C** and start collection. The counter will count how many sections were collected.

---

### Troubleshooting

#### Rainbow Sections
**Probable causes:**
1. Tape runs during the sectioning process and creates water disturbance.  
   **Solution:** Try to add delay to collect between sectioning or decrease/increase collection speed (reduce/increase time used to run tape the set distance) to make motor motion smoother.
2. Dull knife, too large blockface, collector too close to knife edge, or even touching the boat.

#### Sections Deformed (Squeezed Between Knife Edge and Collector)
**Probable cause:** Too little distance moved per collection event or collection not timed appropriately.  
**Solution:** Watch closely when the squeeze happens. If it happens during cutting, try to collect *while cutting* (in my test setup, disturbance was minimal).

#### Sections Float Away from Collector Arm
**Solutions:**
1. Move arm closer to knife edge or center it better.  
2. Collect with higher tape speed to create more pull in knife boat.  
3. Plasma discharge tape.

---

## Author

Created by Georg Kislinger, Deutsches Zentrum für Neurodegenerative Erkrankungen (DZNE).

---

## License

This script is provided for educational and research purposes.  
Free to use and modify with attribution.
