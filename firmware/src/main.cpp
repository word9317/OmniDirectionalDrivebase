#include <Arduino.h>
#include <gyro.h>
#include <rsl.h>
#include <constants.h>

void setup() {
  initLEDController();
  setActive(false);
  mpuSetup();
  mpuCalibrate();
  Serial.begin(9600);
  setActive(true);
}

void loop() {
  handleLEDTimers();
  String response = "";
  if(testingGyro){
    response += mpuGetAxis(AXIS_Z);
  }

  if(response != ""){
    sendLED();
    Serial.println(response);
  }
}