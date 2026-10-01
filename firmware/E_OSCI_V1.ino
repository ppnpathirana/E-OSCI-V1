// ================================================================
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
