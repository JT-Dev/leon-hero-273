#!/usr/bin/env python3

import pygame

import constants
from . import base

class Solid(base.Entity):
	def __init__(self, position, loader, texture):
		super().__init__()

		textures = {
			"grass": loader.load("textures/grass.png", "image").convert_alpha(),
			"dirt": loader.load("textures/dirt.png", "image").convert_alpha(),
			"platform": loader.load("textures/platform.png", "image").convert_alpha(),
			"invisible": None
		}

		self.image = textures[texture]
		self.rect = pygame.Rect(position.x, position.y, constants.CELL_WIDTH, constants.CELL_HEIGHT)

	def update(self, inputmanager):
		# Solids don't need to be updated
		pass
