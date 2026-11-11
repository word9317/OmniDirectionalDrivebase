#pragma once

#include <Arduino.h>

enum Axis { AXIS_X = 0, AXIS_Y = 1, AXIS_Z = 2 };

bool mpuSetup();

void mpuCalibrate();


float mpuGetAxis(Axis axis);