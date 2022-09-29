#!/usr/bin/env python

# RASPIAN USAGE: first install pyaudio for mode 3 to work
# also adjust GPIO as necessary for your physical configuration
# IMPORTANT: audio will play through raspi 3.5 mm jack, use `alsamixer` to TURN DOWN THE VOLUME

# $ pip install pyaudio

import os
import curses
from time import sleep
from sys import stdout
from gpiozero import Button, PWMLED
import pyaudio
import numpy as np

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
    term_len = curses.COLS
    term_height = curses.LINES

    # state for mode 1
    pos_x = term_len - 2  # for some reason curses has a problem with drawing in the bottom-most box
    pos_y = term_height - 2

    # state for mode 2
    color_pair = 0
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # state for mode 3 (audio code based on https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python)
    p = pyaudio.PyAudio()
    volume = 0.25  # range [0.0, 1.0]
    fs = 44100  # sampling rate, Hz, must be integer
    duration = 0.5  # in seconds, may be float
    freqs = [
        130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65,
        220.00, 233.08, 246.94
    ]
    current_note = 0

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)

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

        elif mode == 1:
            # mode 2: cycle through colors, (cycle backwards if joystick_x held)
            # holding joystick button pauses cycle, switch turns on reverse video
            sleep(1)
            color_mode = curses.A_REVERSE if switch.is_active else curses.A_NORMAL
            if not joystick.is_active:
                if joystick_x.is_active:
                    color_pair = (color_pair + 1) % 8
                else:
                    color_pair = (color_pair - 1) % 8
            for i in range(term_height - 1):
                stdscr.addstr(i, 0, '#' * term_len,
                              color_mode | curses.color_pair(color_pair))

        elif mode == 2:
            # mode 3: play sine wave, joystick controls frequency (hold button for a little longer than normal to switch modes
            # hold joystick to stop, switch toggles up an octave

            # again, code taken from https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python
            while True:
                if button.is_pressed:
                    break
                # switch jumps up an octave
                f = freqs[current_note] * 2 if switch.is_active else freqs[
                    current_note]
                samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f /
                                  fs)).astype(np.float32)
                stream.write((volume * samples).tobytes())
                if not joystick.is_active:
                    if joystick_x.is_active:
                        current_note = (current_note - 1) % len(freqs)
                    else:
                        current_note = (current_note + 1) % len(freqs)

        # update the screen after each loop
        stdscr.refresh()


curses.wrapper(main)
