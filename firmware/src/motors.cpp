#include "Motors.h"
#include "constants.h"

void RobotMotors::init() {
    pinMode(ENA_1, OUTPUT);
    pinMode(IN1_1, OUTPUT);
    pinMode(IN2_1, OUTPUT);
    pinMode(IN3_1, OUTPUT);
    pinMode(IN4_1, OUTPUT);
    pinMode(ENB_1, OUTPUT);

    pinMode(ENA_2, OUTPUT);
    pinMode(IN1_2, OUTPUT);
    pinMode(IN2_2, OUTPUT);
    pinMode(IN3_2, OUTPUT);
    pinMode(IN4_2, OUTPUT);
    pinMode(ENB_2, OUTPUT);
}

void RobotMotors::estop() {
    motorsEnabled = false;

    analogWrite(ENA_1, 0);
    analogWrite(ENB_1, 0);
    analogWrite(ENA_2, 0);
    analogWrite(ENB_2, 0);

    // Pull all direction pins LOW
    digitalWrite(IN1_1, LOW); digitalWrite(IN2_1, LOW);
    digitalWrite(IN3_1, LOW); digitalWrite(IN4_1, LOW);
    digitalWrite(IN1_2, LOW); digitalWrite(IN2_2, LOW);
    digitalWrite(IN3_2, LOW); digitalWrite(IN4_2, LOW);
    
    Serial.println("EMERGENCY STOP ACTIVATED!");
}

void RobotMotors::enable() {
    motorsEnabled = true;
    Serial.println("Motors re-enabled.");
}

void RobotMotors::setMotor(int motorNum, int speed) {
    if (!motorsEnabled) {
        speed = 0;
    } // <-- Fixed: Added missing closing brace here

    speed = constrain(speed, -255, 255);
    bool reverse = speed < 0;
    int absSpeed = abs(speed);

    switch (motorNum) {
        case 1:
            analogWrite(ENA_1, absSpeed);
            digitalWrite(IN1_1, reverse ? LOW : HIGH);
            digitalWrite(IN2_1, reverse ? HIGH : LOW);
            break;
        case 2:
            analogWrite(ENB_1, absSpeed);
            digitalWrite(IN3_1, reverse ? LOW : HIGH);
            digitalWrite(IN4_1, reverse ? HIGH : LOW);
            break;
        case 3:
            analogWrite(ENA_2, absSpeed);
            digitalWrite(IN1_2, reverse ? LOW : HIGH);
            digitalWrite(IN2_2, reverse ? HIGH : LOW);
            break;
        case 4:
            analogWrite(ENB_2, absSpeed);
            digitalWrite(IN3_2, reverse ? LOW : HIGH);
            digitalWrite(IN4_2, reverse ? HIGH : LOW);
            break;
    }
}