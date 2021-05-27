import i2c


EN = 0b00000100

FUNCTION_SET = 0x32
LCD_8BIT = 0x16
LCD_2LINES = 0x08
DISPLAY_SET = 0x08
DISPLAY_ON = 0x04
DISPLAY_OFF = 0x00
CURSOR_ON = 0x02
CURSOR_OFF = 0x00
BLINK_ON = 0x01
BLINK_OFF = 0x00
ENTRY_MODE_SET = 0x04
LCD_INCREMENT = 0x02
LCD_NO_SHIFT = 0x00

CMD_MODE = 0
DATA_MODE = 1

BACKLIGHT_ON = 0x08
BACKLIGHT_OFF = 0x00

CLEAR = 0x01
HOME = 0x02
NEXT_LINE = 0xC0



class LcdDisplay():
    """
    This class lets the user write messages on a LCD 1602 I2C display.
    """
    def __init__(self, i2cdrv, addr=0x27, clk=400000):
        self.port = i2c.I2C(i2cdrv, addr, clk)
        self.port.start()
        self.backlight = BACKLIGHT_OFF
        self.width = 16
        self._command(FUNCTION_SET | LCD_8BIT | LCD_2LINES)
        self.backlight_off()
        self.clear()
        self._command(DISPLAY_SET | DISPLAY_ON | CURSOR_ON | BLINK_OFF)
        self._command(ENTRY_MODE_SET | LCD_INCREMENT | LCD_NO_SHIFT)
        self.backlight_on()


    def backlight_on(self):
        """
        Turns display's backlight on.
        """
        self.backlight = BACKLIGHT_ON
        self._write_bytes(0)


    def backlight_off(self):
        """
        Turns display's backlight off.
        """
        self.backlight = BACKLIGHT_OFF
        self._write_bytes(0)


    def clear(self):
        """
        Clears the display and moves the cursor back to the beginning.
        """
        self._command(CLEAR)
        sleep(1)
        self._home()


    def show(self, string):
        """
        Shows the given string on the display. If the string is too long
        it will stop at the last available cursor position.
        """
        msg = bytearray(string)
        for i in range(len(msg)):
            self._data(msg[i])
            if i == self.width - 1:
                self._command(NEXT_LINE)
            elif i == self.width * 2 - 1:
                return


    def _command(self, value):
        self._send(value, CMD_MODE)


    def _data(self, value):
        self._send(value, DATA_MODE)


    def _send(self, data, mode):
        highnib = data & 0xf0
        lownib = (data << 4) & 0xf0
        self._write((highnib) | mode)
        self._write((lownib) | mode)


    def _write(self, data):
        self._write_bytes(data)
        self._pulse_enable(data)


    def _write_bytes(self, values):
        self.port.write(values | self.backlight)


    def _pulse_enable(self, data):
        self._write_bytes(data | EN)
        sleep(1)
        self._write_bytes(data & ~EN)
        sleep(1)


    def _home(self):
        self._command(HOME)
        sleep(1)
