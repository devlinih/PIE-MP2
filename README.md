# PIE Mini Project 2

Devlin Ih, Kat Canavan, Ethan Chen

# Repository Structure

## PanTiltFirmware

Contains the Arduino sketch with the 3D scanner firmware. Expects servos
connected to `D5` and `D6`, as well as the distance sensor connected to `A0`.

## circuitTest

Contains an Arduino sketch that mocks the 3D scanner firmware. Used to test
serial communication between PC and Arduino.

## reportPlots

Contains Python generated figures for the project report.

## visualizer

Contains Python code for the 3D scanner interface. To run the interface, run
`python user_interface.py` from this directory.
