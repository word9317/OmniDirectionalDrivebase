#include <gyro.h>
#include <Wire.h>
#include <math.h>

static const uint8_t MPU_ADDR = 0x68;

static float gyroBias[3] = {0, 0, 0};
static float angle[3]    = {0, 0, 0};
static unsigned long lastMicros = 0;
static bool firstRun = true;

static bool readSensor(float a[3], float g[3]) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);  // first data register
  if (Wire.endTransmission(false) != 0) return false;
  if (Wire.requestFrom(MPU_ADDR, (uint8_t)14) != 14) return false;

  int16_t ax = (Wire.read() << 8) | Wire.read();
  int16_t ay = (Wire.read() << 8) | Wire.read();
  int16_t az = (Wire.read() << 8) | Wire.read();
  Wire.read(); Wire.read();  // skip temperature
  int16_t gx = (Wire.read() << 8) | Wire.read();
  int16_t gy = (Wire.read() << 8) | Wire.read();
  int16_t gz = (Wire.read() << 8) | Wire.read();

  a[0] = ax / 16384.0f;  // +/-2 g range
  a[1] = ay / 16384.0f;
  a[2] = az / 16384.0f;
  g[0] = gx / 131.0f;    // +/-250 deg/s range
  g[1] = gy / 131.0f;
  g[2] = gz / 131.0f;
  return true;
}

bool mpuSetup() {
  Wire.begin();  // connect to sda scl pins
  Wire.setClock(400000);

  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);
  Wire.write(0x00);
  if (Wire.endTransmission() != 0) return false;

  delay(100);
  firstRun = true;
  return true;
}

void mpuCalibrate() {
  const int samples = 500;
  float sum[3] = {0, 0, 0};
  int good = 0;

  for (int i = 0; i < samples; i++) {
    float a[3], g[3];
    if (readSensor(a, g)) {
      sum[0] += g[0];
      sum[1] += g[1];
      sum[2] += g[2];
      good++;
    }
    delay(3);
  }

  if (good > 0) {
    for (int i = 0; i < 3; i++) gyroBias[i] = sum[i] / good;
  }

  angle[0] = angle[1] = angle[2] = 0;
  firstRun = true;
}

float mpuGetAxis(Axis axis) {
  float a[3], g[3];
  if (!readSensor(a, g)) return angle[axis];

  unsigned long now = micros();
  float dt = (now - lastMicros) * 1e-6f;
  lastMicros = now;

  float accRoll  = atan2f(a[1], a[2]) * 57.2958f;
  float accPitch = atan2f(-a[0], sqrtf(a[1] * a[1] + a[2] * a[2])) * 57.2958f;

  if (firstRun) {
    angle[0] = accRoll;
    angle[1] = accPitch;
    angle[2] = 0;
    firstRun = false;
    return angle[axis];
  }
  angle[0] = 0.98f * (angle[0] + (g[0] - gyroBias[0]) * dt) + 0.02f * accRoll;
  angle[1] = 0.98f * (angle[1] + (g[1] - gyroBias[1]) * dt) + 0.02f * accPitch;
  angle[2] += (g[2] - gyroBias[2]) * dt;  // yaw: gyro only

  return angle[axis];
}