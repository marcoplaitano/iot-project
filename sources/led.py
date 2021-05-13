class Led():
    def __init__(self, pin, client):
        self._pin = pin
        self._client = client
        self._is_on = False
        pinMode(self._pin, OUTPUT)


    def off(self):
        if self._is_on:
            self._is_on = False
            digitalWrite(self._pin, LOW)
            self._client.publish("iot-marco/data/led", "off")


    def on(self):
        if not self._is_on:
            self._is_on = True
            digitalWrite(self._pin, HIGH)
            self._client.publish("iot-marco/data/led", "on")


    def toggle(self):
        if self._is_on:
            self.off()
        else:
            self.on()


    def state(self):
        return "on" if self._is_on else "off"


    def control(self, command):
        if command == "get-state":
            self._client.publish("iot-marco/data/led", self.state())
