#!/usr/bin/env python

import os
import curses
from time import sleep
from sys import stdout
from gpiozero import Button, PWMLED

# handle GPIO
button = Button(2)
switch = Button(3)
joystick = Button(4)
joystick_x = Button(5)
joystick_y = Button(6)


# initialize mode and change_mode functions
def change_mode():
    global mode
    mode = (mode + 1) % 3


mode = 0
button.when_activated = change_mode


def main(stdscr):
    # curses
    stdscr.clear()
    curses.curs_set(0)
    term_len = curses.COLS
    term_height = curses.LINES

    pos_x = term_len - 2
    pos_y = term_height - 2
    while True:
        if mode == 0:
            # mode 1: move circle around screen across x, y coordinates, switch controls character
            # draw grid of #'s with 'O' as cursor
            for i in range(pos_y):
                stdscr.addstr(i, 0, '#' * term_len)
            # stdscr.addstr(pos_y, 0,
            #               '#' * pos_x + 'O' + '#' * (term_len - pos_x - 1))
            stdscr.addstr(pos_y, 0, '#' * pos_x)
            stdscr.addstr(pos_y, pos_x, 'O')
            stdscr.addstr(pos_y, pos_x + 1, '#' * (term_len - pos_x - 1))
            for i in range(pos_y + 1, term_height):
                stdscr.addstr(i, 0, '#' * (term_len - 1))

            jx = jy = True
            if switch.is_active:
                # gravity reverse!!!
                jx = joystick_x.is_active
                jy = joystick_y.is_active
            else:
                jx = not joystick_x.is_active
                jy = not joystick_y.is_active

            if jx:
                if 0 < pos_x:
                    pos_x -= 1
            else:
                if pos_x < term_len - 2:
                    pos_x += 1

            if jy:
                if 0 < pos_y:
                    pos_y -= 1
            else:
                if pos_y < term_height - 2:
                    pos_y += 1
        if mode == 1:
            continue
            # mode 2
        if mode == 2:
            continue
            # mode 3
        stdscr.refresh()
        sleep(0.1)


curses.wrapper(main)
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
