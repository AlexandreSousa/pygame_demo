# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from colors import *

# All classes of the game are here


class Characters(Sprite):

    '''
    Base class for all characters of the game
    '''

    def __init__(self, start_px, start_py, image_name, *groups):
        Sprite.__init__(self, *groups)
        self.start_px = start_px
        self.start_py = start_py
        self.px = 0
        self.py = 0
        self._move_states = {"LEFT": 0, "RIGHT": 0, "UP": 0, "DOWN": 0}
        self.rect = Rect(self.start_px, self.start_py, 0, 0)
        self._base_image_path = "sprites/"
        self.image_name = image_name
        self.image = pygame.image.load(
            self._base_image_path + image_name + "RIGHT1.png")
        self.convert_image()
        pygame.draw.rect(self.image, BLACK, self)

    def move(self, side):
        '''
        move the character
        '''
        side_state = str(self._move_states[side] + 1)
        self.image = pygame.image.load(
            self._base_image_path + self.image_name + side + side_state + ".png")

        self._change_state(side)

    def _change_state(self, side):
        '''
        change the position of the character in the screen
        '''
        self.convert_image()
        if side == 'LEFT':
            x, y = -10, 0
        if side == 'RIGHT':
            x, y = 10, 0
        if side == 'UP':
            x, y = 0, -10
        if side == 'DOWN':
            x, y = 0, 10
        self.rect.move_ip(x, y)
        self.px += x
        self.py += y

        self._move_states[side] += 1
        if self._move_states[side] > 2:
            self._move_states[side] = 0

    def convert_image(self):
        '''
        Convert the character image and set colorkey to magenta(i.e pynk)
        '''
        self.image.set_alpha(None, RLEACCEL)
        self.image.convert()
        self.image.set_colorkey(MAGENTA, RLEACCEL)


class Hero(Characters):

    '''
    Class for the heroes of the game
    '''

    def __init__(self, start_px, start_py, image_name, *groups):
        Characters.__init__(self, start_px, start_py, image_name, *groups)


class Npc(Characters):

    '''
    Class for all the npcs of the game
    npcs = all characters that you can interact
    '''

    def __init__(self, start_px, start_py, image_name, *groups):
        Characters.__init__(self, start_px, start_py, *groups)
