// ================================================================
// E-OSCI V1 - Signal Generator Header
// Author: P.P.N.Pathirana
// ================================================================

#ifndef SIGNAL_GEN_H
#define SIGNAL_GEN_H

#include <stdint.h>

void siggen_init();
void siggen_setFreq(float freqHz);
void siggen_stop();

#endif // SIGNAL_GEN_H
