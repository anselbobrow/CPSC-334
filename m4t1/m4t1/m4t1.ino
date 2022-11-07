// the code for this project is documented in the knowledge share on Notion at this link:
// https://www.notion.so/scottpetersen/Ansel-and-Srikar-Multithreading-ESP-ace617fd3eaf40dc9bc51e315eea32cc

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