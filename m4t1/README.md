# Ansel and Srikar - Multithreading ESP

To run the 2 motors simultaneously, we tried multithreading the ESP 32. It has two CPUs, so the individual CPUs were given tasks to run each motor, independently keeping track of the position and timing of each motor. This allows the servo motor to be evenly incremented (like the second hands of the clock) by 10º in parallel with the full 360º rotation of the stepper motor, instead of having the servo jump all 10 degrees at once in between stepper rotations. 

This guide explains setting up multithreading on the ESP using Free RTOS (a minimal OS for task management on embedded systems). ((it’s not [the one we used in lab](https://randomnerdtutorials.com/esp32-dual-core-arduino-ide/) but it’s a little cleaner)) The Arduino IDE supports Free RTOS without even needing to import a header file.

[https://savjee.be/blog/multitasking-esp32-arduino-freertos/](https://savjee.be/blog/multitasking-esp32-arduino-freertos/)

NB: we did not get this working perfectly, as Free RTOS’s watchdog gets annoyed at the line

```arduino
myStepper.step(stepsPerRevolution);
```

and resets the system, causing the servo motor to glitch out every few seconds. It is clear that both motors were running fine in tandem up until this point, so figuring out a way to disable the watchdog or otherwise convene to the will of Free RTOS would probably fix this.

Here is the code we used to run the 2 motors in parallel: (motor code is I think based on examples from the included ESP32Servo and Stepper Libraries and [this link](https://create.arduino.cc/projecthub/debanshudas23/getting-started-with-stepper-motor-28byj-48-3de8c9))

```arduino
#include <ESP32Servo.h>
#include <Stepper.h>

TaskHandle_t Task1;
TaskHandle_t Task2;

const int stepsPerRevolution = 2048;  // change this to fit the number of steps per revolution

// ULN2003 Motor Driver Pins
#define IN1 12
#define IN2 14
#define IN3 27
#define IN4 26

// initialize the stepper library
Stepper myStepper(stepsPerRevolution, IN1, IN3, IN2, IN4);

Servo myservo;  // create servo object to control a servo

// Recommended PWM GPIO pins on the ESP32 include 2,4,12-19,21-23,25-27,32-33 
int servoPin = 32;

void setup() {
  // initialize the serial port
  Serial.begin(115200);

  xTaskCreatePinnedToCore(
    StepperCode, /* Function to implement the task */
    "Task1", /* Name of the task */
    10000,  /* Stack size in words */
    NULL,  /* Task input parameter */
    1,  /* Priority of the task */
    &Task1,  /* Task handle. */
    0); /* Core where the task should run */

  xTaskCreatePinnedToCore(
    ServoCode, /* Function to implement the task */
    "Task2", /* Name of the task */
    10000,  /* Stack size in words */
    NULL,  /* Task input parameter */
    1,  /* Priority of the task */
    &Task2,  /* Task handle. */
    1); /* Core where the task should run */
}

void loop() {
	// this is empty, code runs in loops in the two task functions below
}

void StepperCode(void * parameter) {
  // set the speed at 5 rpm
  myStepper.setSpeed(5);
  for (;;) {
		// rotate
    myStepper.step(stepsPerRevolution);
  }
}

void ServoCode(void * parameter) {
  // initialization for servo lib
	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	myservo.setPeriodHertz(50); // standard 50 hz servo
	myservo.attach(servoPin, 400, 2400); // attaches the servo on pin 18 to the servo object
	// using default min/max of 1000us and 2000us
	// different servos may require different min/max settings
	// for an accurate 0 to 180 sweep
  int pos = 0;
  int offset = 1;

  for (;;) {
    if (pos >= 180) {
			// switch directions if we've reached the edge of servo capabilities
      offset = -1;
    }
    if (pos <= 0) {
			// and vice versa of above
      offset = 1;
    }
    pos += offset;
    myservo.write(pos);
    delay(1200); // tick 10 degrees over the course of 12 seconds = 1 degree per 1200 ms
  }
}
```