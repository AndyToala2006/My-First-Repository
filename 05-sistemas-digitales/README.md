# 05 · Sistemas Digitales

Prácticas de sistemas embebidos con **Raspberry Pi Pico** y **MicroPython**,
simuladas en **Wokwi**. Se trabajan los protocolos de comunicación digital.

## 🧰 Tecnologías
- Raspberry Pi Pico (RP2040)
- MicroPython
- Wokwi (simulador online)
- Protocolos **I2C**, **SPI** y **UART**

## 📂 Archivos
| Archivo | Descripción |
|---------|-------------|
| `diagram.json` | Conexiones del Pico, LCD I2C, potenciómetro y chip MCP3008 |
| `main.py` | Lectura SPI, despliegue I2C, envío UART y control A/B |
| `lcd_api.py` · `i2c_lcd.py` | Driver del LCD 16x2 por I2C |
| `mcp3008.chip.json` · `mcp3008.chip.c` | Chip ADC SPI simulado |
| `wokwi.toml` | Configuración del proyecto Wokwi |

## ▶️ Cómo simular
1. Instala la extensión **Wokwi** en VS Code (o usa [wokwi.com](https://wokwi.com)).
2. Abre esta carpeta y ejecuta la simulación.

> El chip MCP3008 es una versión simplificada (siempre devuelve CH0).
> Si tu LCD usa otra dirección I2C, cambia `LCD_ADDR` en `main.py`.
