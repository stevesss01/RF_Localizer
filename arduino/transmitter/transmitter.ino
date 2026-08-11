/*
 * RF Localizer - Transmitter Node
 * Arduino Uno
 * nRF24L01 / RF communication prototype
 */

float angle = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {

  // Smooth RF signal-strength variation
  int signal =
      70 +
      15 * sin(angle) +
      8 * sin(angle * 0.4);

  // Numeric output consumed by the Python dashboard
  Serial.println(signal);

  angle += 0.25;

  delay(200);
}