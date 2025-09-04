#include <Arduino.h>
#include <WiFiMulti.h>
#include <WiFi.h>
#include <HTTPClient.h>

#define PIR_PIN 12 //replace this with the GPIO pin your PIR sensor is connected to
#define LED_PIN 2

// Replace with your WIFI credentials
#define WIFI_SSID "ssid"
#define WIFI_PASSWORD "password"

// Replace with your PC's LAN IP where the flask server is running
#define API_URL "http://x.x.x.x:yyyy/motion"

WiFiMulti wifiMulti;
int motionState = 0;
bool wasConnected = false;
bool motionSent = false;  // Ensure request sent once per motion event

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  wifiMulti.addAP(WIFI_SSID, WIFI_PASSWORD);

  Serial.println("Connecting to WiFi...");
  while (wifiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("Connected! IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Ensure Wi-Fi is connected
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected, reconnecting...");
    wifiMulti.run();
    delay(500);
    return;
  }

  // Read PIR sensor
  motionState = digitalRead(PIR_PIN);
  digitalWrite(LED_PIN, motionState);

  // Debug: check connectivity to Flask server
  WiFiClient testClient;
  if (!testClient.connect("192.168.1.150", 5000)) {
    Serial.println("Server not found");
    delay(1000);
    return;
  }

  // Motion detected → send request once
  if (motionState == HIGH && !motionSent) {
    Serial.println("Motion detected! Sending request to API...");

    HTTPClient http;
    http.begin(API_URL);
    int httpResponseCode = http.GET();

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Response: ");
      Serial.println(response);
      motionSent = true;  // Mark as sent
    } else {
      Serial.print("Error on sending request: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  }

  // Reset flag when motion stops
  if (motionState == LOW && motionSent) {
    motionSent = false;
    Serial.println("No motion");
  }

  delay(50);
}