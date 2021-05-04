from servo import servo


COVER_DEGREE = 90
UNCOVER_DEGREE = 0


class SUNSHIELD():
    def __init__(self, pin, client):
        self._motor = servo.Servo(pin)
        self._client = client
        self._covering = False


    def init(self):
        self._motor.attach()
        self._motor.moveToDegree(0)


    def is_covering(self):
        return self._motor.getCurrentDegree() != UNCOVER_DEGREE


    def cover(self):
        if self.is_covering():
            return False
        self._motor.moveToDegree(COVER_DEGREE)
        self._client.publish("iot-marco/data/sunshield", "covering")
        return True


    def uncover(self):
        if not self.is_covering():
            return False
        self._motor.moveToDegree(UNCOVER_DEGREE)
        self._client.publish("iot-marco/data/sunshield", "not covering")
        return True


    def toggle(self):
        if self.is_covering():
            self.uncover()
        else:
            self.cover()


    def state(self):
        return "covering" if self.is_covering() else "not covering"


    def control(self, command):
        if command == "get-state":
            self._client.publish("iot-marco/data/sunshield", self.state())
