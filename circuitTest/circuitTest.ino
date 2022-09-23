#include "Arduino.h"

#define BAUD_RATE 115200

String commandString = "";

void setup () {
  Serial.begin(BAUD_RATE);
  Serial.println("Hello World");
}

void loop () {
  commandString = "";
  if (Serial.available()) {
    commandString = Serial.readStringUntil('\n');
    // Return a set of points representing fake scan data on receiving SCAN
    if (commandString.equals("SCAN")) {
      Serial.print("[");
      for (int tilt = 0; tilt <= 90; tilt += 5) {
        for (int pan = 0; pan <= 180; pan += 5) {
          char dataPoint[40];
          int distance = 800;
          sprintf(dataPoint, "(%d,%d,%d),", pan, tilt, distance);
          Serial.print(dataPoint);
        }
      }
      Serial.println("]");
    }
  }
}
