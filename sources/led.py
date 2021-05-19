class Led():
    def __init__(self, pin, client):
        self._pin = pin
        self._client = client
        self._is_on = False
        pinMode(self._pin, OUTPUT)


    def off(self):
        if not self._is_on:
            return
        digitalWrite(self._pin, LOW)
        self._is_on = False
        self._client.publish("iot-marco/data/led", "off")


    def on(self):
        if self._is_on:
            return
        digitalWrite(self._pin, HIGH)
        self._is_on = True
        self._client.publish("iot-marco/data/led", "on")


    def state(self):
        return "on" if self._is_on else "off"


    def control(self, command):
        if command == "get-state":
            self._client.publish("iot-marco/data/led", self.state())
        elif command == "turn-on":
            self.on()
        elif command == "turn-off":
            self.off()
