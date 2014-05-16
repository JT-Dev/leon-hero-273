#!/usr/bin/env python3

import pygame

import g
import time
import utils
import constants
import sys

class SplashScreen(object):
	def __init__(self, loader):
		self.splash = loader.load("sprites/splash.png", "image").convert_alpha()
		self.splash = pygame.transform.scale(self.splash, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

		self.cur_time = time.time()
		self.end_time = self.cur_time + constants.SPLASH_LENGTH

	def update(self, _):
		self.cur_time = time.time()

		if self.cur_time >= self.end_time:
			g.screen = g.screen_map["title"]

	def draw(self, surface):
		#x = (constants.SCREEN_WIDTH - self.splash.get_width()) // 2
		#y = (constants.SCREEN_HEIGHT - self.splash.get_height()) // 2
		x = y = 0

		surface.blit(self.splash, (x, y))

	def peek(self):
		return self.cur_time >= self.end_time
