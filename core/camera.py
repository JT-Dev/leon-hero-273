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

import utils
import constants

class Camera(object):
	"A simple camera object."

	def __init__(self, window, level):
		self.level = level
		self.rect = pygame.Rect((0, 0), (window.width, window.height))
		self.buffer = pygame.Rect((0, 0), (constants.BUFFER_WIDTH, constants.BUFFER_HEIGHT))

	def _center(self, target):
		# Find camera position [painful to say the least]
		x = (target.x + (target.width // 2)) - (self.rect.width // 2)
		y = (target.y + (target.height // 2)) - (self.rect.height // 2)

		# Ensure the camera doesn't go off-screen
		x = max(0, x)
		y = max(0, y)
		x = min(self.level.width - self.rect.width, x)
		y = min(self.level.height - self.rect.height, y)

		self.rect.x = x
		self.rect.y = y

		self.buffer.centerx = self.rect.centerx
		self.buffer.centery = self.rect.centery

	def apply(self, target):
		"Applies the camera offset to the target."
		dx = -self.rect.x
		dy = -self.rect.y

		return pygame.Rect(target.x + dx, target.y + dy, target.width, target.height)

	def update(self, target):
		"Update camera position to center to target."
		self._center(target)
