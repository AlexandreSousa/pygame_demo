# -*- coding: utf-8 -*-

import pygame
import time
import config
from fsm import Fsm
from pygame.locals import *
from pygame.sprite import Sprite
from colors import *


class Characters(Sprite):
    """"
    Base class for all characters of the game
    """

    def __init__(self, start_px, start_py, *groups):
        Sprite.__init__(self, *groups)
        self.px = start_px
        self.py = start_py
        self.yVel = 0
        self.states = {
              "stand_still": self.stand_still,
              "move": self.move,
              "jump": self.jump,
              "get_down": self.get_down,
              "attack": self.attack,
        }

        self.fsm = Fsm(active_state="stand_still", states=self.states)
        self.images = {}
        self._base_image_path = "src/sprites/"
        self._load_state_images()
        self.rect = Rect(self.px, self.py, 0, 0)
        self.image = self.images[self.fsm.get_state()][0]
        self.convert_image()
        pygame.draw.rect(self.image, BLACK, self)

    def _load_state_images(self):
        base_image_path = self._base_image_path
        images = config.load_game_config_file("src/characters.yaml")
        hero_images = images["hero_images"]
        for state in self.states:
            self.images[state] = [Characters._load_scale_2x(base_image_path + image) for image in hero_images[state]]

    @classmethod
    def _load_scale_2x(cls, image):
        return pygame.transform.scale2x(pygame.image.load(image))

    def _load_image_in_actual_side(self, index):
        state = self.fsm.get_state()
        if self.fsm.side == "left":
            self.image = pygame.transform.flip(self.images[state][index], True, False)
        else:
            self.image = self.images[state][index]

    def stand_still(self):
        self._load_image_in_actual_side(0)
        self.convert_image()


    def jump(self):
        self.yVel = -15
        self.jumping = True

    def get_down(self):
        pass

    def is_jumping(self, gravity):
        return
        # if self.jumping:
        #     print self.py
        #
        #     self.yVel += gravity
        #     self.py += self.yVel
        #     self.rect.move_ip(self.px, self.py)
        #     if self.yVel < 0:
        #         self.py -= self.yVel
        #         if self.py > 50:
        #             self.py = 0
        #             self.jumping = False

    def attack(self):
        attack_count = self.fsm.attack_count
        self._load_image_in_actual_side(attack_count)
        if attack_count == 4:
            self.fsm.attack_count = 0
            self.fsm.set_state("stand_still")
        else:
            self.fsm.attack_count +=1
        self.convert_image()

    def move(self):
        side_moves = self.fsm.moves_count
        self._load_image_in_actual_side(side_moves)
        if self.fsm.side  == 'left':
            self.rect.move_ip(-10, 0)
        else:
            self.rect.move_ip(10, 0)
        self.convert_image()
        time.sleep(0.075)

    def convert_image(self):
        '''
        Convert the character image and set colorkey to magenta(i.e pynk)
        '''
        self.image.set_alpha(None, RLEACCEL)
        self.image.convert()
        self.image.set_colorkey(MAGENTA, RLEACCEL)

class Hero(Characters):

    def __init__(self, *args, **kwargs):
        super(Hero, self).__init__(*args, **kwargs)
