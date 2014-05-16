#!/usr/bin/env python3

import pygame

import g
import utils
import constants

class CreditScreen(object):
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
		self.credits_plain_text = [
			"Programming:",
			"Aleksa Sarai (cyphar.com) [engine, camera, player]",
			"James Ridey [enemies]",
			"",
			"Graphics:",
			"Tom Gosby",
			"",
			"Level Design:",
			"Tom Gosby [the skillful ones]",
			"James Ridey [the hard ones]",
			"",
			"SFX:",
			"Tom Gosby",
			"",
			"Music:",
			"Theme for Harold v2 Kevin MacLeod (incompetech.com)",
			"Chipper Doodle v2 Kevin MacLeod (incompetech.com)",
			"Mellowtron Kevin MacLeod (incompetech.com)",
			"Move Forward Kevin MacLeod (incompetech.com)",
			"Licensed under Creative Commons: By Attribution 3.0",
		]

		self.credits_font = loader.load("fonts/kenvector_future.ttf", "font", size=26)

		self.music = loader.load("sounds/titlescreen/music.ogg", "sound")
		self.music.play(loops=-1)

		self.running = True
		self.buttons = []

		menu_button = self.Button((constants.SCREEN_WIDTH / 2 - 190 / 2, constants.SCREEN_HEIGHT - 50 - 40),
			loader.load("sprites/buttons/back_up.png", "image").convert_alpha(),
			loader.load("sprites/buttons/back_down.png", "image").convert_alpha(),
			self, g.screen_map["title"]
		)

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
			self.music.stop()
			inputmanager.reset()

	def draw(self, surface):
		for button in self.buttons:
			button.draw(surface)

		label = utils.TextWrapping().render_textrect(self.credits_plain_text, self.credits_font, pygame.Rect((0,0),(constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT - 150)), (255,255,255))

		#x = (constants.SCREEN_WIDTH - label.get_width()) // 2
		#y = (constants.SCREEN_HEIGHT - label.get_height()) // 2

		x = 100
		y = 40

		surface.blit(label, (x, y))

	def peek(self):
		return not self.running
