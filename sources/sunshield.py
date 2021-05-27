import pwm


class Sunshield():
    """
    This class represents the cardboard panel attached to the Servo Motor.
    The actions of cover and uncover mask the real operations of turning
    the motor in either directions. It also needs the mqtt client so that
    it can send various notifications to the user.
    """
    def __init__(self, pin, client):
        self._pin = pin
        pinMode(self._pin, OUTPUT)
        self._client = client
        self._period = 20000
        self._cover_pw = 1700
        self._uncover_pw = 700
        # starts in "uncover" position by default
        self._position = self._uncover_pw
        pwm.write(self._pin, self._period, self._uncover_pw, MICROS)


    def _move_to(self, pulse):
        """
        Turns the motor to the desired pulse.
        """
        pwm.write(self._pin, self._period, pulse, MICROS)
        self._position = pulse


    def change_cover_pw(self, new_pw):
        """
        Lets the user specify a new value for cover_pw.
        """
        self._cover_pw = new_pw


    def change_uncover_pw(self, new_pw):
        """
        Lets the user specify a new value for uncover_pw.
        """
        self._uncover_pw = new_pw


    def is_covering(self):
        """
        Returns wether the sunshield is currently covering the photoresistor.
        """
        return self._position != self._uncover_pw


    def cover(self):
        """
        Turns the motor in the established position to cover the photoresistor.
        """
        if self.is_covering():
            return
        self._move_to(self._cover_pw)
        self._client.publish("iot-marco/data/sunshield", "covering")


    def uncover(self):
        """
        Turns the motor in the established position to uncover the photoresistor.
        """
        if not self.is_covering():
            return
        self._move_to(self._uncover_pw)
        self._client.publish("iot-marco/data/sunshield", "not covering")


    def state(self):
        """
        Returns a string representing the current state of the device.
        """
        return "covering" if self.is_covering() else "not covering"


    def control(self, command):
        """
        Usually called when a message is received in the "iot-marco/commands/sunshield" subtopic.
        The payload of the message (the command parameter here) is the action to perform.
        """
        if command == "get-state":
            self._client.publish("iot-marco/data/sunshield", self.state())
        elif command == "cover":
            self.cover()
        elif command == "uncover":
            self.uncover()
