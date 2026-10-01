import os

base_dir = r"C:\Users\Pasindu\.gemini\antigravity\scratch\E-OSCI-V1"

files = {
    "LICENSE": """MIT License

Copyright (c) 2026 P.P.N.Pathirana

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
    ".gitignore": """# Arduino build files
build/
*.bin
*.elf
*.hex

# OS generated files
.DS_Store
Thumbs.db
""",
    "CHANGELOG.md": """# Changelog

## [1.0.0] - 2026-10-01
- Initial release of E-OSCI V1
- ESP32 I2S DMA sampling at 1 Msps
- ILI9341 display support
- WiFi web interface
- Measurement features
- SD card logging
""",
    "firmware/config.h": """// ================================================================
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
""",
    "firmware/adc_sampler.h": """// ================================================================
// E-OSCI V1 - ADC Sampler Header
// Author: P.P.N.Pathirana
// ================================================================

#ifndef ADC_SAMPLER_H
#define ADC_SAMPLER_H

#include <stdint.h>
#include <stdbool.h>

extern volatile uint16_t adcBuffer[];

void adc_sampler_init();
bool adc_captureOnce();

#endif // ADC_SAMPLER_H
""",
    "firmware/adc_sampler.cpp": """// ================================================================
// E-OSCI V1 - ADC Sampler Module
// Author: P.P.N.Pathirana
// ================================================================

#include "adc_sampler.h"
#include "config.h"
#include <Arduino.h>
#include <driver/i2s.h>

volatile uint16_t adcBuffer[BUFFER_SIZE];

void adc_sampler_init() {
    Serial.println("[ADC] Initializing I2S ADC...");
    
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX | I2S_MODE_ADC_BUILT_IN),
        .sample_rate = ADC_SAMPLE_RATE,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_RIGHT,
        .communication_format = I2S_COMM_FORMAT_I2S_MSB,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 4,
        .dma_buf_len = 512,
        .use_apll = false,
        .tx_desc_auto_clear = false,
        .fixed_mclk = 0
    };
    
    i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
    i2s_set_adc_mode(ADC_UNIT_1, ADC1_CHANNEL_6); // GPIO 34
    i2s_adc_enable(I2S_NUM_0);
}

bool adc_captureOnce() {
    size_t bytesRead;
    i2s_read(I2S_NUM_0, (void*)adcBuffer, BUFFER_SIZE * sizeof(uint16_t), &bytesRead, portMAX_DELAY);
    
    for (int i = 0; i < BUFFER_SIZE; i++) {
        adcBuffer[i] &= 0x0FFF;
    }
    
    return bytesRead == (BUFFER_SIZE * sizeof(uint16_t));
}
""",
    "firmware/trigger.h": """// ================================================================
// E-OSCI V1 - Trigger Engine Header
// Author: P.P.N.Pathirana
// ================================================================

#ifndef TRIGGER_H
#define TRIGGER_H

#include <stdint.h>

typedef enum {
    TRIG_RISING,
    TRIG_FALLING
} TriggerEdge_t;

void trigger_setLevel(uint16_t level);
void trigger_setEdge(TriggerEdge_t edge);
int trigger_find(volatile uint16_t* buffer, int length);

#endif // TRIGGER_H
""",
    "firmware/trigger.cpp": """// ================================================================
// E-OSCI V1 - Trigger Engine Module
// Author: P.P.N.Pathirana
// ================================================================

#include "trigger.h"

static uint16_t trigLevel = 2048;
static TriggerEdge_t trigEdge = TRIG_RISING;

void trigger_setLevel(uint16_t level) {
    trigLevel = level;
}

void trigger_setEdge(TriggerEdge_t edge) {
    trigEdge = edge;
}

int trigger_find(volatile uint16_t* buffer, int length) {
    int searchLen = length / 2;
    for (int i = 1; i < searchLen; i++) {
        if (trigEdge == TRIG_RISING) {
            if (buffer[i - 1] < trigLevel && buffer[i] >= trigLevel) {
                return i;
            }
        } else {
            if (buffer[i - 1] > trigLevel && buffer[i] <= trigLevel) {
                return i;
            }
        }
    }
    return -1;
}
""",
    "firmware/measurements.h": """// ================================================================
