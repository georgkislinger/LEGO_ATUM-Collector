from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, ForceSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait, StopWatch

# === SETUP ===
hub = PrimeHub()
motor_b = Motor(Port.B, Direction.COUNTERCLOCKWISE)
motor_d = Motor(Port.D, Direction.COUNTERCLOCKWISE)
color_sensor = ColorSensor(Port.F)
force_sensor = ForceSensor(Port.E)
watch = StopWatch()

# === SHARED CONFIG ===
TAPE_THICKNESS = 0.1
REEL_START_RADIUS_D = 20.5
REEL_START_RADIUS_B = 25.0
GEAR_RATIO_D = 9
GEAR_RATIO_B = 3

# === DISPLAY PATTERNS ===
LETTER_C = [
    [100, 100, 100, 100, 100],
    [100,   0,   0,   0,   0],
    [100,   0,   0,   0,   0],
    [100,   0,   0,   0,   0],
    [100, 100, 100, 100, 100]
]

LETTER_T = [
    [100, 100, 100, 100, 100],
    [  0,   0, 100,   0,   0],
    [  0,   0, 100,   0,   0],
    [  0,   0, 100,   0,   0],
    [  0,   0, 100,   0,   0]
]

LETTER_R = [
    [100, 100, 100, 100,   0],
    [100,   0,   0,   0, 100],
    [100, 100, 100, 100,   0],
    [100,   0, 100,   0,   0],
    [100,   0,   0, 100,   0]
]

# === MENU SYSTEM ===
def show_menu():
    """Main program selection menu using hub buttons correctly"""
    current_program = 0  # 0=C, 1=T, 2=R
    programs = [LETTER_C, LETTER_T, LETTER_R]
    program_names = ["Collection", "Tension", "Rewind"]
    
    print("Menu: LEFT=prev, RIGHT=next, CENTER=select")
    
    while True:
        # Display current program letter
        hub.display.icon(programs[current_program])
        
        # Check each button individually
        try:
            if hub.buttons.left.pressed():
                current_program = (current_program - 1) % 3
                print(f"Selected: {program_names[current_program]}")
                wait(300)  # Debounce
                while hub.buttons.left.pressed():
                    wait(50)
                
            elif hub.buttons.right.pressed():
                current_program = (current_program + 1) % 3
                print(f"Selected: {program_names[current_program]}")
                wait(300)  # Debounce
                while hub.buttons.right.pressed():
                    wait(50)
                
            elif hub.buttons.center.pressed():
                print(f"Starting {program_names[current_program]} program...")
                wait(300)  # Debounce
                while hub.buttons.center.pressed():
                    wait(50)
                
                # Run selected program
                if current_program == 0:
                    run_collection_program()
                elif current_program == 1:
                    run_tension_program()
                elif current_program == 2:
                    run_rewind_program()
                    
                # Return to menu after program exits
                print("Returning to menu...")
                print("Menu: LEFT=prev, RIGHT=next, CENTER=select")
                
        except AttributeError:
            print("Button API error - using force sensor instead")
            return show_menu_force_sensor()
            
        wait(50)

def show_menu_force_sensor():
    """Fallback menu using force sensor if buttons don't work"""
    current_program = 0
    programs = [LETTER_C, LETTER_T, LETTER_R]
    program_names = ["Collection", "Tension", "Rewind"]
    
    print("Force sensor menu: Press to cycle, hold 2s to select")
    
    while True:
        hub.display.icon(programs[current_program])
        
        if force_sensor.pressed():
            start_time = 0
            while force_sensor.pressed():
                start_time += 50
                wait(50)
                if start_time >= 2000:  # 2 second hold
                    print(f"Starting {program_names[current_program]} program...")
                    
                    if current_program == 0:
                        run_collection_program()
                    elif current_program == 1:
                        run_tension_program()
                    elif current_program == 2:
                        run_rewind_program()
                        
                    print("Returning to menu...")
                    break
            
            if start_time < 2000:  # Short press - cycle programs
                current_program = (current_program + 1) % 3
                print(f"Selected: {program_names[current_program]}")
                wait(500)
        
        wait(50)

# === SHARED FUNCTIONS ===
def estimate_radius(motor_angle_deg, start_radius_mm):
    turns = motor_angle_deg / 360
    return start_radius_mm + TAPE_THICKNESS * turns

def wait_for_force_start():
    """Wait for force sensor press to start, release to continue"""
    print("Press force sensor to start...")
    while not force_sensor.pressed():
        wait(50)
    print("Starting...")
    while force_sensor.pressed():
        wait(50)

