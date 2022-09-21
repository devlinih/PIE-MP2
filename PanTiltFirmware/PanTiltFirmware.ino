// Firmware for a rudimentary 3D scanner using a pan/tilt mechanism
// Olin College of Engineering PIE Miniproject 2

#include <Servo.h>

const int SENSOR = 0; // IR distance sensor on A0
Servo pan;            // create servo object for pan
Servo tilt;           // create servo object for tilt
int pan_deg;          // global variable to store the pan servo position
int tilt_deg;         // global variable to store the tilt servo position
bool scanning;        // global vaiable to indicate if the Arduimo should be scanning

// function prototypes for organization
void readSerialBuffer();
void panTilt();
void sendData();

// setup function to initialize hardware and software
void setup()
{
  // start the serial port with fast baud rate (115200 bits per sec)
  Serial.begin(115200);

  // attach servos to pins
  pan.attach(3);  // Servo on D3
  tilt.attach(5); // Servo on D5

  // todo move the servos to the start position
}

// main loop
void loop()
{
  if (scanning == false)
  { // listen for python script to initiate scan
    readSerialBuffer();
  }
  else
  { // do the scanning things
    panTilt();
    sendData();

    // TODO this is a placeholder so it doesn't run forever but eventually
    //  need to impliment logic to decide when it's done scanning
    scanning = false;
  }
}

void readSerialBuffer()
{
  while (Serial.available() == 0){}              // wait for data available in serial receive buffer
  String command = Serial.readStringUntil('\n'); // read until timeout
  command.trim();                                // remove white space or \n
  if (command.substring(2) == "SCAN")
  {
    scanning = true;
  }
}

void panTilt()
{
  // move servos
}

void sendData() // NOTE: currenly sends chunks of data at a time
{
  // get current position of servos in degrees
  pan_deg = 0;  // default for initial testing
  tilt_deg = 0; // default for initial testing

  // get voltage of IR sensor
  int sensor = 0; // default for initial testing

  //TODO if it's the first time add '['
  //TODO if it's the second time add ','
  //TODO if it's the last time add ']'

  // write to serial to send back to python script
  Serial.print("(");
  Serial.print(pan_deg);  Serial.print(",");
  Serial.print(tilt_deg); Serial.print(",");
  Serial.print(sensor);   Serial.print(")");
}