# Ansel and Srikar - Multithreading ESP

To run the 2 motors simultaneously, we tried multithreading the ESP 32. It has two CPUs, so the individual CPUs were given tasks to run each motor, independently keeping track of the position and timing of each motor. This allows the servo motor to be evenly incremented (like the second hands of the clock) by 10º in parallel with the full 360º rotation of the stepper motor, instead of having the servo jump all 10 degrees at once in between stepper rotations.

This guide explains setting up multithreading on the ESP using Free RTOS (a minimal OS for task management on embedded systems). ((it’s not [the one we used in lab](https://randomnerdtutorials.com/esp32-dual-core-arduino-ide/) but it’s a little cleaner)) The Arduino IDE supports Free RTOS without even needing to import a header file.

[https://savjee.be/blog/multitasking-esp32-arduino-freertos/](https://savjee.be/blog/multitasking-esp32-arduino-freertos/)

NB: we did not get this working perfectly, as Free RTOS’s watchdog gets annoyed at the line

```arduino
myStepper.step(stepsPerRevolution);
```

and resets the system, causing the servo motor to glitch out every few seconds. It is clear that both motors were running fine in tandem up until this point, so figuring out a way to disable the watchdog or otherwise convene to the will of Free RTOS would probably fix this.

The motor code is I think based on examples from the included ESP32Servo and Stepper Libraries and [this link](https://create.arduino.cc/projecthub/debanshudas23/getting-started-with-stepper-motor-28byj-48-3de8c9)
