// ================================================================
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
