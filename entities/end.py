#!/usr/bin/env python3

import pygame

import constants
from . import base

class EndDoor(base.Entity):
	def __init__(self, position, loader):
		super().__init__()

		self.image = loader.load("sprites/door.png", "image")
		self.rect = pygame.Rect(position.x, position.y, constants.END_WIDTH, constants.END_HEIGHT)

	def update(self, inputmanager):
		# Solids don't need to be updated
		pass
