Wokwi Pico - SPI + I2C + UART (Simulacion)

Archivos:
- diagram.json: conexiones del Pico, LCD I2C, potenciometro y el chip MCP3008 simulado.
- main.py: lectura SPI, despliegue I2C, envio UART y control A/B.
- lcd_api.py / i2c_lcd.py: driver del LCD 16x2 por I2C.
- mcp3008.chip.json / mcp3008.chip.c: chip SPI simulado.

Notas:
- El chip MCP3008 es una version simplificada: siempre devuelve CH0.
- Si tu LCD usa otra direccion I2C, cambia LCD_ADDR en main.py.