// E-OSCI V1 - Measurements Header
// Author: P.P.N.Pathirana
// ================================================================

#ifndef MEASUREMENTS_H
#define MEASUREMENTS_H

#include <stdint.h>
#include <stdbool.h>

typedef struct {
    float vpp;
    float vmax;
    float vmin;
    float vavg;
    float vrms;
    float frequency;
    float period_ms;
    float dutyCycle;
    bool valid;
} MeasResult_t;

void measurements_calc(volatile uint16_t* buffer, int length, MeasResult_t* res);

#endif // MEASUREMENTS_H
""",
    "firmware/measurements.cpp": """// ================================================================
// E-OSCI V1 - Measurements Module
// Author: P.P.N.Pathirana
// ================================================================

#include "measurements.h"
#include "config.h"
#include <math.h>

void measurements_calc(volatile uint16_t* buffer, int length, MeasResult_t* res) {
    uint16_t maxVal = 0;
    uint16_t minVal = 4095;
    uint32_t sum = 0;
    uint64_t sumSq = 0;
    
    for (int i = 0; i < length; i++) {
        uint16_t val = buffer[i];
        if (val > maxVal) maxVal = val;
        if (val < minVal) minVal = val;
        sum += val;
        sumSq += (val * val);
    }
    
    res->vmax = maxVal * VOLTAGE_SCALE;
    res->vmin = minVal * VOLTAGE_SCALE;
    res->vpp = res->vmax - res->vmin;
    res->vavg = (sum / (float)length) * VOLTAGE_SCALE;
    res->vrms = sqrt((float)sumSq / length) * VOLTAGE_SCALE;
    
    uint16_t midVal = (maxVal + minVal) / 2;
    int crossings = 0;
    int firstCross = -1;
    int lastCross = -1;
    int highCount = 0;
    
    for (int i = 1; i < length; i++) {
        if (buffer[i] >= midVal) highCount++;
        
        if (buffer[i - 1] < midVal && buffer[i] >= midVal) {
            crossings++;
            if (firstCross == -1) firstCross = i;
            lastCross = i;
        }
    }
    
    res->dutyCycle = ((float)highCount / length) * 100.0;
    
    if (crossings >= 2) {
        float periods = crossings - 1;
        float samplesPerPeriod = (lastCross - firstCross) / periods;
        res->frequency = ADC_SAMPLE_RATE / samplesPerPeriod;
        res->period_ms = 1000.0 / res->frequency;
        res->valid = true;
    } else {
        res->frequency = 0;
        res->period_ms = 0;
        res->valid = false;
    }
}
""",
    "firmware/display.h": """// ================================================================
// E-OSCI V1 - Display Header
// Author: P.P.N.Pathirana
// ================================================================

#ifndef DISPLAY_H
#define DISPLAY_H

#include "measurements.h"
#include <stdint.h>

void display_init();
void display_splash();
void display_status(const char* msg);
void display_clear();
void display_grid();
void display_waveform(volatile uint16_t* buffer, int length);
void display_info(MeasResult_t* meas);

#endif // DISPLAY_H
""",
    "firmware/display.cpp": """// ================================================================
// E-OSCI V1 - Display Module
// Author: P.P.N.Pathirana
// ================================================================

#include "display.h"
#include "config.h"
#include <TFT_eSPI.h>
#include <Arduino.h>

static TFT_eSPI tft = TFT_eSPI();

void display_init() {
    tft.init();
    tft.setRotation(1);
    tft.fillScreen(COLOR_BG);
}

void display_splash() {
    tft.fillScreen(COLOR_BG);
    tft.setTextColor(COLOR_ACCENT);
    tft.setTextSize(3);
    tft.setCursor(50, 80);
    tft.print("E-OSCI V1");
    
    tft.setTextColor(COLOR_TEXT);
    tft.setTextSize(2);
    tft.setCursor(30, 130);
    tft.print("ESP32 Smart Oscilloscope");
    
    tft.setTextSize(1);
    tft.setCursor(80, 180);
    tft.print("By: P.P.N.Pathirana");
    
    delay(2000);
}

