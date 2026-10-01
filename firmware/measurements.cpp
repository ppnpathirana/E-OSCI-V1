// ================================================================
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
