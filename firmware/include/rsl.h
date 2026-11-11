#pragma once
#include <Arduino.h>
#include <Modulino.h>

void initLEDController();

void handleLEDTimers();

void setActive(bool active);

void receiveLED();