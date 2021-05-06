# file: main.py
# author: marco
# date: 23 April 2021

# to redirect output to the console
import streams
streams.serial()


#########################################
#          libraries to import          #
#########################################

import adc
import json
from mqtt import mqtt
from meas.htu21d import htu21d
import sources.wifi_connection as wifi
import sources.led as leds
import sources.fan as fans
import sources.sunshield as sunshields



#########################################
#               variables               #
#########################################

PHOTORESISTOR_PIN = A1

# if the temperature exceeds this value the cooling fan will be turned on
MAX_TEMP = 37.00
# when the fan is on and temperature reaches this value, the fan turns off
MIN_TEMP = 32.00
# === the following variables are measured in seconds ===
# time the device can remain uncovered with a high value of brightness
UNCOVER_TIME = 10
# time the device has to remain covered
COVER_TIME = 8
# time between each iteration of the main loop
SLEEP_TIME = 2

client = mqtt.Client("mydevice", True)

# temperature and humidity sensor
htu = htu21d.HTU21D(I2C0)

# cooling fan controlled by a relay on pin D23
fan = fans.FAN(D23, client)

# cardboard panel attached to a servo motor controlled by pin D17
sunshield = sunshields.SUNSHIELD(D17.PWM, client)

# led to activate if the room is too dark
led = leds.LED(D18, client)



#########################################
#     mqtt communication functions      #
#########################################

def confirm_subscribe(data):
    print("succesfully subscribed")


# creates a message containing all the control variables and shares them via mqtt
def send_variables():
    data = {
        "max temp": MAX_TEMP,
        "min temp": MIN_TEMP,
        "cover time": COVER_TIME,
        "uncover time": UNCOVER_TIME
    }
    # the message is a JSON representation of the dictionary
    message = json.dumps(data)
    client.publish("iot-marco/data/variables", str(message))


# sends a message containing the 3 parameters read by the sensors via mqtt
def send_sensor_values(t, h, b):
    data = {
        "temperature": t,
        "humidity": h,
        "brightness": b
    }
    message = json.dumps(data)
    client.publish("iot-marco/data/sensors", str(message))


# sends a message containing the state of the devices via mqtt
def send_devices_data():
    data = {
        "fan": fan.state(),
        "sunshield": sunshield.state(),
        "led": led.state()
    }
    message = json.dumps(data)
    client.publish("iot-marco/data/devices", str(message))


# takes the new values from the received data and updates the global variables
def set_variables(data):
    global MAX_TEMP, MIN_TEMP, COVER_TIME, UNCOVER_TIME
    # the message received is a JSON object
    values = json.loads(data)
    MAX_TEMP = float(values["max temp"])
    MIN_TEMP = float(values["min temp"])
    COVER_TIME = int(values["cover time"])
    UNCOVER_TIME = int(values["uncover time"])
    # sends the values back to the user
    send_variables()


# called when any message is received
def read_data(client, data):
    message = data['message']
    topic = str(message.topic)
    payload = str(message.payload)

    if topic == "iot-marco/commands/set-variables":
        set_variables(payload)
    elif topic == "iot-marco/commands/get-variables":
        send_variables()
    elif topic == "iot-marco/commands/get-devices":
        send_devices_data()
    elif topic == "iot-marco/commands/fan":
        fan.control(payload)
    elif topic == "iot-marco/commands/sunshield":
        sunshield.control(payload)
    elif topic == "iot-marco/commands/led":
        led.control(payload)



#########################################
#           control functions           #
#########################################

def monitor_temperature(value):
    if value > MAX_TEMP:
        fan.start()
    elif value < MIN_TEMP and fan.is_running():
        fan.stop()


def is_bright(value):
    return value < 1000


def is_dark(value):
    return value > 2000


time_passed = 0

def monitor_brightness(value):
    global time_passed
    # turns on the control led when the lighting is insufficient
    if is_dark(value):
        led.on()
    else:
        led.off()
    # if the room is too bright it starts counting the passing of time.
    # When time_passed reaches the UNCOVER_TIME threshold the sunshield
    # will cover the device for a period of time equal to COVER_TIME
    if is_bright(value) and not sunshield.is_covering():
        time_passed += SLEEP_TIME
        if time_passed > UNCOVER_TIME:
            time_passed = 0
            sunshield.cover()
    elif sunshield.is_covering():
        time_passed += SLEEP_TIME
        if time_passed > COVER_TIME:
            time_passed = 0
            sunshield.uncover()
    else:
        time_passed = 0



#########################################
#                 setup                 #
#########################################

pinMode(PHOTORESISTOR_PIN, INPUT_ANALOG)

wifi.connect()

client.on(mqtt.SUBACK, confirm_subscribe)
client.connect("test.mosquitto.org", keepalive=0)
client.loop(read_data)
client.subscribe([["iot-marco/commands/#", 0]])

htu.start()
htu.init()

sunshield.init()



#########################################
#          program starts here          #
#########################################

while True:
    # reads the values
    temperature = htu.get_temp()
    humidity = htu.get_humid()
    brightness = analogRead(PHOTORESISTOR_PIN)

    # monitors them
    monitor_temperature(temperature)
    monitor_brightness(brightness)

    # sends them
    send_sensor_values(temperature, humidity, brightness)

    sleep(SLEEP_TIME * 1000)
