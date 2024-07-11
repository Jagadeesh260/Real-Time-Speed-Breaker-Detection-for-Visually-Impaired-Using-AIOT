#include <WiFi.h>
#include <WebServer.h>
#include <WebSocketsServer_Generic.h>

const char* ssid = "JAGADEESH";
const char* password = "6380251481";

WebServer server(80);
WebSocketsServer webSocketServer(81);

// Variables to store the data
float speed = 7;
float latitude = 80.980021;
float longitude = 23.003457;
float change = 0.5;

String message = ""; // Variable to store the message

void handleRoot() {
  String response = "Speed: " + String(speed) + "<br>";
  response += "Latitude: " + String(latitude) + "<br>";
  response += "Longitude: " + String(longitude) + "<br>";
  response += "Change: " + String(change) + "<br>";
  response += "Prediction: " + message; // Display the message on the webpage
  
  server.send(200, "text/html", response);
}

void handleSpeedBreaker() {
  // Update the message with the received data
  message = server.arg("message");
  Serial.println("Received message: " + message);
  
  server.send(200, "text/plain", "Message received");
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
  // Handle WebSocket events here if needed
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.print("Connected to WiFi. IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/speed-breaker", HTTP_POST, handleSpeedBreaker); // New route to handle speed breaker indication

  server.begin();
  Serial.println("HTTP server started");

  webSocketServer.begin();
  webSocketServer.onEvent(webSocketEvent);
  Serial.println("WebSocket server started");
}

void loop() {
  server.handleClient();
  webSocketServer.loop();
}