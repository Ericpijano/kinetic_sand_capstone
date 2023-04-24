#include <Arduino.h>
// Test code for blinking built-in LED on an Arduino Nano

// Pin connected to the built-in LED
const int ledPin = 13;

// Blink interval (in milliseconds)
const int blinkInterval = 1000; // 1000 ms = 1 second

void setup() {
  // Set the LED pin as output
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Turn the LED on
  digitalWrite(ledPin, HIGH);
  // Wait for the blink interval
  delay(blinkInterval);

  // Turn the LED off
  digitalWrite(ledPin, LOW);
  // Wait for the blink interval
  delay(blinkInterval);
}
