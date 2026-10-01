// ================================================================
// E-OSCI V1 - ADC Sampler Module
// Author: P.P.N.Pathirana
// ================================================================

#include "adc_sampler.h"
#include "config.h"
#include <Arduino.h>
#include <driver/i2s.h>

volatile uint16_t adcBuffer[BUFFER_SIZE];

void adc_sampler_init() {
    Serial.println("[ADC] Initializing I2S ADC...");
    
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX | I2S_MODE_ADC_BUILT_IN),
        .sample_rate = ADC_SAMPLE_RATE,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_RIGHT,
        .communication_format = I2S_COMM_FORMAT_I2S_MSB,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 4,
        .dma_buf_len = 512,
        .use_apll = false,
        .tx_desc_auto_clear = false,
        .fixed_mclk = 0
    };
    
    i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
    i2s_set_adc_mode(ADC_UNIT_1, ADC1_CHANNEL_6); // GPIO 34
    i2s_adc_enable(I2S_NUM_0);
}

bool adc_captureOnce() {
    size_t bytesRead;
    i2s_read(I2S_NUM_0, (void*)adcBuffer, BUFFER_SIZE * sizeof(uint16_t), &bytesRead, portMAX_DELAY);
    
    for (int i = 0; i < BUFFER_SIZE; i++) {
        adcBuffer[i] &= 0x0FFF;
    }
    
    return bytesRead == (BUFFER_SIZE * sizeof(uint16_t));
}
