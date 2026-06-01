from machine import Pin, SPI, I2C, UART
from time import sleep_ms
from i2c_lcd import I2cLcd

# ---- SPI (MCP3008) ----
spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(17, Pin.OUT, value=1)

# ---- I2C (LCD 16x2) ----
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400_000)

# Auto-detect LCD I2C address (commonly 0x27 or 0x3F)
_scan = i2c.scan()
print("I2C scan:", _scan)
if 0x27 in _scan:
    LCD_ADDR = 0x27
elif 0x3F in _scan:
    LCD_ADDR = 0x3F
else:
    LCD_ADDR = _scan[0] if _scan else 0x27

print("LCD_ADDR:", hex(LCD_ADDR))

lcd = None
try:
    lcd = I2cLcd(i2c, LCD_ADDR, 2, 16)
except Exception as e:
    print("LCD init failed:", e)

# ---- UART (Serial Monitor) ----
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

paused = False


def read_adc(channel=0):
    if channel < 0 or channel > 7:
        return 0
    tx = bytearray(3)
    rx = bytearray(3)
    tx[0] = 0x01
    tx[1] = (0x08 | channel) << 4
    tx[2] = 0x00
    cs(0)
    spi.write_readinto(tx, rx)
    cs(1)
    value = ((rx[1] & 0x03) << 8) | rx[2]
    return value


def handle_uart():
    global paused
    if uart.any():
        b = uart.read(1)
        if b == b'A':
            paused = True
        elif b == b'B':
            paused = False


def lcd_write(line1, line2):
    if lcd is None:
        return
    lcd.move_to(0, 0)
    lcd.putstr((line1 + " " * 16)[:16])
    lcd.move_to(0, 1)
    lcd.putstr((line2 + " " * 16)[:16])


lcd_write("SPI/I2C/UART", "Listo")
sleep_ms(500)

while True:
    handle_uart()

    if paused:
        lcd_write("PAUSA", "UART=A/B")
        uart.write(b"PAUSED\n")
        sleep_ms(500)
        continue

    adc = read_adc(0)
    msg = "Sensor: {}".format(adc)

    lcd_write("ADC CH0", msg)
    uart.write((msg + "\n").encode())

    sleep_ms(1000)
