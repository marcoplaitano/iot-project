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
        self._client.publish("sunshield", "covering")
        return True


    def uncover(self):
        if not self.is_covering():
            return False
        self._motor.moveToDegree(UNCOVER_DEGREE)
        self._client.publish("sunshield", "not covering")
        return True


    def toggle(self):
        if self.is_covering():
            self.uncover()
        else:
            self.cover()


    def control(self, command):
        if command == "get-state":
            state = "covering" if self.is_covering() else "not covering"
            self._client.publish("sunshield", state)
            return True
        else:
            return False
