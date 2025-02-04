#include "Servo.h"
Servo servoMotorObj;

int led_red = 4;
int led_green = 5;
int buzzer = 6;

int const servoMotorPin = 3;

void setup() {
  Serial.begin(9600);

  servoMotorObj.attach(servoMotorPin);
  pinMode(led_red, OUTPUT);
  pinMode(led_green, OUTPUT);
  pinMode(buzzer, OUTPUT);

  servoMotorObj.write(0);
  digitalWrite(led_red, 1);
}

void loop() {
  if (Serial.available()) {
    char status = Serial.read();
    if (status == '1') {
      servoMotorObj.write(90);
      tone(buzzer, 1000, 1000);
      digitalWrite(led_green, 1);
      digitalWrite(led_red, 0);
    }
    else {
      servoMotorObj.write(0);
      digitalWrite(led_green, 0);
      digitalWrite(led_red, 1);
    }

    delay(1000);
  }
}