void display_status(const char* msg) {
    tft.fillRect(0, 220, 320, 20, COLOR_BG);
    tft.setTextColor(COLOR_TEXT);
    tft.setTextSize(1);
    tft.setCursor(10, 225);
    tft.print(msg);
}

void display_clear() {
    tft.fillScreen(COLOR_BG);
}

void display_grid() {
    for (int x = 0; x <= 320; x += 40) {
        tft.drawLine(x, 0, x, 240, COLOR_GRID);
    }
    for (int y = 0; y <= 240; y += 40) {
        tft.drawLine(0, y, 320, y, COLOR_GRID);
    }
}

void display_waveform(volatile uint16_t* buffer, int length) {
    int prevX = 0;
    int prevY = 240 - (buffer[0] * 240 / 4095);
    
    for (int i = 1; i < length && i < 320; i++) {
        int x = i;
        int y = 240 - (buffer[i] * 240 / 4095);
        tft.drawLine(prevX, prevY, x, y, COLOR_WAVE);
        prevX = x;
        prevY = y;
    }
}

void display_info(MeasResult_t* meas) {
    tft.setTextColor(COLOR_TEXT, COLOR_BG);
    tft.setTextSize(1);
    
    tft.setCursor(10, 10);
    tft.printf("Vpp: %.2fV", meas->vpp);
    tft.setCursor(100, 10);
    tft.printf("Freq: %.0fHz", meas->frequency);
    tft.setCursor(200, 10);
    tft.printf("Duty: %.1f%%", meas->dutyCycle);
    
    tft.setCursor(10, 220);
    tft.printf("Vrms: %.2fV  Vavg: %.2fV", meas->vrms, meas->vavg);
}
""",
    "firmware/signal_gen.h": """// ================================================================
// E-OSCI V1 - Signal Generator Header
// Author: P.P.N.Pathirana
// ================================================================

#ifndef SIGNAL_GEN_H
#define SIGNAL_GEN_H

#include <stdint.h>

void siggen_init();
void siggen_setFreq(float freqHz);
void siggen_stop();

#endif // SIGNAL_GEN_H
""",
    "firmware/signal_gen.cpp": """// ================================================================
// E-OSCI V1 - Signal Generator Module
// Author: P.P.N.Pathirana
// ================================================================

#include "signal_gen.h"
#include "config.h"
#include <Arduino.h>

static const int pwmChannel = 0;
static const int pwmResolution = 8;

void siggen_init() {
    ledcSetup(pwmChannel, 100000, pwmResolution);
    ledcAttachPin(PIN_SIGGEN_OUT, pwmChannel);
}

void siggen_setFreq(float freqHz) {
    ledcWriteTone(pwmChannel, freqHz);
}

void siggen_stop() {
    ledcWriteTone(pwmChannel, 0);
}
""",
    "firmware/web_server.h": """// ================================================================
// E-OSCI V1 - Web Server Header
// Author: P.P.N.Pathirana
// ================================================================

#ifndef WEB_SERVER_H
#define WEB_SERVER_H

#include <stdint.h>

void web_init();
void web_loop();
void web_sendWaveform(volatile uint16_t* buffer, int length);

#endif // WEB_SERVER_H
""",
    "firmware/web_server.cpp": """// ================================================================
// E-OSCI V1 - Web Server Module
// Author: P.P.N.Pathirana
// ================================================================

#include "web_server.h"
#include <WiFi.h>
#include <WebServer.h>

