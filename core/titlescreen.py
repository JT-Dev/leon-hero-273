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
import utils
import constants
import sys

class TitleScreen(object):
	class Button(object):
		#0 Button Not Down
		#1 Button Down

		def __init__(self, pos, image_up, image_down, main, screen):
			self.image_up = image_up
			self.image_down = image_down
			self.rect = pygame.Rect(pos, self.image_up.get_rect().size)

			self.main = main
			self.screen = screen
			self.state = 0

		def clicked(self):
			if not self.screen:
				pygame.quit()
				sys.exit()

			self.main.running = False
			g.screen = self.screen

		def draw(self, surface):
			if self.state:
				surface.blit(self.image_down, self.rect)
			else:
				surface.blit(self.image_up, self.rect)

	def __init__(self, loader):
		self.background = loader.load("sprites/logo.png","image").convert_alpha()
		self.background = pygame.transform.scale(self.background, (constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2))

		self.music = loader.load("sounds/titlescreen/music.ogg", "sound")
		self.music.play(loops=-1)

		g.deaths = 0

		self.running = True
		self.buttons = []

		play_button = self.Button((10, 100),
			loader.load("sprites/buttons/play_up.png", "image").convert_alpha(),
			loader.load("sprites/buttons/play_down.png", "image").convert_alpha(),
			self, g.screen_map["info"]
		)

		credit_button = self.Button((10, 155),
			loader.load("sprites/buttons/credits_up.png", "image").convert_alpha(),
			loader.load("sprites/buttons/credits_down.png", "image").convert_alpha(),
			self, g.screen_map["credit"]
		)

		quit_button = self.Button((10, 210),
			loader.load("sprites/buttons/quit_up.png", "image").convert_alpha(),
			loader.load("sprites/buttons/quit_down.png", "image").convert_alpha(),
			self, None
		)

		self.buttons.append(play_button)
		self.buttons.append(credit_button)
		self.buttons.append(quit_button)

	def update(self, inputmanager):
		clicked = False

		for button in self.buttons:
			if not inputmanager.click_pos:
				break

			if button.rect.collidepoint(inputmanager.click_pos):
				if inputmanager.click_state:
					button.state = 1
				else:
					clicked = True
					button.clicked()
			elif button.state:
				button.state = 0

		if clicked:
			self.music.stop()
			inputmanager.reset()

	def draw(self, surface):
		x = (constants.SCREEN_WIDTH - self.background.get_width()) // 2
		y = (constants.SCREEN_HEIGHT - self.background.get_height()) // 2

		surface.blit(self.background, (x, y))

		for button in self.buttons:
			button.draw(surface)

	def peek(self):
		return not self.running
