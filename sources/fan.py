class Fan():
    def __init__(self, pin, client):
        self._pin = pin
        self._client = client
        self._running = False


    def is_running(self):
        return self._running


    def start(self, force=False):
        if self._running:
            return False
        self._running = True
        digitalWrite(self._pin, HIGH)
        self._client.publish("iot-marco/data/fan", "running")
        return True


    def stop(self):
        if not self._running:
            return False
        self._running = False
        digitalWrite(self._pin, LOW)
        self._client.publish("iot-marco/data/fan", "not running")
        return True


    def state(self):
        return "running" if self._running else "not running"


    def control(self, command):
        if command == "get-state":
            self._client.publish("iot-marco/data/fan", self.state())
