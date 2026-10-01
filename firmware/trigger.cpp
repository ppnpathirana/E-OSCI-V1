// ================================================================
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
