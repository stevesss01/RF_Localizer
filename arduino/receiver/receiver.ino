/*
 * RF Localizer - Receiver Node
 * Arduino Uno
 * Receiver-side monitoring demonstration
 */

float angle = 0;

void setup() {
  Serial.begin(9600);

  Serial.println("RF RECEIVER NODE ACTIVE");
  Serial.println("----------------------");
}

void loop() {

  // Simulated received signal-strength variation
  int rssi =
      65 +
      10 * sin(angle);

  Serial.print("[RX] RSSI : ");
  Serial.print(rssi);
  Serial.println(" dBm");

  angle += 0.15;

  delay(500);
}