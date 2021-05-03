class LED():
    def __init__(self, pin, client):
        self._pin = pin
        self._client = client
        self._is_on = False
        pinMode(self._pin, OUTPUT)


    def off(self):
        if self._is_on:
            self._is_on = False
            digitalWrite(self._pin, LOW)
            self._client.publish("led", "off")


    def on(self):
        if not self._is_on:
            self._is_on = True
            digitalWrite(self._pin, HIGH)
            self._client.publish("led", "on")


    def toggle(self):
        if self._is_on:
            self.off()
        else:
            self.on()


    def control(self, command):
        if command == "get-state":
            state = "on" if self._is_on else "off"
            self._client.publish("led", state)
            return True
        else:
            return False
