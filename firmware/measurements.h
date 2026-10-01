// ================================================================
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
