import pwm


PERIOD = 20000
COVER_PW = 1700
UNCOVER_PW = 700


class Sunshield():
    def __init__(self, pin, client):
        self._pin = pin
        self._client = client
        self._position = UNCOVER_PW
        pinMode(self._pin, OUTPUT)
        pwm.write(self._pin, PERIOD, UNCOVER_PW, MICROS)


    def _move_to(self, pulse):
        pwm.write(self._pin, PERIOD, pulse, MICROS)
        self._position = pulse


    def is_covering(self):
        return self._position != UNCOVER_PW


    def cover(self):
        if self.is_covering():
            return
        self._move_to(COVER_PW)
        self._client.publish("iot-marco/data/sunshield", "covering")


    def uncover(self):
        if not self.is_covering():
            return
        self._move_to(UNCOVER_PW)
        self._client.publish("iot-marco/data/sunshield", "not covering")


    def state(self):
        return "covering" if self.is_covering() else "not covering"


    def control(self, command):
        if command == "get-state":
            self._client.publish("iot-marco/data/sunshield", self.state())
        elif command == "cover":
            self.cover()
        elif command == "uncover":
            self.uncover()
