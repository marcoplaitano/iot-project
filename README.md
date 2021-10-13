# IoT course 2020/2021 Final Project

Final project presented at the end of the Internet Of Things course for the
academic year 2020/2021.

- - - - - -

## Description

The idea behind this project is to implement a basic weather station to monitor
the following parameters:
+ temperature
+ humidity
+ brightness

The first two are obtained with the usage of a HTU21D sensor.
Ambient brightness is measured by a photoresistor.

In case the temperature exceeds a certain threshold, **MAX_TEMP**, a coolingfan
\- controlled by a relay - is turned on.<br>
Said fan is turned off once the temperature reaches an acceptablevalue:
**MIN_TEMP**.

A cardboard panel is attacched to a servo motor. When the device reads a stable,
high value of brightness for a period of time that is greater than
**UNCOVER_TIME**, the motor will turn and the panel will cover the sunlight.<br>
After a fixed period of time, **COVER_TIME**, the motor will turn back, thus
exposing the device to full light again.<br>
If the room is not bright enough a led will be turned on to simulate a lighting
control system.

The user can interact with the device through a web interface. It shows the data
collected by the sensors and gives the user the option to change the value of
the following variables:<br>
**MAX_TEMP**, **MIN_TEMP**, **COVER_TIME**, **UNCOVER_TIME**.

- - - - - -

## Implementation

The firmware has been produced with a version of the Python language derived
from the [Zerynth SDK] for IoT platforms.

The user interface is web-based and implemented in HTML, CSS and Javascript.

The exchange of data between the device and the webpage is achieved using the
MQTT message protocol.

- - - - - -

## Components

+ ESP32-DevKitC development board
+ HTU21D temperature and humidity sensor
+ Servo motor (Tower Pro SG90)
+ Single relay board (Parallax Inc)
+ PC cooling fan
+ Breadboard
+ Photoresistor
+ LED
+ 220 Ohm resistor
+ 10k Ohm resistor
+ *12x* M/M jumper wires
+ *12x* M/F jumper wires

- - - - - -

## How it looks

### Overview

![Overview]

### Web Interface

![Web Interface]

- - - - - -

## License

Distributed under the [MIT License].


<!-- Links -->

[Zerynth SDK]:
https://www.zerynth.com/zsdk

[Overview]:
https://github.com/marcoplaitano/images/blob/main/iot_weather_overview.png
"Overview"

[Web Interface]:
https://github.com/marcoplaitano/images/blob/main/iot_weather_webinterface.png
"Web Interface"

[MIT License]:
LICENSE