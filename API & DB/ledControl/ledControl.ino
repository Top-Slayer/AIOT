const int RED_LED_PIN = 13;    // RED LED pin
const int GREEN_LED_PIN = 12; // GREEN LED pin
const int BLUE_LED_PIN = 11;  // BLUELED pin

void setup() {
    pinMode(RED_LED_PIN, OUTPUT);    // ຕັ້ງ pin ເປັນຮູບແບບການອອກ
    pinMode(GREEN_LED_PIN, OUTPUT); // 노란색 LED ຕັ້ງ pin ເປັນຮູບແບບການອອກ
    pinMode(BLUE_LED_PIN, OUTPUT);  // 초록색 LED ຕັ້ງ pin ເປັນຮູບແບບການອອກ
    Serial.begin(9600);              // Start Serial communition
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n'); // 시리얼로부터 명령어를 읽음

        if (command == "RED_ON") {
            digitalWrite(RED_LED_PIN, HIGH); // 빨간색 LED 켜기
        } else if (command == "RED_OFF") {
            digitalWrite(RED_LED_PIN, LOW);  // 빨간색 LED 끄기
        } else if (command == "GREEN_ON") {
            digitalWrite(GREEN_LED_PIN, HIGH); // 노란색 LED 켜기
        } else if (command == "GREEN_OFF") {
            digitalWrite(GREEN_LED_PIN, LOW);  // 노란색 LED 끄기
        } else if (command == "BLUE_ON") {
            digitalWrite(BLUE_LED_PIN, HIGH); // 초록색 LED 켜기
        } else if (command == "BLUE_OFF") {
            digitalWrite(BLUE_LED_PIN, LOW);  // 초록색 LED 끄기
        }
    }
}