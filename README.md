# IoT course 2020/2021 Final Project

# Description

The idea behind this project is to implement a basic weather station to monitor the following parameters:
+ temperature
+ humidity
+ brightness

The first two are obtained with the usage of a [HTU21D sensor](https://www.amazon.com/dp/B00XR7CR1I/).
Ambient brightness is measured by a photoresistor.

In case the temperature exceeds a certain threshold, **MAX_TEMP**, a cooling fan - controlled by a relay - is turned on.<br>
Said fan is turned off once the temperature reaches an acceptable value: **MIN_TEMP**.

A cardboard panel is attacched to a servo motor. When the device reads a stable, high value of brightness<br>
for a period of time that is greater than **UNCOVER_TIME**, the motor will turn and the panel will cover the sunlight.<br>
After a fixed period of time, **COVER_TIME**, the motor will turn back, thus exposing the device to full light again.<br>
If the room is not bright enough a led will be turned on to simulate a lighting control system.

The user can interact with the device through a web interface. It shows the data collected by the sensors<br>
and gives the user the option to change the value of the following variables:<br>
**MAX_TEMP**, **MIN_TEMP**, **COVER_TIME**, **UNCOVER_TIME**.

-----

# Implementation

The main device is an **ESP32-DevKitC** with [Zerynth OS](https://www.zerynth.com/zos/) installed on it.<br>
The language used is Python - a version that is compatible with Zerynth OS.

The user interface is web-based and implemented in HTML, CSS and Javascript.

The exchange of data between the device and the webpage is achieved through the use of the MQTT message protocol.

-----

# Components

+ ESP32-DevKitC development board
+ HTU21D temperature and humidity sensor
+ Servo motor Tower Pro SG90
+ Single relay board Parallax Inc
+ PC cooling fan
+ Breadboard
+ Photoresistor
+ 1x LED
+ 1x 220 ohm resistor
+ 1x 10k ohm resistor
+ 9x M-M jumper wires
+ 9x M-F jumper wires

-----

# Documentation

### ZERYNTH OS
+ [documentation](https://docsv2.zerynth.com/latest/reference/core/stdlib/docs/)
+ [examples](https://docsv2.zerynth.com/latest/reference/core/stdlib/docs/examples/)

### ESP32 DEVKIT-C
+ [zerynth documentation](https://docsv2.zerynth.com/latest/reference/boards/esp32_devkitc/docs/)

### MQTT PROTOCOL
+ [zerynth implementation](https://docsv2.zerynth.com/latest/reference/libs/zerynth/mqtt/docs/)
+ [paho javascript implementation](https://www.eclipse.org/paho/index.php?page=clients/js/index.php)

### HTU21D SENSOR
+ [zerynth library](https://docsv2.zerynth.com/latest/reference/libs/meas/htu21d/docs/htu21d/)
