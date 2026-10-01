// ================================================================
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
