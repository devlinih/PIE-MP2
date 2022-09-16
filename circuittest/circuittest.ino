#define SENSORPIN A0
#define SERVOPAN 5
#define SERVOTILT 6

#include "Arduino.h"

#include <Servo.h>

void setup () {
  pinMode(SERVOPAN, OUTPUT);
  pinMode(SERVOTILT, OUTPUT);

  Serial.begin(9600);
}

void loop () {
  int distanceSensor = analogRead(SENSORPIN);
  Serial.print("Measured Value: ");
  Serial.println(distanceSensor);
}
