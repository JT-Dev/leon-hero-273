#!/usr/bin/env python3

import pygame

import random
import constants
import utils
from . import base

class Aeron(base.Entity):
	def __init__(self, pos, loader):
		super().__init__()

		self.dying_timer = -1
		self.grounded_timer = 0

		self.dead = False
		self.velocity = utils.Vector(0, 0)

		self.left = random.randint(0, 1)
		self.in_air = False

		self.sprites = {
			"air": loader.load("sprites/aeron/air.png", "image").convert_alpha(),
			"ground": loader.load("sprites/aeron/grounded.png", "image").convert_alpha(),
			"dead": loader.load("sprites/aeron/crushed.png", "image").convert_alpha()
		}

		self.image = self.sprites["air"]

		self.sounds = {
			"die": loader.load("sounds/sfx/aeron_die.wav", "sound")
		}

		self.rect = pygame.Rect((pos.x, pos.y), self.image.get_rect().size)
		self.jump_speed = constants.ENEMY_AERON_JUMP_SPEED
		self.move_speed = constants.ENEMY_AERON_MOVE_SPEED

	def distance(self, other):
		return ((self.rect.centerx - other.rect.centerx) ** 2 + (self.rect.centery - other.rect.centery) ** 2) ** 0.5

	def update(self, solids):
		if self.dying_timer == -1:
			self.velocity.y += constants.GRAVITY

			if not self.in_air:
				self.velocity.x = 0
				self.grounded_timer += 1

			if self.grounded_timer > 100:
				self.grounded_timer = 0
				self.velocity.x = -self.move_speed if self.left else self.move_speed
				self.velocity.y = -self.jump_speed
				self.in_air = True

			dx = self.velocity.x
			dy = self.velocity.y

			x_rect = pygame.Rect(self.rect.x + dx, self.rect.y,      self.rect.width, self.rect.height)
			y_rect = pygame.Rect(self.rect.x,      self.rect.y + dy, self.rect.width, self.rect.height)

			for solid in solids:
				if self.distance(solid) > 100:
					continue
				self._check_collide(solid, x_rect, y_rect)

			self.rect.x += self.velocity.x
			self.rect.y += self.velocity.y

			if self.in_air:
				self.image = self.sprites["air"]
			else:
				self.image = self.sprites["ground"]

			if self.left:
				self.image = pygame.transform.flip(self.image, True, False)
		else:
			self.dying_timer -= 1

	def _check_collide(self, solid, x_rect, y_rect):
		if solid.rect.colliderect(x_rect):
			self.left = not self.left
			self.velocity.x = 0

		if solid.rect.colliderect(y_rect):
			if self.velocity.y > 0:
				self.in_air = False
			self.velocity.y = 0

	def kill(self):
		self.sounds["die"].play()
		self.dead = True

	def collision(self, player):
		if self.rect.top <= player.rect.bottom and player.velocity.y > 0:
			player.velocity.y = -constants.PLAYER_JUMP_SPEED

			self.image = self.sprites["dead"]
			self.velocity.x = 0
			self.dying_timer = 50
			self.kill()
		else:
			player.kill()
