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

import pygame.locals

class InputManager(object):
	OFF = 0
	ON = 1
	OLD_ON = 2

	def __init__(self):
		self.keys = {}
		self.click_pos = None
		self.click_state = False

	def handle(self, event):
		if event.type == pygame.locals.KEYDOWN:
			self.keys[event.key] = self.ON
		elif event.type == pygame.locals.KEYUP:
			self.keys[event.key] = self.OFF
		elif event.type == pygame.locals.MOUSEBUTTONDOWN:
			self.click_pos = event.pos
			self.click_state = True
		elif event.type == pygame.locals.MOUSEBUTTONUP:
			self.click_pos = event.pos
			self.click_state = False

	def check_key(self, key):
		return self.keys.get(key, self.OFF) != self.OFF

	def check_key_single(self, key):
		state = self.keys.get(key, self.OFF)

		if state == self.ON:
			self.keys[key] = self.OLD_ON

		return state == self.ON

	def reset(self):
		self.keys = {}
		self.click_pos = None
		self.click_state = False
