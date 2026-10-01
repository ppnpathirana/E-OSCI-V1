// ================================================================
// E-OSCI V1 - Web Server Header
// Author: P.P.N.Pathirana
// ================================================================

#ifndef WEB_SERVER_H
#define WEB_SERVER_H

#include <stdint.h>

void web_init();
void web_loop();
void web_sendWaveform(volatile uint16_t* buffer, int length);

#endif // WEB_SERVER_H
