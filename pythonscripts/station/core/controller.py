import os

# claudes fix for some conflicts with pyqt
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS", "1")

import pygame

from config import (
    AXIS_LEFT_X, AXIS_LEFT_Y, AXIS_RIGHT_X, STICK_DEADZONE, TURN_COEFFICIENT_INVERSE,
)


def _deadzone(v):
    return 0.0 if abs(v) < STICK_DEADZONE else v


class ControllerInput:
    def __init__(self):
        pygame.display.init()      # init the stuff
        pygame.joystick.init()
        self._joy = None

    @property
    def active(self):
        return self._joy is not None

    def list_controllers(self):
        # get list of controllers, hopefully the function name is self explanatory
        pygame.joystick.quit()
        pygame.joystick.init()
        return [
            (i, pygame.joystick.Joystick(i).get_name())
            for i in range(pygame.joystick.get_count())
        ]

    def select(self, index):
        # select a controller to use
        self._joy = None
        if index is None:
            return
        try:
            self._joy = pygame.joystick.Joystick(index)
            self._joy.init()
        except pygame.error:
            self._joy = None

    def read(self):
        # return inputs
        if self._joy is None:
            return 0.0, 0.0, 0.0
        try:
            pygame.event.pump()
            x = _deadzone(self._joy.get_axis(AXIS_LEFT_X))
            y = -_deadzone(self._joy.get_axis(AXIS_LEFT_Y))
            z = _deadzone(self._joy.get_axis(AXIS_RIGHT_X)) / TURN_COEFFICIENT_INVERSE
            return x, y, z
        except pygame.error:       # controller unplugged or not selected
            self._joy = None
            return 0.0, 0.0, 0.0

    def shutdown(self):
        self._joy = None
        pygame.joystick.quit()
        pygame.display.quit()