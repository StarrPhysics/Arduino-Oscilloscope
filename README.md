
# Arduino Oscilloscope
<!--- Table of contents for the future
## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
-->
## Introduction
This passion-project is an attempt to use the Ardueno's analog pins as a (moderately) viable oscilloscope for studying electrical behavior. The program is built in two parts:

1. A C++ library for operating the Arduino side of the program.
2. A python client which communicates with the Arduino program and plots the data.

This program was built with an Arduino MEGA framework in mind, and so manual adjustment might be necessary depending on the circumstances. Note, this program is not an ideal replacement for an oscilloscope due to the limitations of the unspecialized hardware.

<!---
## Features
- Real-time visualization of electronic signals
- Adjustable timebase and voltage scale
- Triggering options for stable signal display
- Save and export captured waveforms
- Simple and intuitive user interface
-->
## Dependencies & Versions
The python program is built under the following:

1. [Python v3.10.11](https://www.python.org/)
2. [pyserial v3.5](https://github.com/pyserial/pyserial)
3. [numpy v1.26.0](https://numpy.org)
4. [matplotlib v3.8.0](https://matplotlib.org)

## How to Use
Here is a bare-minimum example of of how the`ArduinoOscilloscope.cpp` program should be incorporated into your ino file:
```ino
#include "./ArduinoOscilloscope.h"

ArduinoOscilloscope instance = InitalizeArduinoOscilloscope(9600,A14);

void setup() {
  instance.establishConnection();
}

void loop()
{
  instance.sendPinData();
}
```
Note this is just a copy of the `ArduinoOscilloscope.ino` in the project source.

Once these basic methods are placed in their appropriate locations, the python program can be executed by running the `ArduinoOscilloscope.py` script. Here's an example of the setup process and execution:

[![Example Video](https://i3.ytimg.com/vi/_zJXhK_8eHc/maxresdefault.jpg)](https://youtu.be/_zJXhK_8eHc)

# Contributing
Admittedly, the program isn't perfect, and my lack of experience in writing low level code might be a limiting factor; but I'm eager to optimize the project over time so that I can complement my study of circuits, hardware, and general computer science. Consequently, if you have any questions or recommendations, please raise an issue and let me know if you have any thoughts.
