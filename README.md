# Pybricks Multi-Program Tape Controller for ATUM (Automated Tape Collecting Ultramicrotomy)

This project implements a multi-program control system for the LEGO® PrimeHub (LEGO Education SPIKE Prime / Mindstorms Robot Inventor) using the Pybricks MicroPython API.  
It provides three motor-based control programs for tape movement and winding mechanics: Collection, Tension, and Rewind.

---

## Features

- Interactive menu system using force sensor to cycle through modes.
- Three programmable modes:
  1. Collection Mode — Moves tape segments when a red color is detected. Red colored sticker or similar should be attached to the sample holder at an appropriate position.
  2. Tension Mode — To set initial tape tension at constant speed.
  3. Rewind Mode — Rewinds tape at controlled speed.
- Dynamic display icons for C, T, and R menu entries.
- Smart tape radius estimation based on reel geometry and gear ratios.
- Force sensor-based start and exit control.

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
| `TAPE_THICKNESS` | Thickness of tape layer (mm) | 0.05 | Used to calculate necessary motor movements as tape is spooled from one reel to other|
| `REEL_START_RADIUS_D` | Starting radius of motor D reel (mm) | 20.5 | Empty (taking-) reel diameter |
| `REEL_START_RADIUS_B` | Starting radius of motor B reel (mm) | 29.0 | Full (giving-) reel radius|
| `TAPE_MM` | Amount of tape collected on red event | 10 | Amount of tape used to collect one section |
| `MOVE_TIME_MS` | Duration of tape collection on red event | 2000 | Duration of motors = ON after red event |
| `MOVE_DELAY_MS` | Delay of movement after red event | 200 | Delay between red detection and motor start |
| `GIVING_OVERSHOOT_MM` | Additional tape given by motor b | 0 | Can be used if tape is too tight after few collection event, can be negative to keep tape taut |
| `GEAR_RATIO_D` | Gear ratio for motor D | 9 | If setup changes, gear ratios can be adjusted |
| `GEAR_RATIO_B` | Gear ratio for motor B | 3 | If setup changes, gear ratios can be adjusted |

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
   - Use force sensor to exit any mode, e.g. if accidentally selected wrong mode.

---

## Program Descriptions

### 1. Collection Program
- Moves tape a defined distance whenever red color is detected.
- Adjustable parameters for movement time, delay, and overshoot. (See table with params)
- Displays event count on the hub. Top two rows indicate ones, rows 3 and 4 indicate tens and last rows indicate hundreds.

### 2. Tension Program
- Use prior to collection mode to set the correct tape tension.
- Runs until the force sensor is pressed again to stop.

### 3. Rewind Program
- Rewinds the tape back onto the lower reel. Mostly for testing purposes, to not have to manually rewind tape to the bottom reel.
- Controlled, consistent rewind motion.

---

## How to operate the Auto-Collector

### Before Starting

Follow these steps to prepare and start the ATUM system:

1. **Attach the Red Sticker**  
   Place a red sticker on the sample holder so that it is detected during the cutting movement of the microtome arm.  
   Avoid permanent detection — the sensor should only briefly detect red during each cutting cycle.

2. **Test Color Detection and Collection Trigger**  
   Eyeball the sticker placement, then start the PrimeHub.  
   Cycle through the menu to **C (Collection Mode)** and confirm by a long press on the force sensor.  
   Let the microtome arm perform a cut and verify that the collector moves the tape after each cut.  
   The appropriate **delay** depends on the sticker position; the **distance and time** to run depend on sectioning speed and blockface size.  
   To exit **C (Collection Mode)**, restart the hub or press sensor.

3. **Set Reel Parameters**  
   Measure your tape reel diameters and enter the values in the software. Standard values may already work well.  
   If you want to change when or how the collector moves, adjust the **collection distance** and **delay** parameters to better coordinate with your cutting process.  
   After modifying parameters, reupload the updated script to the hub.

4. **Insert the Knife and Adjust the Tape Arm**  
   Insert the knife into the ultramicrotome system.  
   Adjust the tape arm so that it is approximately **1.5 sections (or blockface lengths)** away from the knife edge.  
   Fix the arm in place by tightening the collector arm screw.  
   The tape should be **submerged in the waterbath** but must **not touch the knife edge or boat**.

5. **Start the PrimeHub and Tension the Tape**  
   Press the main button on the PrimeHub to start it.  
   Once the hub boots, cycle through the menu to reach **T (Tension Mode)**.  
   Run the program until the tape becomes taut — it should not bend the plastic arm but also must not show visible slack.  
   Stop the **Tension Mode** by pressing the force sensor.

6. **Begin Collection Mode**  
   Cycle to **C (Collection Mode)** again and start the program.  
   The display counter will increment with each collected section, allowing you to track progress in real time.


---

## Troubleshooting

### Rainbow Sections
**Probable causes:**
1. Tape runs during the sectioning process and creates water disturbance.  
   **Solution:** Try to add delay to collect between sectioning or decrease/increase collection speed (reduce/increase time used to run tape the set distance) to make motor motion smoother.
2. Dull knife, too large blockface, collector too close to knife edge, or even touching the boat.

### Sections Deformed (Squeezed Between Knife Edge and Collector)
**Probable cause:** Too little distance moved per collection event or collection not timed appropriately.  
**Solution:** Watch closely when the squeeze happens. If it happens during cutting, try to collect *while cutting* (in my test setup, disturbance was minimal).

### Sections Float Away from Collector Arm
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
