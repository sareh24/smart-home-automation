import random
import time
import tkinter as tk
from threading import Thread

# Define IoT Device Classes
class SmartDevice:
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = False

    def toggle_status(self):
        self.status = not self.status

class SmartLight(SmartDevice):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.brightness = 0

    def set_brightness(self, brightness):
        self.brightness = brightness

class Thermostat(SmartDevice):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.temperature = 20

    def set_temperature(self, temperature):
        self.temperature = temperature

class SecurityCamera(SmartDevice):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.motion_detected = False

    def detect_motion(self):
        self.motion_detected = random.choice([True, False])

# Automation System and Rule Classes
class AutomationSystem:
    def __init__(self):
        self.devices = []
        self.rules = []
       

    def add_device(self, device):
        self.devices.append(device)
       

    def add_rule(self, rule):
        self.rules.append(rule)
        print(self.rules)
    

    def execute_rules(self):
        for rule in self.rules:
            rule.apply(self.devices)

class AutomationRule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

    def apply(self, devices):
        if self.condition(devices):
            self.action(devices)

# GUI Dashboard Class
class Dashboard:
    def __init__(self, root, system):
        self.root = root
        self.system = system
        self.root.title("Smart Home IoT Simulator")

     # New attribute to toggle between manual and random input for devices
        self.random_mode = True 

        self.labels = []
        self.buttons = []  # Store buttons for state updates(add to documentation)
        self.automation_on = True
        self.automation_text = tk.StringVar()
        #self.automation_text.set("Random automation: {}".format("ON" if self.automation_on else "OFF"))


        self.device_listbox = tk.Listbox(root, width=50)
        self.device_listbox.pack()

        self.create_device_controls()
        self.create_rule_controls()

        self.update_device_list()
        self.update_thread = Thread(target=self.simulation_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
                # Sensor input toggle button
        self.sensor_mode_button = tk.Button(root, text="Switch to Manual Control", command=self.toggle_sensor_mode)
        self.sensor_mode_button.pack()

        #self.automation_btn = tk.Button(self.root, textvariable=self.automation_text, command=lambda: self.toggle_random())
        #self.automation_btn.pack()


    # NEW - Toggle between manual and random mode for device input
    def toggle_sensor_mode(self):
        self.random_mode = not self.random_mode
        mode_text = "Switch to Random Automation" if not self.random_mode else "Switch to Manual Control"
        self.sensor_mode_button.config(text=mode_text)

         # Disable all manual controls when in random mode
        for widget in self.buttons:
          widget["button"].config(state="normal" if not self.random_mode else "disabled")

    def toggle_random(self):
        self.automation_on = not self.automation_on
        #self.automation_text.set("Random automation: {}".format("ON" if self.automation_on else "OFF"))

    def create_device_controls(self):
        # Create controls for each device
        for i, device in enumerate(self.system.devices):
            if isinstance(device, SmartLight):
                self.create_light_controls(device)
                var_str = tk.StringVar()
                var_str.set("{} - {}%".format(device.device_id, device.brightness))
                tmp_label = tk.Label(self.root, textvariable=var_str)
                self.labels.append({
                    'id': device.device_id,
                    'label': var_str,
                    'device': device
                })
                tk.Button(self.root, text="Toggle ON/OFF", command=lambda device=device: self.toggle_helper(device)).pack()
                tmp_label.pack()
            elif isinstance(device, Thermostat):
                self.create_thermostat_controls(device)
                var_str = tk.StringVar()
                var_str.set("{} - {}-C".format(device.device_id, device.temperature))
                tmp_label = tk.Label(self.root, textvariable=var_str)
                self.labels.append({
                    'id': device.device_id,
                    'label': var_str,
                    'device': device
                })
                tk.Button(self.root, text="Toggle ON/OFF", command=lambda device=device: self.toggle_helper(device)).pack()
                tmp_label.pack()
            elif isinstance(device, SecurityCamera):
                self.create_camera_controls(device)
                var_str = tk.StringVar()
                var_str.set("{} - Motion: {}".format(device.device_id, 'YES' if device.motion_detected else 'NO'))
                tmp_label = tk.Label(self.root, textvariable=var_str)
                self.labels.append({
                    'id': device.device_id,
                    'label': var_str,
                    'device': device
                })
                tk.Button(self.root, text="Toggle ON/OFF", command=lambda device=device: self.toggle_helper(device)).pack()
                tmp_label.pack()

    def toggle_helper(self, device):
        device.toggle_status()
        self.update_values()  # Ensure labels and button states are updated.

           # Dynamically update the button text (e.g., 'Turn On' or 'Turn Off')
        for widget in self.buttons:
           if widget["device_id"] == device.device_id:  # Identify the button tied to this device
              widget["button"].config(text="Turn On" if not device.status else "Turn Off")

    def update_values(self):
        for tmp_label in self.labels:
            device = tmp_label['device']
            if isinstance(device, SmartLight):
                tmp_label['label'].set("{} - {}".format(device.device_id, f"{device.brightness}%" if device.status else "(OFF)"))
            elif isinstance(device, Thermostat):
                tmp_label['label'].set("{} - {}".format(device.device_id, f"{device.temperature}C" if device.status else "(OFF)"))
            elif isinstance(device, SecurityCamera):
                tmp_label['label'].set("{} - Motion: {}".format(device.device_id, ('YES' if device.motion_detected else 'NO')  if device.status else "(OFF)"))

    def create_light_controls(self, light):
         tk.Label(self.root, text=f"{light.device_id} Controls:").pack()  # Label for the light controls

        # Slider for brightness adjustment
         tk.Scale(
            self.root, from_=0, to=100, orient="horizontal",
            command=lambda val, dev=light: self.set_brightness(dev, int(val))
         ).pack()

         # ON/OFF button
         toggle_btn = tk.Button(
            self.root,
            text="Turn On" if not light.status else "Turn Off",
            command=lambda dev=light: self.toggle_helper(dev)
         )
         toggle_btn.pack()

         # Store in self.buttons for state updates
         self.buttons.append({"device_id": light.device_id, "button": toggle_btn})

    def create_thermostat_controls(self, thermostat):
            # Create and pack a label for the thermostat
      tk.Label(self.root, text=f"{thermostat.device_id} Temperature:").pack()

    # Slider for temperature adjustment
      tk.Scale(
        self.root, from_=18, to=30, orient="horizontal",
        command=lambda val, dev=thermostat: self.set_temperature(dev, int(val))
       ).pack()

    # Toggle button for turning the thermostat ON/OFF
      tk.Button(
        self.root,
        text="Toggle Thermostat",  # Button label
        command=lambda dev=thermostat: self.toggle_device(dev)  # Toggle functionality
       ).pack()

    def create_camera_controls(self, camera):
        # Label for the camera controls
      tk.Label(self.root, text=f"{camera.device_id} Motion Detection:").pack()

    # Button for detecting motion
      tk.Button(
        self.root,
        text="Random Detect Motion",
        command=lambda camera=camera: self.detect_motion(camera)
      ).pack()

    def create_rule_controls(self):
        # Create controls for adding rules
      tk.Label(self.root, text="Create Automation Rule").pack()

      tk.Button(self.root, text="Turn on lights when motion is detected",
              command=lambda: self.add_light_rule()).pack()
    def add_light_rule(self):
        """
        Add a rule that turns on the lights when motion is detected by the camera.
        """
        def motion_detected(devices):
            # Check if any camera detected motion
            return any(isinstance(d, SecurityCamera) and d.motion_detected for d in devices)

        def turn_on_lights(devices):
            # Turn on all smart lights
            for device in devices:
                if isinstance(device, SmartLight):
                    device.status = True

        # Create and add the automation rule
        rule = AutomationRule(motion_detected, turn_on_lights)
        self.system.add_rule(rule) 
    
    def update_device_list(self):
        self.device_listbox.delete(0, tk.END)
        for device in self.system.devices:
            self.device_listbox.insert(tk.END, f"{device.device_id}: {type(device).__name__} Status: {'On' if device.status else 'Off'}")

    def simulation_loop(self):
        while True:
            if self.automation_on and self.random_mode:
                
                randomize_device_states(self.system.devices)
            self.system.execute_rules()
            self.update_values()
            self.update_device_list()
            time.sleep(2)  # Simulate updates every 2 seconds

    def set_brightness(self, light, brightness):
        light.set_brightness(int(brightness))

    def set_temperature(self, thermostat, temperature):
        thermostat.set_temperature(int(temperature))

    def detect_motion(self, camera):
        camera.detect_motion()

    def create_automation_rule(self):
        def motion_detected(devices):
            for device in devices:
                if isinstance(device, SecurityCamera) and device.motion_detected:
                    return True
            return False

        def turn_on_lights(devices):
            for device in devices:
                if isinstance(device, SmartLight):
                    device.status = True

        rule = AutomationRule(motion_detected, turn_on_lights)
        self.system.add_rule(rule)

def toggle_device(self, device):
    """
    Toggles the status (ON/OFF) of a given device.
    """
    device.status = not device.status  # Invert current status

# Randomization mechanism
def randomize_device_states(devices):
    for device in devices:
        if not device.status:
            continue

        if isinstance(device, SmartLight):
            device.set_brightness(random.randint(0, 100))
        elif isinstance(device, Thermostat):
            device.set_temperature(random.randint(18, 25))
        elif isinstance(device, SecurityCamera):
            device.detect_motion()

# Main function to initialize and run the simulation
if __name__ == "__main__":
    # Create IoT Devices
    light1 = SmartLight("Living Room Light")
    light2 = SmartLight("Living Room 2 Light")
    thermostat1 = Thermostat("Living Room Thermostat")
    camera1 = SecurityCamera("Front Door Camera")

    # Create Automation System
    automation_system = AutomationSystem()
    automation_system.add_device(light1)
    automation_system.add_device(light2)
    automation_system.add_device(thermostat1)
    automation_system.add_device(camera1)

    # Create GUI Dashboard
    root = tk.Tk()
    dashboard = Dashboard(root, automation_system)
    root.mainloop()