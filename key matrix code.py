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

# set each pin to be an input at the start, these will switch as necessary
def setup_pins(input_pins):
    for pin in input_pins:
        key_pin = digitalio.DigitalInOut(pin)
        key_pin.direction = digitalio.Direction.INPUT
        key_pin.pull = digitalio.Pull.UP
        pin_array.append(key_pin)
    return pin_array

# reads the state of each key and returns an array with the value
def read_key_matrix(column_pin_array,row_pin_array):
    keys = [[0]*len(column_pin_array)]*len(row_pin_array)
    for column_num, column_pin in enumerate(column_pin_array):
        # change the pin to output and set it True
        column_pin.switch_to_output(value=True)
        # check each row and assign it's value to the keys array
        for row_num, row_pin in enumerate(row_pin_array):
            row_pin.switch_to_input(pull=digitalio.Pull.UP)
            keys[column_num][row_num] = row_pin.value
    return keys

# A simple neat keyboard demo in CircuitPython

# The pins we'll use, each will have an internal pullup, also defines the key order and count
#keypress_pins = [board.A3,board.A1,board.A2]

column_pins = [board.D13,board.D12] # ,board.D11,board.D10
row_pins = [board.D10,board.D9] #,board.D17,board.D18,board.D19

time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
# Our array of key objects
#key_pin_array = []

column_pin_array = setup_pins(column_pins)
row_pin_array = setup_pins(row_pins)

#initialize the key states as 0
key_states = [[0]*len(column_pin_array)]*len(row_pin_array)


# https://circuitpython.readthedocs.io/projects/hid/en/latest/api.html#adafruit-hid-keycode-keycode
# Any key may be entered as a single keycode, a string, or a list
# Use a string to type out simple text - \t for tab  \n for return \b for backspace
# If using a list, the keys will be sent in order, to press two keys together (ie - shift+tab), make a list within the list
# to disable a key, use a bool - False
# this must match the number of keys defined - multiply columns by rows to get the number of keys needed to be defined
key_map = [[]*len(column_pin_array)]*len(row_pin_array)
key_map[0][0] = Keycode.TAB # single key
key_map[0][1] = [Keycode.SHIFT,Keycode.TAB],Keycode.UP_ARROW] # sequence with modifer
key_map[1][0] = False # disabled key
key_map[1][1] = "A string!" # send a string

#if len(keys_pressed) < len(keypress_pins):
#    logger.warning("More keys defined than key presses!")

# The keyboard object!
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

print("Waiting for key pin...")

while True:
    key_states = read_key_matrix(column_pin_array, row_pin_array)
    
    for col_num, col in enumerate(key_states):
        for row_num, key_state in enumerate(col):
            if key_state:
                print("Key pressed:")
                print(col_num,row_num,sep=", ")
                
#                key = key_map[col_num][row_num]
#                if isinstance(key, str):  # If it's a string...
#                    keyboard_layout.write(key)  # ...Print the string
#                elif isinstance(key, list): # if it's a sequence to be typed...
#                    for key_press in key:
#                        if isinstance(key_press, list): # if it's a combination within the sequence, like a key with a modifier (ctrl, shift, etc)
#                            for a_press in key_press:
#                            keyboard.press(a_press)
#                        else:  # no modifier included so just send the key press
#                            keyboard.press(key_press)
#                        keyboard.release_all() # release the key or combination of presses for each step in the sequence
#                elif isinstance(key, bool):
#                    pass # this is basically a disabled key or position
#                else:  # If it's not a string or a list, treat it as a single key press...
#                    keyboard.press(key)  # "Press"...
#                    keyboard.release_all()  # ..."Release"!

    time.sleep(0.02) # debounce the keys
