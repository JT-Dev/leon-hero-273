#!/usr/bin/env python3

# Leon: Hero 273 -- A game made for a 48-hour game jam.
# Copyright (C) 2014 JT-Dev

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# 1. The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