static WebServer server(80);
static volatile uint16_t* lastBuffer = NULL;
static int lastBufferLen = 0;

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <title>E-OSCI V1</title>
  <style>
    body { background-color: #111; color: #fff; font-family: monospace; text-align: center; }
    canvas { background-color: #000; border: 1px solid #444; }
  </style>
</head>
<body>
  <h2>E-OSCI V1 - Web Viewer</h2>
  <canvas id="oscCanvas" width="800" height="400"></canvas>
  <div id="readouts">Connecting...</div>
  <script>
    const canvas = document.getElementById('oscCanvas');
    const ctx = canvas.getContext('2d');
    
    function drawGrid() {
        ctx.strokeStyle = '#222';
        ctx.beginPath();
        for(let x=0; x<=800; x+=100) { ctx.moveTo(x, 0); ctx.lineTo(x, 400); }
        for(let y=0; y<=400; y+=50) { ctx.moveTo(0, y); ctx.lineTo(800, y); }
        ctx.stroke();
    }
    
    async function fetchData() {
        try {
            const res = await fetch('/data');
            const arrayBuffer = await res.arrayBuffer();
            const data = new Uint16Array(arrayBuffer);
            
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, 800, 400);
            drawGrid();
            
            ctx.strokeStyle = '#0f0';
            ctx.beginPath();
            for(let i=0; i<data.length && i<800; i++) {
                let y = 400 - (data[i] * 400 / 4095);
                if(i===0) ctx.moveTo(i, y);
                else ctx.lineTo(i, y);
            }
            ctx.stroke();
            
            document.getElementById('readouts').innerText = "Live Waveform Updated";
        } catch(e) {
            console.log(e);
        }
        setTimeout(fetchData, 100);
    }
    fetchData();
  </script>
</body>
</html>
)rawliteral";

void handleRoot() {
    server.send(200, "text/html", index_html);
}

void handleData() {
    if (lastBuffer != NULL && lastBufferLen > 0) {
        server.send_P(200, "application/octet-stream", (const char*)lastBuffer, lastBufferLen * 2);
    } else {
        server.send(404, "text/plain", "No data");
    }
}

void web_init() {
    WiFi.softAP("E-OSCI-V1", "oscope1234");
    server.on("/", handleRoot);
    server.on("/data", handleData);
    server.begin();
    Serial.println("[WiFi] AP Started: E-OSCI-V1");
}

void web_loop() {
    server.handleClient();
}

void web_sendWaveform(volatile uint16_t* buffer, int length) {
    lastBuffer = buffer;
    lastBufferLen = length;
}
""",
    "firmware/sd_logger.h": """// ================================================================
// E-OSCI V1 - SD Logger Header
// Author: P.P.N.Pathirana
// ================================================================

#ifndef SD_LOGGER_H
#define SD_LOGGER_H

#include <stdint.h>

void sd_init();
void sd_logWaveform(volatile uint16_t* buffer, int length);

#endif // SD_LOGGER_H
""",
    "firmware/sd_logger.cpp": """// ================================================================
// E-OSCI V1 - SD Logger Module
// Author: P.P.N.Pathirana
// ================================================================

#include "sd_logger.h"
#include "config.h"
#include <SPI.h>
#include <SD.h>
#include <Arduino.h>

static bool sdReady = false;

void sd_init() {
    if (!SD.begin(PIN_SD_CS)) {
        Serial.println("[SD] Mount failed");
        sdReady = false;
        return;
    }
    Serial.println("[SD] Card initialized");
    sdReady = true;
}

void sd_logWaveform(volatile uint16_t* buffer, int length) {
    if (!sdReady) return;
    
    File file = SD.open("/wave.csv", FILE_APPEND);
    if (!file) {
        Serial.println("[SD] Failed to open wave.csv for appending");
        return;
    }
    
    for (int i = 0; i < length; i++) {
        file.print(buffer[i]);
        if (i < length - 1) file.print(",");
    }
    file.println();
    file.close();
}
""",
    "firmware/ui_menu.h": """// ================================================================
// E-OSCI V1 - UI Menu Header
// Author: P.P.N.Pathirana
// ================================================================

#ifndef UI_MENU_H
#define UI_MENU_H

void ui_init();
void ui_loop();

#endif // UI_MENU_H
""",
    "firmware/ui_menu.cpp": """// ================================================================
// E-OSCI V1 - UI Menu Module
// Author: P.P.N.Pathirana
// ================================================================

#include "ui_menu.h"
#include "config.h"
#include <Button2.h>
#include <Arduino.h>

static Button2 btnMenu(PIN_BTN_MENU);
static Button2 btnUp(PIN_BTN_UP);
static Button2 btnDown(PIN_BTN_DOWN);
static Button2 btnSelect(PIN_BTN_SELECT);

void ui_init() {
    btnMenu.setDebounceTime(50);
    btnUp.setDebounceTime(50);
    btnDown.setDebounceTime(50);
    btnSelect.setDebounceTime(50);
    
    btnMenu.setTapHandler([](Button2& b) {
        Serial.println("[UI] Menu short press");
    });
    
    btnMenu.setLongClickHandler([](Button2& b) {
        Serial.println("[UI] Menu long press");
    });
}

