#!/usr/bin/env python3

import pygame

from . import base

class Spike(base.Entity):
	"A goddamn Spike."

	def __init__(self, pos, loader):
		super().__init__()

		self.dead = False
		self.dying_timer = -1

		self.image = loader.load("sprites/spike.png", "image").convert_alpha()
		self.rect = pygame.Rect((pos.x, pos.y), self.image.get_rect().size)

	def update(self, solids):
		# Spikes don't need to be updated.
		pass

	def collision(self, player):
		player.kill()
