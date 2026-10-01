// ================================================================
// E-OSCI V1 - Web Server Module
// Author: P.P.N.Pathirana
// ================================================================

#include "web_server.h"
#include <WiFi.h>
#include <WebServer.h>

static WebServer server(80);
static volatile uint16_t* lastBuffer = NULL;
static int lastBufferLen = 0;

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <title>E-OSCI V1</title>
  <style>
    body { background-color: #111; color: #fff; font-family: monospace; text-align: center; }
    canvas { background-color: #000; border: 1px solid #444; }
  </style>
</head>
<body>
  <h2>E-OSCI V1 - Web Viewer</h2>
  <canvas id="oscCanvas" width="800" height="400"></canvas>
  <div id="readouts">Connecting...</div>
  <script>
    const canvas = document.getElementById('oscCanvas');
    const ctx = canvas.getContext('2d');
    
    function drawGrid() {
        ctx.strokeStyle = '#222';
        ctx.beginPath();
        for(let x=0; x<=800; x+=100) { ctx.moveTo(x, 0); ctx.lineTo(x, 400); }
        for(let y=0; y<=400; y+=50) { ctx.moveTo(0, y); ctx.lineTo(800, y); }
        ctx.stroke();
    }
    
    async function fetchData() {
        try {
            const res = await fetch('/data');
            const arrayBuffer = await res.arrayBuffer();
            const data = new Uint16Array(arrayBuffer);
            
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, 800, 400);
            drawGrid();
            
            ctx.strokeStyle = '#0f0';
            ctx.beginPath();
            for(let i=0; i<data.length && i<800; i++) {
                let y = 400 - (data[i] * 400 / 4095);
                if(i===0) ctx.moveTo(i, y);
                else ctx.lineTo(i, y);
            }
            ctx.stroke();
            
            document.getElementById('readouts').innerText = "Live Waveform Updated";
        } catch(e) {
            console.log(e);
        }
        setTimeout(fetchData, 100);
    }
    fetchData();
  </script>
</body>
</html>
)rawliteral";

void handleRoot() {
    server.send(200, "text/html", index_html);
}

void handleData() {
    if (lastBuffer != NULL && lastBufferLen > 0) {
        server.send_P(200, "application/octet-stream", (const char*)lastBuffer, lastBufferLen * 2);
    } else {
        server.send(404, "text/plain", "No data");
    }
}

void web_init() {
    WiFi.softAP("E-OSCI-V1", "oscope1234");
    server.on("/", handleRoot);
    server.on("/data", handleData);
    server.begin();
    Serial.println("[WiFi] AP Started: E-OSCI-V1");
}

void web_loop() {
    server.handleClient();
}

void web_sendWaveform(volatile uint16_t* buffer, int length) {
    lastBuffer = buffer;
    lastBufferLen = length;
}