void ui_loop() {
    btnMenu.loop();
    btnUp.loop();
    btnDown.loop();
    btnSelect.loop();
}
""",
    "firmware/E_OSCI_V1.ino": """// ================================================================
// E-OSCI V1 - Main Sketch
// Author: P.P.N.Pathirana
// ================================================================

#include <Arduino.h>
#include "config.h"
#include "adc_sampler.h"
#include "trigger.h"
#include "measurements.h"
#include "display.h"
#include "signal_gen.h"
#include "web_server.h"
#include "sd_logger.h"
#include "ui_menu.h"

MeasResult_t currentMeas;
uint32_t sampleCount = 0;

void setup() {
    Serial.begin(115200);
    Serial.println("=================================");
    Serial.println("E-OSCI V1 - ESP32 Oscilloscope");
    Serial.println("Author: P.P.N.Pathirana");
    Serial.println("=================================");

    display_init();
    display_splash();

    ui_init();
    sd_init();
    siggen_init();
    adc_sampler_init();
    web_init();

    siggen_setFreq(100000); // 100 kHz test signal
    
    Serial.println("[BOOT] System ready");
    display_status("Ready...");
}

void loop() {
    web_loop();
    ui_loop();

    if (adc_captureOnce()) {
        int trigIdx = trigger_find(adcBuffer, BUFFER_SIZE);
        
        if (trigIdx >= 0) {
            measurements_calc(adcBuffer, BUFFER_SIZE, &currentMeas);
            display_clear();
            display_grid();
            display_waveform(adcBuffer + trigIdx, BUFFER_SIZE - trigIdx);
            display_info(&currentMeas);
            web_sendWaveform(adcBuffer, BUFFER_SIZE);
            sampleCount++;
        }
    }
}
""",
    "web/index.html": """<!-- Web assets mapped to PROGMEM in firmware/web_server.cpp -->""",
    "web/style.css": """/* Combined into index.html */""",
    "web/script.js": """/* Combined into index.html */""",
    "hardware/bom.csv": """Item,Description,Quantity,Price Est (LKR)
ESP32-WROOM-32,Microcontroller DevKit,1,2500
ILI9341 2.8",SPI TFT Display,1,3000
SD Card Module,MicroSD SPI,1,800
Push Buttons,Tactile Switches,4,200
Resistors,100k & 10k,2,50
PCB/Breadboard,Prototyping,1,500
Total,,,7050""",
    "hardware/schematic.md": """# E-OSCI V1 Schematic

- ESP32 GPIO34 -> 100k/10k Voltage Divider -> Signal Input
- ESP32 SPI Pins -> ILI9341 Display & SD Card
- ESP32 GPIO32,33,25,26 -> Push Buttons -> GND
""",
    "hardware/pinout.md": """# Pinout Map

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
""",
    "docs/SETUP.md": """# Setup Instructions
1. Install Arduino IDE
2. Add ESP32 Core
3. Install TFT_eSPI and Button2 libraries
4. Configure TFT_eSPI User_Setup.h
5. Compile and upload
""",
    "docs/USER_GUIDE.md": """# User Guide
- Connect input signal to ADC pin (via divider)
- Press Menu to toggle modes
- Connect to E-OSCI-V1 WiFi to view on web
""",
    "docs/CALIBRATION.md": """# Calibration
Ensure resistors are exactly 100k and 10k for 11.0 attenuation.
Adjust `VOLTAGE_SCALE` in config.h if necessary.
""",
    "docs/TROUBLESHOOTING.md": """# Troubleshooting
- White screen: Check TFT SPI pins
- No waveform: Check ADC pin connection and trigger level
- WiFi not showing: Wait 10 seconds after boot
""",
    "docs/PROJECT_DESCRIPTION.md": """# Project Description
University Final Year Project: E-OSCI V1

1. Abstract: A portable oscilloscope...
2. Introduction: Oscilloscopes are vital...
3. Hardware Design: ESP32 + ILI9341...
(Full report content to be expanded)
"""
}

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("All files generated successfully!")
