import i2c

HTU_I2C_ADDRESS = 0x40

HTU21D_TRIGGER_TEMP_NOHOLD = 0xF3
HTU21D_TRIGGER_HUMD_NOHOLD = 0xF5
HTU21D_WRITE_USER_REG = 0xE6
HTU21D_READ_USER_REG = 0xE7
HTU21D_SOFT_RESET = 0xFE

BITRES_HTU_RH_12_TEMP14 = 0x02
BITRES_HTU_RH_8_TEMP12 = 0x03
BITRES_HTU_RH_10_TEMP13 = 0x82
BITRES_HTU_RH_11_TEMP11 = 0x83

BITRES_HTU_LIST = [BITRES_HTU_RH_12_TEMP14, BITRES_HTU_RH_8_TEMP12, BITRES_HTU_RH_10_TEMP13, BITRES_HTU_RH_11_TEMP11]


class HTU21D(i2c.I2C):
    def __init__(self, i2cdrv, addr=HTU_I2C_ADDRESS, clk=400000):
        i2c.I2C.__init__(self, i2cdrv, addr, clk)
        self._addr = addr


    def init(self, res=0):
        self.write_bytes(HTU21D_SOFT_RESET)
        self.write_bytes(HTU21D_WRITE_USER_REG, BITRES_HTU_LIST[0])
        self._delay_t = 50
        self._delay_h = 16
        self.write_read(HTU21D_READ_USER_REG,1)


    def get_temp(self):
        self.write_bytes(HTU21D_TRIGGER_TEMP_NOHOLD)
        sleep(self._delay_t)
        data = self.read(2)
        raw = (data[0] << 8) | (data[1] & 0xFC)
        temp = - 46.85 + (175.72 * raw) / 65536
        return temp


    def get_humid(self):
        self.write_bytes(HTU21D_TRIGGER_HUMD_NOHOLD)
        sleep(self._delay_h)
        data = self.read(2)
        raw = (data[0] << 8) | (data[1] & 0xFC)
        humid = - 6 + (125 * raw) / 65536
        return humid
