// ================================================================
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
