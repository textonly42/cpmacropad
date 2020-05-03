# CircuitPython demo - Keyboard emulator

import time

import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import adafruit_logging as logging

logger = logging.getLogger('macrolog')

# A simple neat keyboard demo in CircuitPython

# The pins we'll use, each will have an internal pullup, also defines the key order and count
keypress_pins = [board.A3,board.A1,board.A2]
# Our array of key objects
key_pin_array = []

# https://circuitpython.readthedocs.io/projects/hid/en/latest/api.html#adafruit-hid-keycode-keycode
# Any key may be entered as a single keycode, a string, or a list
# Use a string to type out simple text - \t for tab  \n for return \b for backspace
# If using a list, the keys will be sent in order, to press two keys together (ie - shift+tab), make a list within the list
keys_pressed =  [Keycode.TAB,
                [[Keycode.SHIFT,Keycode.TAB],Keycode.UP_ARROW],
                [Keycode.TAB,Keycode.UP_ARROW]
                ]

if len(keys_pressed) < len(keypress_pins):
    logger.warning("More keys defined than key presses!")

# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

# Make all pin objects inputs with pullups
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pin_array.append(key_pin)

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

print("Waiting for key pin...")

while True:
    # Check each pin
    for key_pin in key_pin_array:
        if not key_pin.value:  # Is it grounded?
            i = key_pin_array.index(key_pin)
            print("Pin #%d is grounded." % i)

            # Turn on the red LED
            led.value = True

            while not key_pin.value:
                pass  # Wait for it to be ungrounded!
            # "Type" the Keycode or string
            key = keys_pressed[i]  # Get the corresponding Keycode or string
            if isinstance(key, str):  # If it's a string...
                keyboard_layout.write(key)  # ...Print the string
            elif isinstance(key, list): # if it's a sequence to be typed...
                for key_press in key:
                    if isinstance(key_press, list): # if it's a combination within the sequence, like a key with a modifier (ctrl, shift, etc)
                        for a_press in key_press:
                            keyboard.press(a_press)
                    else:  # no modifier included so just send the key press
                        keyboard.press(key_press)
                    keyboard.release_all() # release the key or combination of presses for each step in the sequence
            else:  # If it's not a string or a list, treat it as a single key press...
                keyboard.press(key)  # "Press"...
                keyboard.release_all()  # ..."Release"!

            # Turn off the red LED
            led.value = False

    time.sleep(0.02) # debounce the keys