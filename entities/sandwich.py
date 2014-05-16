#!/usr/bin/env python3

import pygame

import utils
import constants
import random
from . import base

class Sandwich(base.Entity):
	def __init__(self, pos, loader):
		super().__init__()

		self.dying_timer = -1
		self.velocity = utils.Vector(0, 0)

		self.dead = False
		self.left = random.randint(0, 1)

		self.image = loader.load("sprites/sandwich/walk1.png", "image").convert_alpha()
		self.walk_image = utils.Cycler(12,
			loader.load("sprites/sandwich/walk1.png", "image").convert_alpha(),
			loader.load("sprites/sandwich/walk2.png", "image").convert_alpha(),
		)

		self.rect = pygame.Rect((pos.x, pos.y), self.image.get_rect().size)
		self.move_speed = constants.ENEMY_SANDWICH_MOVE_SPEED

	def distance(self, other):
		return ((self.rect.centerx - other.rect.centerx) ** 2 + (self.rect.centery - other.rect.centery) ** 2) ** 0.5

	def update(self, solids):
		self.velocity.x += -self.move_speed if self.left else self.move_speed
		self.velocity.y += constants.GRAVITY

		self.velocity.x *= constants.FRICTION

		self.velocity.x = min(self.velocity.x, constants.ENEMY_SANDWICH_MAX_SPEED)
		self.velocity.x = max(self.velocity.x, -constants.ENEMY_SANDWICH_MAX_SPEED)

		dx = self.velocity.x
		dy = self.velocity.y

		x_rect = pygame.Rect(self.rect.x + dx, self.rect.y,      self.rect.width, self.rect.height)
		y_rect = pygame.Rect(self.rect.x,      self.rect.y + dy, self.rect.width, self.rect.height)

		for solid in solids:
			if self.distance(solid) > 100:
				continue

			self._check_collide(solid, x_rect, y_rect)

		if self.velocity.y > 0:
			self.velocity.x = -self.velocity.x
			self.velocity.y = 0
			self.left = not self.left

		self.rect.x += self.velocity.x
		self.rect.y += self.velocity.y

		self.image = self.walk_image.next()

		if self.left:
			self.image = pygame.transform.flip(self.image, True, False)

	def _check_collide(self, solid, x_rect, y_rect):
		if solid.rect.colliderect(x_rect):
			self.left = not self.left
			self.velocity.x = 0

		if solid.rect.colliderect(y_rect):
			self.velocity.y = 0

	def collision(self, player):
		player.kill()
