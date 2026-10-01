// ================================================================
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
