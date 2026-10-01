# E-OSCI V1 - ESP32 Smart Oscilloscope

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview
A low-cost, portable digital oscilloscope using ESP32-WROOM-32.

## Features
- 1 Msps sampling via I2S + DMA
- 2.8" ILI9341 TFT display
- WiFi web interface (browser-based waveform viewer)
- Automatic measurements (Vpp, Vrms, Vavg, Frequency, Period, Duty Cycle)
- Trigger engine (Auto/Normal/Single, Rising/Falling edge)
- PWM-based signal generator
- SD card CSV waveform logging
- 4-button UI menu system

## Quick Start
1. Flash firmware using Arduino IDE.
2. Connect components according to pin map.
3. Power on and connect to WiFi AP "E-OSCI-V1".
4. Navigate to http://192.168.4.1 for web interface.

## Pin Map
| Function        | GPIO |
|-----------------|------|
| TFT_CS          | 15   |
| TFT_DC          | 2    |
| TFT_RST         | 4    |
| TFT_MOSI        | 23   |
| TFT_SCLK        | 18   |
| TFT_MISO        | 19   |
| SD_CS           | 5    |
| BTN_MENU        | 32   |
| BTN_UP          | 33   |
| BTN_DOWN        | 25   |
| BTN_SELECT      | 26   |
| ADC_INPUT       | 34   |
| SIGGEN_OUT      | 27   |

## License
MIT License. Copyright (c) 2026 P.P.N.Pathirana
