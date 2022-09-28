#!/usr/bin/env python

import os
from time import sleep
from sys import stdout
from gpiozero import Button, PWMLED

button = Button(2)
switch = Button(3)
joystick = Button(4)
joystick_x = Button(5)
joystick_y = Button(6)

mode = 0


def change_mode():
    global mode
    mode = (mode + 1) % 3


button.when_activated = change_mode

term_len = os.get_terminal_size().columns
pos = 0
stdout.write(' ' * term_len)
while True:
    stdout.write('\b' * term_len + '#' * pos + 'O' + '#' *
                 (term_len - pos - 1))
    stdout.flush()
    sleep(0.1)
    if mode == 0:
        if not joystick_x.is_pressed:
            if pos < term_len - 1:
                pos += 1
        else:
            if 0 < pos:
                pos -= 1
    if mode == 1:
        if joystick_y.is_pressed:
            if pos < term_len - 1:
                pos += 1
        else:
            if 0 < pos:
                pos -= 1

# while True:
#    if button.is_pressed:
#        print("Button is pressed")
#    else:
#        print("Button is not pressed")
#    if switch.is_pressed:
#        print("Switch is on")
#    else:
#        print("Switch is off")
#    if joystick.is_pressed:
#        print("Joystick is pressed")
#    else:
#        print("Joystick is not pressed")
# if joystick_x.is_pressed:
#     print("Joystick is left")
# else:
#     print("Joystick is not left")
# if joystick_y.is_pressed:
#     print("Joystick is up")
# else:
#     print("Joystick is not up")
# time.sleep(0.5)

# spinner
# sys.stdout.write(' ')
# while True:
#     for c in ('/', '-', '\\', '|'):
#         time.sleep(1)
#         sys.stdout.write('\b' + c)
#         sys.stdout.flush()
