// ================================================================
// E-OSCI V1 - SD Logger Header
// Author: P.P.N.Pathirana
// ================================================================

#ifndef SD_LOGGER_H
#define SD_LOGGER_H

#include <stdint.h>

void sd_init();
void sd_logWaveform(volatile uint16_t* buffer, int length);

#endif // SD_LOGGER_H
