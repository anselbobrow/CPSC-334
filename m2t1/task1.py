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


mode = 1
button.when_activated = change_mode


def main(stdscr):
    # curses initialization
    stdscr.clear()
    curses.curs_set(0)  # hide the cursor
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)
    term_len = curses.COLS
    term_height = curses.LINES

    # initial state for mode 1
    pos_x = term_len - 2  # for some reason curses has a problem with drawing in the bottom-most box
    pos_y = term_height - 2

    # initial state for mode 2
    color_pair = 0
    while True:
        if mode == 0:
            # mode 1: move circle around screen across x, y coordinates, switch controls character
            # draw grid of #'s with 'O' as cursor. switch flips joystick directions.

            # draw the grid
            for i in range(pos_y):
                stdscr.addstr(i, 0, '#' * term_len)
            stdscr.addstr(pos_y, 0, '#' * pos_x)
            stdscr.addstr(pos_y, pos_x, 'O')
            stdscr.addstr(pos_y, pos_x + 1, '#' * (term_len - pos_x - 1))
            for i in range(pos_y + 1, term_height):
                stdscr.addstr(i, 0, '#' * (term_len - 1))

            # switch functionality
            jx = jy = True
            if switch.is_active:
                jx = joystick_x.is_active
                jy = joystick_y.is_active
            else:
                # gravity reverse!!!
                jx = not joystick_x.is_active
                jy = not joystick_y.is_active

            # update the position
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
            sleep(0.1)
        if mode == 1:
            # mode 2: cycle through colors, (cycle backwards if joystick_x held)
            # holding joystick button pauses cycle, switch turns on reverse video
            color_mode = curses.A_REVERSE if switch.is_active else curses.A_NORMAL
            for i in range(term_height - 1):
                stdscr.addstr(i, 0, '#' * term_len,
                              color_mode | curses.color_pair(color_pair))
            if not joystick.is_active:
                if joystick_x.is_active:
                    color_pair = (color_pair + 1) % 8
                else:
                    color_pair = (color_pair - 1) % 8
            sleep(1)
        if mode == 2:
            # mode 3
            continue

        # update the screen after each loop
        stdscr.refresh()


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
