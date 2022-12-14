// Firmware for a rudimentary 3D scanner using a pan/tilt mechanism
// Olin College of Engineering PIE Miniproject 2

#include <Servo.h>

const int SENSOR = 0;         // IR distance sensor on A0
Servo pan;                    // create servo object for pan
Servo tilt;                   // create servo object for tilt

const int LEVEL_PAN = 82;     // pan degree when straight
const int LEVEL_TILT = 60;    // tilt degree when flat

// set scanning resolution
const int TILT_INTERVAL1 = 2; // Scan 1 resolution (degrees), MUST be evenly divisible by max-min tilt degrees
const int TILT_INTERVAL2 = 2; // degrees down between each pan row, MUST be evenly divisible by max-min tilt degrees
const int PAN_INTERVAL = 2;   // frequency of data scans per pan (degrees), MUST be evenly divisible by max-min pan degrees

// breadth of scan sweep relative to resting positions
const int MAX_TILT_DEG = LEVEL_TILT +30;  // maximum tilt position (degree)
const int MIN_TILT_DEG = LEVEL_TILT -30;  // minimum tilt position (degree)
const int MAN_PAN_DEG = LEVEL_PAN +30;    // maximum pan position (degree)
const int MIN_PAN_DEG = LEVEL_PAN -30;    // minimum pan position (degree)

// Define the enumerated types for state machine
enum states
{
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

  // set servos to resting position
  pan.write(LEVEL_PAN);
  tilt.write(LEVEL_TILT);

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
  for (int tilt_deg = MIN_TILT_DEG; tilt_deg <= MAX_TILT_DEG; tilt_deg += TILT_INTERVAL1)
  {
    tilt.write(tilt_deg);
    delay(150);
    sendData();
    Serial.print(",");
  }
  // scan complete, return to listening
  Serial.println();
  state = LISTENING;
}

void scan2() // uses both pan and tilt servos
{
  for (int tilt_deg = MIN_TILT_DEG; tilt_deg <= MAX_TILT_DEG; tilt_deg += TILT_INTERVAL2)
  {
    // tilt after each full pan
    tilt.write(tilt_deg);
    // big delay between pan cycles
    pan.write(MIN_PAN_DEG);
    delay(250);
    for (int pan_deg = MIN_PAN_DEG; pan_deg < MAN_PAN_DEG; pan_deg += PAN_INTERVAL)
    {
      // small delay between scans and small servo movement
      delay(100);
      // pan and scan
      pan.write(pan_deg); // pan a bit
      // send data over serial
      sendData();
      Serial.print(",");
    }
  }
  // scan complete, return to listening
  Serial.println();
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
  if (command.equals("SCAN1"))
  {
    // start scanning mode 1 in next loop
    state = SCAN1;
  }
  else if (command.equals("SCAN2"))
  {
    // start scanning mode 2 in next loop
    state = SCAN2;
  }
  else if (command.equals("CALIBRATE"))
  {
    // set servos to default position
    tilt.write(LEVEL_TILT);
    pan.write(LEVEL_PAN);

    // send data over serial
    sendData();
    Serial.println();
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
}
