#include "wokwi-api.h"
#include <stdlib.h>

// Simple MCP3008-like SPI device for simulation.
// It ignores the requested channel and always returns CH0 (potentiometer).
// This keeps the SPI demo simple while still exercising the bus.

typedef struct {
  pin_t cs;
  pin_t ch[8];
  spi_dev_t spi;
  uint8_t tx[3];
} chip_state_t;

static uint16_t clamp_u16(int value) {
  if (value < 0) return 0;
  if (value > 1023) return 1023;
  return (uint16_t)value;
}

static uint16_t read_channel0(chip_state_t *state) {
  // Analog API returns voltage in volts (0.0 .. 5.0)
  float v = pin_adc_read(state->ch[0]);
  int raw = (int)(v * 1023.0f / 5.0f + 0.5f);
  return clamp_u16(raw);
}

static void spi_done(void *user_data, spi_dev_t spi, uint8_t *buffer, uint32_t count) {
  chip_state_t *state = (chip_state_t *)user_data;
  // If CS is still low and the master continues clocking, keep sending data.
  if (pin_read(state->cs) == LOW) {
    spi_start(state->spi, state->tx, 3);
  }
}

static void cs_changed(void *user_data, pin_t pin, uint32_t value) {
  chip_state_t *state = (chip_state_t *)user_data;
  if (value == LOW) {
    uint16_t adc = read_channel0(state);
    state->tx[0] = 0x00;
    state->tx[1] = (uint8_t)((adc >> 8) & 0x03);
    state->tx[2] = (uint8_t)(adc & 0xFF);
    spi_start(state->spi, state->tx, 3);
  } else {
    spi_stop(state->spi);
  }
}

void chip_init(void) {
  chip_state_t *state = (chip_state_t *)malloc(sizeof(chip_state_t));

  state->cs = pin_init("CS", INPUT_PULLUP);
  state->ch[0] = pin_init("CH0", ANALOG);
  state->ch[1] = pin_init("CH1", ANALOG);
  state->ch[2] = pin_init("CH2", ANALOG);
  state->ch[3] = pin_init("CH3", ANALOG);
  state->ch[4] = pin_init("CH4", ANALOG);
  state->ch[5] = pin_init("CH5", ANALOG);
  state->ch[6] = pin_init("CH6", ANALOG);
  state->ch[7] = pin_init("CH7", ANALOG);

  spi_config_t cfg = {
    .sck = pin_init("CLK", INPUT),
    .mosi = pin_init("DIN", INPUT),
    .miso = pin_init("DOUT", OUTPUT),
    .mode = 0,
    .done = spi_done,
    .user_data = state,
  };
  state->spi = spi_init(&cfg);

  pin_watch(state->cs, cs_changed, state);
}
