#include <Arduino.h>
#include <Modulino.h>

ModulinoPixels pixels;

const unsigned long ACTIVE_BLINK_INTERVAL = 500;
const unsigned long RECEIVE_BLINK_DURATION = 50; // when instruction is recieved instead of holding robot over to know when its recieving instructions from the rock

bool isSystemActive = false;
bool activeLedState = false;
unsigned long lastActiveMillis = 0;

bool isReceiving = false;
unsigned long receiveStartMillis = 0;

// update pixels based on the state
void updatePixels() {
  // if active, orange is flashing, and if not active, dont flash
  for (int i = 0; i < 7; i++) {
    if (isSystemActive && activeLedState) {
      pixels.set(i, 255, 80, 0, 25);
    } else {
      pixels.clear(i);
    }
  }

  // comms signal light
  if (isReceiving) {
    pixels.set(7, BLUE, 25);
  } else {
    pixels.clear(7);
  }

  pixels.show();
}

void handleLEDTimers() {
  unsigned long currentMillis = millis();
  bool needsUpdate = false;

  // check last orange interval(if active though)
  if (isSystemActive) {
    if (currentMillis - lastActiveMillis >= ACTIVE_BLINK_INTERVAL) {
      lastActiveMillis = currentMillis;
      activeLedState = !activeLedState;
      needsUpdate = true;
    }
  }

  //  turn off blue LED if done recieving
  if (isReceiving && (currentMillis - receiveStartMillis >= RECEIVE_BLINK_DURATION)) {
    isReceiving = false;
    needsUpdate = true;
  }

  if (needsUpdate) {
    updatePixels();
  }
}

// set is active(like enabled/disabled)
void setActive(bool active) {
  if (isSystemActive != active) {
    isSystemActive = active;
    if (isSystemActive) {
      activeLedState = true;
      lastActiveMillis = millis();
    } else {
      activeLedState = false;
    }
    updatePixels();
  }
}

void receiveLED() {
  isReceiving = true;
  receiveStartMillis = millis();
  updatePixels();
}
