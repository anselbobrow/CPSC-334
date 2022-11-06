

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
// 16 servo objects can be created on the ESP32



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
  delay(500);
  xTaskCreatePinnedToCore(
    ServoCode, /* Function to implement the task */
    "Task2", /* Name of the task */
    10000,  /* Stack size in words */
    NULL,  /* Task input parameter */
    1,  /* Priority of the task */
    &Task2,  /* Task handle. */
    1); /* Core where the task should run */
  delay(500);
}

void loop() {
  // // step one revolution in one direction:
  // Serial.println("clockwise");
  // myStepper.step(stepsPerRevolution);

  // if (pos >= 180) {
  //   offset = -10;
  // }
  // if (pos <= 0) {
  //   offset = 10;
  // }
  // pos += offset;
  // myservo.write(pos);
}

void StepperCode(void * parameter) {
  // set the speed at 5 rpm
  myStepper.setSpeed(5);
  // Serial.println("Entering StepperCode");
  for (;;) {

    myStepper.step(stepsPerRevolution);
    // Serial.println("Running in StepperCode");
  }
}

void ServoCode(void * parameter) {
  // Allow allocation of all timers
	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	myservo.setPeriodHertz(50);    // standard 50 hz servo
	myservo.attach(servoPin, 400, 2400); // attaches the servo on pin 18 to the servo object
	// using default min/max of 1000us and 2000us
	// different servos may require different min/max settings
	// for an accurate 0 to 180 sweep
  // Serial.println("Entering ServoCode");
  int pos = 0;
  int offset = 1;
  for (;;) {
    if (pos >= 180) {
      offset = -1;
    }
    if (pos <= 0) {
      offset = 1;
    }
    pos += offset;
    myservo.write(pos);
    delay(1200);
    Serial.println("pos: " + pos);
  }
}