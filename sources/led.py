class Led():
    """
    This class represents a led connected to one of the board's digital pins.
    It also needs the mqtt client in order to send notifications to the user.
    """
    def __init__(self, pin, client):
        self._pin = pin
        pinMode(self._pin, OUTPUT)
        self._client = client
        # turned off by default
        self._is_on = False
        digitalWrite(self._pin, LOW)


    def on(self):
        """
        Turns the led on and notifies the user via MQTT.
        """
        if self._is_on:
            return
        digitalWrite(self._pin, HIGH)
        self._is_on = True
        self._client.publish("iot-marco/data/led", "on")


    def off(self):
        """
        Turns the led off and notifies the user via MQTT.
        """
        if not self._is_on:
            return
        digitalWrite(self._pin, LOW)
        self._is_on = False
        self._client.publish("iot-marco/data/led", "off")


    def state(self):
        """
        Returns a string representing the current state of the device.
        """
        return "on" if self._is_on else "off"


    def control(self, command):
        """
        Usually called when a message is received in the "iot-marco/commands/led" subtopic.
        The payload of the message (the command parameter here) is the action to perform.
        """
        if command == "get-state":
            self._client.publish("iot-marco/data/led", self.state())
        elif command == "turn-on":
            self.on()
        elif command == "turn-off":
            self.off()
