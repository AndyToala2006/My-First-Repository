from lcd_api import LcdApi
from time import sleep_ms

# I2C LCD driver for PCF8574 backpack
# Pin mapping: P0=RS, P1=RW, P2=E, P3=BACKLIGHT, P4..P7=DB4..DB7

class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = 0x08
        self.rs = 0x00
        self._init_done = False
        super().__init__(num_lines, num_columns)

    def _write_i2c(self, data):
        self.i2c.writeto(self.i2c_addr, bytes([data]))

    def _pulse_enable(self, data):
        self._write_i2c(data | 0x04)
        sleep_ms(1)
        self._write_i2c(data & ~0x04)
        sleep_ms(1)

    def _write4bits(self, data):
        self._write_i2c(data | self.backlight)
        self._pulse_enable(data | self.backlight)

    def _write_cmd(self, cmd):
        self.rs = 0x00
        self._write4bits((cmd & 0xF0))
        self._write4bits((cmd << 4) & 0xF0)

    def _write_data(self, data):
        self.rs = 0x01
        self._write4bits(self.rs | (data & 0xF0))
        self._write4bits(self.rs | ((data << 4) & 0xF0))

    def _init_lcd(self):
        sleep_ms(50)
        self._write4bits(0x30)
        sleep_ms(5)
        self._write4bits(0x30)
        sleep_ms(5)
        self._write4bits(0x30)
        sleep_ms(1)
        self._write4bits(0x20)  # 4-bit mode

        self._write_cmd(self.LCD_FUNCTION | self.LCD_FUNCTION_2LINES)
        self._write_cmd(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)
        self.clear()
        self._write_cmd(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC)
