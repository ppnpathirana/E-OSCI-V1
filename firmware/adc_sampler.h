// ================================================================
// E-OSCI V1 - ADC Sampler Header
// Author: P.P.N.Pathirana
// ================================================================

#ifndef ADC_SAMPLER_H
#define ADC_SAMPLER_H

#include <stdint.h>
#include <stdbool.h>

extern volatile uint16_t adcBuffer[];

void adc_sampler_init();
bool adc_captureOnce();

#endif // ADC_SAMPLER_H
