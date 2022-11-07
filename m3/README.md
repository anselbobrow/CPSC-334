# Synesthesia Box

## About
See [blog_post.md](./blog_post.md) for implementation and inspiration details.

## Raspberry Pi Setup
    
### Supercollider Installation
First, install the `scsynth` backend on the Pi. I built it from source using [this guide](https://github.com/supercollider/supercollider/blob/develop/README_RASPBERRY_PI.md) on GitHub.



## ESP32 Setup

### Wiring Diagram

### Flashing
The ESP32 program to send sensor data over UDP is `m3/RGBox/RGBox.ino`. Before flashing, be sure to adjust the GPIO pin numbers to the ones you are using, as well as the IP address of the devices you wish to send UDP packets to (in this case, the Pi).