def check_force_exit():
    """Check if force sensor pressed to exit program"""
    return force_sensor.pressed()

# === PROGRAM 1: COLLECTION ===
def run_collection_program():
    # Configuration
    TAPE_MM = 10
    MOVE_TIME_MS = 2000
    MOVE_DELAY_MS = 200
    GIVING_OVERSHOOT_MM = 0.00
    
    # State
    red_detected = False
    event_count = 0
    
    def calc_degrees_to_move(tape_mm, radius_mm, gear_ratio):
        reel_deg = (tape_mm / (2 * 3.1416 * radius_mm)) * 360
        return reel_deg * gear_ratio
    
    def is_red_detected():
        h, s, v = color_sensor.hsv()
        return (h < 30 or h > 330) and s > 30 and v > 10
    
    def update_display():
        grid = [[0]*5 for _ in range(5)]
        ones = event_count % 10
        tens = (event_count // 10) % 10
        hundreds = (event_count // 100) % 10
        
        for i in range(min(ones, 10)):
            row, col = divmod(i, 5)
            grid[row][col] = 100
        for i in range(min(tens, 10)):
            row, col = divmod(i, 5)
            grid[row+2][col] = 100
        for i in range(min(hundreds, 5)):
            grid[4][i] = 100
            
        hub.display.icon(grid)
    
    def move_tape():
        nonlocal event_count
        if MOVE_DELAY_MS > 0:
            wait(MOVE_DELAY_MS)
        
        rad_d = estimate_radius(abs(motor_d.angle()) / GEAR_RATIO_D, REEL_START_RADIUS_D)
        rad_b = estimate_radius(abs(motor_b.angle()) / GEAR_RATIO_B, REEL_START_RADIUS_B)
        
        deg_d = calc_degrees_to_move(TAPE_MM, rad_d, GEAR_RATIO_D)
        deg_b = calc_degrees_to_move(TAPE_MM + GIVING_OVERSHOOT_MM, rad_b, GEAR_RATIO_B)
        
        speed_d = deg_d / (MOVE_TIME_MS / 1000)
        speed_b = deg_b / (MOVE_TIME_MS / 1000)
        
        motor_d.run_angle(speed_d, deg_d, wait=False)
        motor_b.run_angle(speed_b, deg_b)
        
        motor_d.stop()
        motor_b.brake()
        
        event_count += 1
        update_display()
    
    # Main collection loop
    wait_for_force_start()
    update_display()
    
    while True:
        if check_force_exit():
            motor_b.stop()
            motor_d.stop()
            break
        
        red = is_red_detected()
        
        if red and not red_detected:
            move_tape()
            red_detected = True
        elif not red:
            red_detected = False
        
        wait(100)

# === PROGRAM 2: TENSION ===
def run_tension_program():
    TENSION_SPEED_MM_S = 2
    
    wait_for_force_start()
    
    while True:
        if check_force_exit():
            motor_d.stop()
            motor_b.stop()
            break
            
        rad_d = estimate_radius(abs(motor_d.angle()) / GEAR_RATIO_D, REEL_START_RADIUS_D)
        rad_b = estimate_radius(abs(motor_b.angle()) / GEAR_RATIO_B, REEL_START_RADIUS_B)
        
        speed_d = (TENSION_SPEED_MM_S / rad_d) * (360 / (2*3.1416)) * GEAR_RATIO_D
        speed_b = (TENSION_SPEED_MM_S / rad_b) * (360 / (2*3.1416)) * GEAR_RATIO_B
        
        motor_d.run(speed_d)
        motor_b.run(-speed_b)
        
        wait(100)

# === PROGRAM 3: REWIND ===
def run_rewind_program():
    wait_for_force_start()
    
    while True:
        if check_force_exit():
            motor_d.stop()
            motor_b.stop()
            break
            
        rad_d = estimate_radius(abs(motor_d.angle()) / GEAR_RATIO_D, REEL_START_RADIUS_D)
        rad_b = estimate_radius(abs(motor_b.angle()) / GEAR_RATIO_B, REEL_START_RADIUS_B)
        
        v = 10.0  # tape speed mm/s
        speed_d = (v / rad_d) * (360 / (2*3.1416)) * GEAR_RATIO_D
        speed_b = (v / rad_b) * (360 / (2*3.1416)) * GEAR_RATIO_B
        
        motor_d.run(-speed_d)  # rewind direction
        motor_b.run(-speed_b)
        
        wait(100)

# === MAIN EXECUTION ===
print("Multi-Program System Starting...")
show_menu()
