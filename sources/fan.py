class Fan():
    """
    This class represents the cooling fan controlled by the relay
    connected to a specific digital pin. It also needs the mqtt client
    so that it can send various notifications to the user.
    """
    def __init__(self, pin, client):
        self._pin = pin
        pinMode(self._pin, OUTPUT)
        self._client = client
        # not running by default
        self._running = False
        digitalWrite(self._pin, LOW)


    def is_running(self):
        """
        Returns wether the fan is currently running or not.
        """
        return self._running


    def start(self):
        """
        Starts the fan and notifies this change to the user via MQTT.
        """
        if self._running:
            return
        digitalWrite(self._pin, HIGH)
        self._running = True
        self._client.publish("iot-marco/data/fan", "running")


    def stop(self):
        """
        Starts the fan and notifies this change to the user via MQTT.
        """
        if not self._running:
            return
        digitalWrite(self._pin, LOW)
        self._running = False
        self._client.publish("iot-marco/data/fan", "not running")


    def state(self):
        """
        Returns a string representing the current state of the device.
        """
        return "running" if self._running else "not running"


    def control(self, command):
        """
        Usually called when a message is received in the "iot-marco/commands/fan" subtopic.
        The payload of the message (the command parameter here) is the action to perform.
        """
        if command == "get-state":
            self._client.publish("iot-marco/data/fan", self.state())
        elif command == "start":
            self.start()
        elif command == "stop":
            self.stop()
