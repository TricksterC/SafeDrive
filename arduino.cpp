const int ledPin = 13;  // LED connected to pin 13

void setup() {
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600);  // Start Serial Communication at 9600 baud
}

void loop() {
    if (Serial.available() > 0) {  // Check if data is available
        char command = Serial.read();  // Read the received character
        if (command == '1') {
            digitalWrite(ledPin, HIGH);  // Turn LED ON
        } else if (command == '0') {
            digitalWrite(ledPin, LOW);   // Turn LED OFF
        }
    }
}
