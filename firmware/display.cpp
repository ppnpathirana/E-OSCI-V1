// ================================================================
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
