#include <Arduino.h>
#include <Modulino.h>
#include <constants.h>

ModulinoPixels pixels;

const unsigned long ACTIVE_BLINK_INTERVAL = rslActiveMilis;
const unsigned long S_R_BLINK_DURATIO = srMilis; // when instruction is recieved instead of holding robot over to know when its recieving instructions from the rock

bool isSystemActive = false;
bool activeLedState = false;
unsigned long lastActiveMillis = 0;

bool isReceiving = false;
unsigned long receiveStartMillis = 0;

bool isSending = false;
unsigned long sendingStartMillis = 0;

// update pixels based on the state
void updatePixels() {
  // if active, orange is flashing, and if not active, dont flash
  for (int i = 0; i < 6; i++) {
    if (isSystemActive && activeLedState) {
      pixels.set(i, 255, 80, 0, 25);
    } else {
      pixels.clear(i);
    }
  }
  // sending signal light
  if (isSending) {
    pixels.set(6, BLUE, 25);
  } else {
    pixels.clear(6);
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
  if (isReceiving && (currentMillis - receiveStartMillis >= S_R_BLINK_DURATIO)) {
    isReceiving = false;
    needsUpdate = true;
  }

  if (isSending && (currentMillis - sendingStartMillis >= S_R_BLINK_DURATIO)) {
    isSending = false;
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

void sendLED(){
  isSending = true;
  sendingStartMillis = millis();
  updatePixels();
}


void initLEDController() {
  Modulino.begin();
  pixels.begin();
}