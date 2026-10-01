// ================================================================
// E-OSCI V1 - Configuration
// Author: P.P.N.Pathirana
// ================================================================

#ifndef CONFIG_H
#define CONFIG_H

// Pin Map
#define PIN_TFT_CS     15
#define PIN_TFT_DC     2
#define PIN_TFT_RST    4
#define PIN_TFT_MOSI   23
#define PIN_TFT_SCLK   18
#define PIN_TFT_MISO   19
#define PIN_SD_CS      5
#define PIN_BTN_MENU   32
#define PIN_BTN_UP     33
#define PIN_BTN_DOWN   25
#define PIN_BTN_SELECT 26
#define PIN_ADC_INPUT  34
#define PIN_SIGGEN_OUT 27

// ADC Settings
#define ADC_SAMPLE_RATE 1000000
#define BUFFER_SIZE     2048
#define VOLTAGE_SCALE   ((3.3 / 4095.0) * 11.0)

// Colors
#define COLOR_BG       0x0000
#define COLOR_GRID     0x4208
#define COLOR_WAVE     0x07E0
#define COLOR_TEXT     0xFFFF
#define COLOR_ACCENT   0xF800

#endif // CONFIG_H
