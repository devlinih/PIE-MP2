// Firmware for a rudimentary 3D scanner using a pan/tilt mechanism
// Olin College of Engineering PIE Miniproject 2

#include <Servo.h>

const int SENSOR = 0;         // IR distance sensor on A0
Servo pan;                    // create servo object for pan
Servo tilt;                   // create servo object for tilt
int samples;                  // the number of samples taken for each scan
const int ALL_SAMPLES = 3;    // total number of samples per scan

// set scanning resolution
const int TILT_INTERVAL = 20; // move 20 degrees down between each pan row
const int PAN_INTERVAL = 5;   // send data every 5 degrees while panning
const int MAX_TILT_DEG = 120; // maximum tilt position (degree)
const int MIN_TILT_DEG = 60;  // minimum tilt postion (degree)
const int MAN_PAN_DEG = 180;  // maximum pan position (degree)
const int MIN_PAN_DEG = 0;    // minimum pan position (degree)

enum states
{ // Defines the enumerated types for state machine
  LISTENING,
  SCAN1,
  SCAN2
};
states state;

// function prototypes for organization
void readSerialBuffer();
void sendData();
void scan1();
void scan2();

// setup function to initialize hardware and software
void setup()
{
  // start the serial port with fast baud rate (115200 bits per sec)
  Serial.begin(115200);

  // attach servos to pins
  pan.attach(3);  // Servo on D3
  tilt.attach(5); // Servo on D5

  // wait for signal
  state = LISTENING;
}

// main loop
void loop()
{
  switch (state)
  {
  case LISTENING: // wait for signal over serial
    readSerialBuffer();
    break;
  case SCAN1: // scan with tilt only
    scan1();
    break;
  case SCAN2: // scan with pan and tilt
    scan2();
    break;
  }
}

void scan1() // use only tilt servo
{
  for (int tilt_deg = MIN_TILT_DEG; tilt_deg < MAX_TILT_DEG; tilt_deg += TILT_INTERVAL)
  {
    tilt.write(tilt_deg);
    delay(150);
    sendData();
  }
  // scan complete, return to listening
  state = LISTENING;
}

void scan2() // uses both pan and tilt servos
{
  for (int tilt_deg = MIN_TILT_DEG; tilt_deg < MAX_TILT_DEG; tilt_deg += TILT_INTERVAL)
  {
    // tilt after each full pan
    tilt.write(tilt_deg);
    // big delay between pan cycles
    delay(2000);
    for (int pan_deg = MIN_PAN_DEG; pan_deg < MAN_PAN_DEG; pan_deg += PAN_INTERVAL)
    {
      // pan and scan
      pan.write(pan_deg); // pan a bit
      // small delay between scans and small servo movement
      delay(150);
      // send data over serial
      sendData();
    }
  }
  // scan complete, return to listening
  state = LISTENING;
}

void readSerialBuffer()
{
  while (Serial.available() == 0)
  {
    // wait for data available in serial receive buffer
  }
  String command = Serial.readStringUntil('\n'); // read until timeout
  command.trim();  // remove white space or \n
  if (command.substring(2) == "SCAN1")
  {
    // begin writing to serial
    Serial.print("[");
    // start scanning mode 1 in next loop
    state = SCAN1;
  }
  else if (command.substring(2) == "SCAN2")
  {
    // begin writing to serial
    Serial.print("[");
    // start scanning mode 2 in next loop
    state = SCAN2;
  }
}

uint16_t readIR()
{
  // helper function to read IR sensor
  uint16_t v1, v2, v3;
  v1 = analogRead(0);
  v2 = analogRead(0);
  v3 = analogRead(0);
  // take the lowest of three samples to filter out spikes
  return min(min(v1, v2), v3);
}

void sendData() // NOTE: sends chunks of data at a time
{
  // get current position of servos in degrees
  int pan_deg = pan.read();
  int tilt_deg = tilt.read();

  // get voltage of IR sensor
  uint16_t sensor = readIR();

  // write to serial to send back to python script
  Serial.print("(");
  Serial.print(pan_deg);
  Serial.print(",");
  Serial.print(tilt_deg);
  Serial.print(",");
  Serial.print(sensor);
  Serial.print(")");

  // add separator between each scan
  if (samples < ALL_SAMPLES)
  {
    Serial.print(",");
  }
  else // end of transmission
  {
    Serial.print("]");
  }
}