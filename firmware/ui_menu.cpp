// ================================================================
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
