#!/usr/bin/env python3

import pygame

import g
import utils
import constants

class InfoScreen(object):
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
			self.main.running = False
			g.screen = self.screen

		def draw(self, surface):
			if self.state:
				surface.blit(self.image_down, self.rect)
			else:
				surface.blit(self.image_up, self.rect)

	def __init__(self, loader):
		self.text = [
			"You are Leon, the 273rd person to attempt saving the princess. Everyone before you has given up or died.",
			"",
			"Can you make it through the fortresses and fields in your way to get to Lord Apoc's castle and save the princess?",
		]

		self.font = loader.load("fonts/kenvector_future.ttf", "font", size=26)

		self.running = True
		self.buttons = []

		menu_button = self.Button((constants.SCREEN_WIDTH / 2 - 190 / 2, constants.SCREEN_HEIGHT - 50 - 40),
			loader.load("sprites/buttons/play_up.png", "image").convert_alpha(),
			loader.load("sprites/buttons/play_down.png", "image").convert_alpha(),
			self, g.screen_map[0]
		)

		self.player = loader.load("sprites/leon/front.png", "image").convert_alpha()
		self.player = pygame.transform.scale(self.player, constants.WIN_PLAYER_SIZE)

		self.buttons.append(menu_button)

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
			inputmanager.reset()

	def draw(self, surface):
		# Label
		label = utils.TextWrapping().render_textrect(self.text, self.font, pygame.Rect((0, 0), (constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT - 150)), (255, 255, 255))

		x = constants.SCREEN_WIDTH // 2
		y = constants.SCREEN_HEIGHT // 2 - (constants.SCREEN_HEIGHT // 3)

		surface.blit(label, (x, y))

		# Buttahnz
		for button in self.buttons:
			button.draw(surface)

		# Player sprite
		x = ((constants.SCREEN_WIDTH // 2) - self.player.get_width()) // 2
		y = (constants.SCREEN_HEIGHT - self.player.get_height()) // 2

		surface.blit(self.player, (x, y))

	def peek(self):
		return not self.running
