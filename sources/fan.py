class Fan():
    def __init__(self, pin, client):
        self._pin = pin
        self._client = client
        self._running = False


    def is_running(self):
        return self._running


    def start(self):
        if self._running:
            return
        digitalWrite(self._pin, HIGH)
        self._running = True
        self._client.publish("iot-marco/data/fan", "running")


    def stop(self):
        if not self._running:
            return
        digitalWrite(self._pin, LOW)
        self._running = False
        self._client.publish("iot-marco/data/fan", "not running")


    def state(self):
        return "running" if self._running else "not running"


    def control(self, command):
        if command == "get-state":
            self._client.publish("iot-marco/data/fan", self.state())
