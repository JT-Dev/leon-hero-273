#!/usr/bin/env python3

import pygame

import g
import sys
import os
import core
import constants
import managers
import utils
import entities

def init_levels(levels, window, loader):
	for index, level in enumerate(levels):
		world = lambda window=window, index=index, level=level, loader=loader: core.World(window, index, level, loader)
		g.screen_map[index] = world

	splashscreen = lambda loader=loader: core.SplashScreen(loader)
	g.screen_map["splash"] = splashscreen

	titlescreen = lambda loader=loader: core.TitleScreen(loader)
	g.screen_map["title"] = titlescreen

	creditscreen = lambda loader=loader: core.CreditScreen(loader)
	g.screen_map["credit"] = creditscreen

	infoscreen = lambda loader=loader: core.InfoScreen(loader)
	g.screen_map["info"] = infoscreen

	winscreen = lambda loader=loader: core.WinScreen(loader)
	g.screen_map["win"] = winscreen


class Game(object):
	def __init__(self, window, surface, loader):
		self.running = True
		self.force_update = False
		self.fps_clock = pygame.time.Clock()

		self.window = window
		self.surface = surface

		self.loader = loader
		self.inputmanager = managers.InputManager()

		self.tracks = [
			loader.load("sounds/gameloops/music1.ogg", "sound"),
			loader.load("sounds/gameloops/music2.ogg", "sound"),
			loader.load("sounds/gameloops/music3.ogg", "sound"),
		]

	def init(self):
		g.screens = []
		levels = []

		for asset in sorted(os.listdir(os.path.join(constants.ASSET_DIR, "levels"))):
			if asset.endswith(".txt"):
				asset = os.path.join("levels", asset)
				level = [line.strip() for line in self.loader.load(asset, "text")]
				levels.append(level)

		init_levels(levels, self.window, self.loader)

		if not g.screen_map:
			utils.error("no screens! panic!")

		g.screen = g.screen_map["splash"]

	def _update(self):
		if not g.screen_map:
			utils.error(".init() not run -- what are you playing at?")

		pygame.event.pump()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				utils.debug("quit signal caught")
				self.running = False
				return

			self.inputmanager.handle(event)

		if self.inputmanager.check_key(pygame.K_q):
			self.running = False
			return

		if self.inputmanager.check_key_single(pygame.K_m):
			g.screen = g.screen_map["title"]
			self.force_update = True
			return

		if self.inputmanager.check_key_single(pygame.K_r):
			g.deaths += 1
			self.force_update = True
			return

		#if self.inputmanager.check_key_single(pygame.K_n):
			#if isinstance(self.screen, core.World):
				#g.screen = g.screen_map.get(self.screen.index+1, g.screen_map["win"])
				#self.force_update = True
				#return

		self.screen.update(self.inputmanager)

	def _draw(self):
		if self.force_update:
			return

		self.surface.fill((0, 0, 0))
		self.screen.draw(self.surface)
		pygame.display.update()

	def run(self):
		utils.debug("Starting main game loop ...")

		self.screen = g.screen()
		while self.running:
			self._update()
			self._draw()

			if self.screen.peek() or self.force_update:
				if (isinstance(self.screen, core.World)):
					self.tracks[self.screen.index % 3].stop()

				self.screen = g.screen()
				if (isinstance(self.screen, core.World)):
					self.tracks[self.screen.index % 3].play(loops=-1)

				self.force_update = False
			self.fps_clock.tick(60)

		pygame.quit()
		sys.exit()

def _init_game():
	# Dem inits tho.
	pygame.init()
	pygame.display.init()
	pygame.mixer.init()

	# File loader
	loader = utils.FileLoader(constants.ASSET_DIR)

	# Icons
	pygame.display.set_icon(loader.load("sprites/icon.png", "image"))

	# Get best screen resolution.
	constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT = pygame.display.list_modes()[0]
	#constants.SCREEN_WIDTH = 640
	#constants.SCREEN_HEIGHT = 480

	# Buffer
	constants.BUFFER_WIDTH, constants.BUFFER_HEIGHT = constants.SCREEN_WIDTH + 200, constants.SCREEN_HEIGHT + 200

	# Set up screen surface.
	os.environ["SDL_VIDEO_CENTERED"] = "1"
	window = utils.Size(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
	surface = pygame.display.set_mode((window.width, window.height), pygame.FULLSCREEN)

	game = Game(window, surface, loader)
	game.init()

	return game

def _play_game():
	game = _init_game()
	game.run()

if __name__ == "__main__":
	_play_game()
