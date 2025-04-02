import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key

# Configuration options for the auto-clicker
options = {
    "delay"     : 0.1,  # Initial delay between clicks
    "min_delay" : 0.05, # Minimum delay between clicks
    "buttons"   : {
        "left"  : Button.left, # Left button to click
        "right" : Button.right, # Right button to click
    },
    "keys":      {
        "start"        : KeyCode(char="s"), # Key to start clicking
        "pause"        : KeyCode(char="p"), # Key to pause clicking
        "stop"         : KeyCode(char="q"), # Key to stop the program
        "toggle_left"  : Key.left,          # Key to toggle left button clicking
        "toggle_right" : Key.right,         # Key to toggle right button clicking
        "speed_up"     : Key.up,            # Key to increase clicking speed
        "speed_down"   : Key.down,          # Key to decrease clicking speed
    }
}

# AutoClicker class handles automatic mouse clicking with configurable options.
class AutoClicker(threading.Thread) :

    def __init__(self, delay, buttons, min_delay) : 
        super(AutoClicker, self).__init__()
        self.delay               = delay # Delay between clicks
        self.min_delay           = min_delay # Minimum delay between clicks
        self.buttons             = buttons # Buttons to click
        self.running             = threading.Event() # Replaces self.running flag
        self.active              = True # Indicates if the program is running
        self.left_click_enabled  = True # Left button enabled
        self.right_click_enabled = False # Right button enabled

    # Start the auto-clicking process.
    def start_clicking(self) : 
        self.running.set()

    # Pause the auto-clicking process.
    def stop_clicking(self) : 
        self.running.clear()

    # Toggle left button clicking.
    def toggle_left_click(self) : 
        self.left_click_enabled = not self.left_click_enabled

    # Toggle right button clicking.
    def toggle_right_click(self) : 
        self.right_click_enabled = not self.right_click_enabled

    # Increase the clicking speed.
    def increase_speed(self):
        self.delay = round(max(self.min_delay, self.delay - 0.1), 2)

    # Decrease the clicking speed.
    def decrease_speed(self):
        self.delay = round(self.delay + 0.1, 2)

    # Exit the program.
    def exit_program(self):
        self.active = False
        self.running.set()  # Unblock any waiting threads

    # Main execution loop of the auto-clicker thread.
    def run(self):
        while self.active:
            self.running.wait()  # Wait until the `start_clicking` event is set
            if self.active:  # Check if still active before clicking
                if self.left_click_enabled:
                    mouse.click(self.buttons["left"])
                if self.right_click_enabled:
                    mouse.click(self.buttons["right"])
                time.sleep(self.delay)


# Initialize mouse controller and auto-clicker
mouse = Controller()
auto_clicker = AutoClicker(
    delay=options["delay"],
    buttons=options["buttons"],
    min_delay=options["min_delay"]
)
auto_clicker.start()

# Display instructions to the user
print("AutoClicker Controls:")
print("Press 's' to Start clicking")
print("Press 'p' to Stop clicking")
print("Press 'q' to Quit the program")
print("Press '←' to Toggle Left Click")
print("Press '→' to Toggle Right Click")
print("Press '↑' to Increase Click Speed")
print("Press '↓' to Decrease Click Speed\n")


def handler(key):
    try:
        if key == options["keys"]["start"]:
            auto_clicker.start_clicking()
        elif key == options["keys"]["pause"]:
            auto_clicker.stop_clicking()
        elif key == options["keys"]["stop"]:
            auto_clicker.exit_program()
            listener.stop()
        elif key == options["keys"]["toggle_left"]:
            auto_clicker.toggle_left_click()
        elif key == options["keys"]["toggle_right"]:
            auto_clicker.toggle_right_click()
        elif key == options["keys"]["speed_up"]:
            auto_clicker.increase_speed()
        elif key == options["keys"]["speed_down"]:
            auto_clicker.decrease_speed()
    except Exception as e:
        print(f"Error handling key press: {e}")


# Start listening for keyboard inputs
with Listener(on_press=handler) as listener:
    listener.join()
