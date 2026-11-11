#include <Arduino.h>
#include <gyro.h>
#include <rsl.h>
#include <constants.h>
#include <motors.h>
#include <math.h>

RobotMotors motors;

void setup()
{
  initLEDController();
  setActive(false);
  mpuSetup();
  mpuCalibrate();
  Serial.begin(9600);
  setActive(true);
}

// drive with a specific rotation(ty random article about frc swerve)
void driveHolonomic(float vx, float vy, float omega)
{
  if (isFieldOriented)
  {
    float yaw = mpuGetAxis(AXIS_Z) * (M_PI / 180.0f);
    float temp_vx = vx * cos(yaw) + vy * sin(yaw);
    float temp_vy = -vx * sin(yaw) + vy * cos(yaw);
    vx = temp_vx;
    vy = temp_vy;
  }

  float m1 = vx - vy - omega; // FL motor(hypothetically)
  float m2 = vx + vy + omega; // FR motor(hypothetically)
  float m3 = vx + vy - omega; // RL motor(hypothetically)
  float m4 = vx - vy + omega; // RR motor(hypothetically)

  // prevent any motor from being over 255 and scale all other motors
  float maxVal = max(max(abs(m1), abs(m2)), max(abs(m3), abs(m4)));
  if (maxVal > 255.0f)
  {
    m1 = (m1 / maxVal) * 255.0f;
    m2 = (m2 / maxVal) * 255.0f;
    m3 = (m3 / maxVal) * 255.0f;
    m4 = (m4 / maxVal) * 255.0f;
  }
  // make motors actually spin
  motors.setMotor(1, (int)m1);
  motors.setMotor(2, (int)m2);
  motors.setMotor(3, (int)m3);
  motors.setMotor(4, (int)m4);
}

// function to dissasemble serial input and process for robot commands
void processCommand(String input)
{
  input.trim();

  // ultra niche commands like enable/disable. all this does is disable motors in case something gets messed up during operation.
  if (input.equalsIgnoreCase("disable"))
  {
    motors.estop();
    setActive(false);
    return;
  }
  if (input.equalsIgnoreCase("enable"))
  {
    motors.enable();
    setActive(true);
    return;
  }
  // calibrate the gyro, disable motors to make sure that robot doesnt try to calibrate while moving
  if (input.equalsIgnoreCase("calibrate"))
  {
    motors.estop();
    mpuCalibrate();
    motors.enable();
    return;
  }

  // actually process movement commands. they will be sent in the following format:
  // x:y:z --- x & y => movement, z => rotation
  int firstColon = input.indexOf(':');
  int secondColon = input.lastIndexOf(':');

  if (firstColon != -1 && secondColon != -1 && firstColon != secondColon)
  {
    float vx = input.substring(0, firstColon).toFloat();
    float vy = input.substring(firstColon + 1, secondColon).toFloat();
    float omega = input.substring(secondColon + 1).toFloat();

    driveHolonomic(vx, vy, omega);

    Serial.print("ACK -> VX:");
    Serial.print(vx);
    Serial.print(" VY:");
    Serial.print(vy);
    Serial.print(" Omega:");
    Serial.println(omega);
  }
  else
  {
    Serial.println("ERR: Unknown command format.");
  }
}

void loop()
{
  handleLEDTimers();

  // process data and flash corresponding LED(onyl when driving)
  if (Serial.available() > 0 && runningRobot)
  {
    String incoming = Serial.readStringUntil('\n');
    receiveLED();
    processCommand(incoming);
  }

  String response = "";
  if (testingGyro)
  {
    response += mpuGetAxis(AXIS_Z);
  }

  if (response != "")
  {
    sendLED();
    Serial.println(response);
  }
}