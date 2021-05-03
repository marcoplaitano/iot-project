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
import sources.wifi_connection as wifi
import sources.mqtt as mqtt
import sources.htu21d as htu21d
import sources.led as leds
import sources.fan as fans
import sources.sunshield as sunshields



#########################################
#               variables               #
#########################################

PHOTORESISTOR_PIN = A1
STATUS_LED_PIN = D19
CONTROL_LED_PIN = D18

# threshold value: if the current temperature exceeds this value
# the cooling fan will be turned on
MAX_TEMP = 37.00
# when the fan is on and temperature reaches this value, the fan turns off
MIN_TEMP = 35.00
# === the following variables are measured in seconds ===
# time the device can remain uncovered with a high value of brightness
UNCOVER_TIME = 10
# time the device has to remain covered
COVER_TIME = 8
# time between each iteration of the main loop
SLEEP_TIME = 2

client = mqtt.MQTTClient("mydevice")

# temperature and humidity sensor
htu = htu21d.HTU21D(I2C0)

# cooling fan controlled by a relay on pin D23
fan = fans.FAN(D23, client)

# cardboard panel attached to a servo motor controlled by pin D17
sunshield = sunshields.SUNSHIELD(D17.PWM, client)

# led to activate if the room is too dark
led = leds.LED(CONTROL_LED_PIN, client)



#########################################
#               functions               #
#########################################

# function called in a thread to have a led blink continuosly
# to indicate that the program is running
def statusLed():
    pinMode(STATUS_LED_PIN, OUTPUT)
    while True:
        pinToggle(STATUS_LED_PIN)
        sleep(int(SLEEP_TIME/2) * 1000)


# creates a string containing all the control variables and shares them via mqtt
def send_variables():
    message = ' '.join([str(MAX_TEMP), str(MIN_TEMP), str(COVER_TIME), str(UNCOVER_TIME)])
    # retain is set to True so that whenever the user logs on the web app,
    # it always shows the updated values of these variables
    client.publish("variables", message, True)


# takes the new values from the received data and updates the global variables
def set_variables(data):
    global MAX_TEMP, MIN_TEMP, COVER_TIME, UNCOVER_TIME
    values = data.split(' ')
    MAX_TEMP = float(values[0])
    MIN_TEMP = float(values[1])
    COVER_TIME = int(values[2])
    UNCOVER_TIME = int(values[3])
    # sends the values back to the user
    send_variables()


# sends a string containing the 3 parameters read by the sensors via mqtt
# the order is: temperature, humidity, brightness
def send_sensor_values(values):
    message = ""
    for val in values:
        message += str(val) + ' '
    client.publish("sensors", message)


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
    # will cover the device for a time equal to COVER_TIME
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


# called when an mqtt message is received
def read_data(client, data):
    message = data['message']
    payload = str(message.payload)
    topic = str(message.topic)

    if topic == "iot/commands/variables":
        set_variables(payload)
    elif topic == "iot/commands/fan":
        fan.control(payload)
    elif topic == "iot/commands/sunshield":
        sunshield.control(payload)
    elif topic == "iot/commands/led":
        led.control(payload)



#########################################
#                 setup                 #
#########################################

# the pin connected to the photoresistor has to read analog data in input
pinMode(PHOTORESISTOR_PIN, INPUT_ANALOG)

# starts a new thread to have a led blink continuosly
thread(statusLed)

wifi.connect()

client.connect(read_data)
client.subscribe("iot/commands/#")

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
    send_sensor_values([temperature, humidity, brightness])

    sleep(SLEEP_TIME * 1000)
