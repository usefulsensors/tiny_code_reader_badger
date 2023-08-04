# MicroPython example of reading the Tiny Code Reader from Useful Sensors on a
# Micro:bit. See https://usfl.ink/ps_dev for full documentation on the module,
# and README.md in this project for details on wiring and assembly.

import struct
import time

from pimoroni_i2c import PimoroniI2C

from read_qr_code import read_qr_code

import badger2040

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 128

TEXT_TOP_PADDING = 8
TEXT_HEIGHT = HEIGHT - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1
LINE_HEIGHT = 18
FONT_SIZE = 0.7

NAME_PADDING = 20

def is_too_long(text, font_size, box_width):
    new_width = display.measure_text(text, font_size)
    return (new_width > box_width)
    

def word_wrap(input_text, font_size, box_width):
    input_lines = input_text.split("\n")
    output_lines = []
    for input_line in input_lines:
        words = input_line.split(" ")        
        while len(words) > 0:
            word = words[0]
            words = words[1:]
            output_line = word
            while is_too_long(output_line, font_size, box_width):
                prefix = output_line[:-1]
                suffix = output_line[-1:]
                while is_too_long(prefix, font_size, box_width):
                    new_prefix = prefix[:-1]
                    suffix = prefix[-1:] + suffix
                    prefix = new_prefix
                output_lines.append(prefix)
                output_line = suffix
            
            while len(words) > 0:
                word = words[0]
                new_output_line = output_line + " " + word
                if is_too_long(new_output_line, font_size, box_width):
                    break
                else:
                    output_line = new_output_line
                    words = words[1:]
                
            output_lines.append(output_line)
    
    return output_lines

def draw_badge(text):
    display.set_pen(0)
    display.clear()

    # Draw a border around the image
    display.set_pen(0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
    display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

    display.set_pen(15)
    display.rectangle(0, 0, TEXT_WIDTH, HEIGHT)

    # Draw the name, scaling it based on the available width
    display.set_pen(0)
    display.set_font("sans")
 
    lines = word_wrap(text, FONT_SIZE, TEXT_WIDTH)
    for index, line in enumerate(lines):
        x = 0
        y = TEXT_TOP_PADDING + (index * LINE_HEIGHT)
        display.text(line, x, y, TEXT_WIDTH, FONT_SIZE)

    display.update()


# ------------------------------
#        Program setup
# ------------------------------

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)
display.set_thickness(2)

TEST_TEXT = """Hello World, this is Pete Warden
I am testing the word wrap capabilities with averyveryveryverylonglonglongword.
"""
draw_badge(TEST_TEXT)

while True:
    # Sometimes a button press or hold will keep the system
    # powered *through* HALT, so latch the power back on.
    display.keepalive()

    if display.pressed(badger2040.BUTTON_A):
        display.clear()
        qr_code_text = read_qr_code(10.0)
        if qr_code_text:
            display_text = qr_code_text
            draw_badge(display_text)

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()

