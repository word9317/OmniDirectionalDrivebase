#pragma once
#include <Arduino.h>

class RobotMotors {
private:
    bool motorsEnabled = true;
public:
    void init();
    void setMotor(int motorNum, int speed); // speed range: -255 to 255
    void estop();
    void enable();
};