// Firmware for a rudimentary 3D scanner using a pan/tilt mechanism
// Olin College of Engineering PIE Miniproject 2

#include <Servo.h>

const int SENSOR = 0;       // IR distance sensor on A0
Servo pan;                  // create servo object for pan
Servo tilt;                 // create servo object for tilt
bool scanning;              // global vaiable to indicate if the Arduimo should be scanning
int samples;                // the number of samples taken for each scan
const int ALL_SAMPLES = 3;  // total number of samples per scan

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

  // TODO move the servos to the start position

  // don't scan yet
  scanning = false;
  samples = 0;
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
    if (samples < ALL_SAMPLES)
    {
      panTilt();
      samples += 1;
      sendData();
    }
    else // finished sampling
    {
      scanning = false;
      samples = 0;
    }
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
    // begin writing to serial
    Serial.print("[");
  }
}

void panTilt()
{
  // move servos a little bit
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

void sendData() // NOTE: currenly sends chunks of data at a time
{
  // get current position of servos in degrees
  int pan_deg = pan.read();
  int tilt_deg = tilt.read();

  // get voltage of IR sensor
  uint16_t sensor = readIR();

  // write to serial to send back to python script
  Serial.print("(");
  Serial.print(pan_deg);  Serial.print(",");
  Serial.print(tilt_deg); Serial.print(",");
  Serial.print(sensor);   Serial.print(")");

  // add separator between each scan
  if (samples < ALL_SAMPLES)
  {
    Serial.print(",");
  }
  else //end of transmission
  {
    Serial.print("]");
  }
}