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
import constants
import utils

from . import base

class Player(base.Entity):
	"The player."

	RIGHT = 0
	LEFT = 1

	def __init__(self, position, loader):
		super().__init__()

		self.dying = False
		self.dead = False
		self.direction = self.RIGHT
		self.jump_level = 0

		self.on_floor = False
		self.velocity = utils.Vector(0.0, 0.0)

		self.sprites = {
			"still": loader.load("sprites/leon/still.png", "image").convert_alpha(),
			"air": loader.load("sprites/leon/air.png", "image").convert_alpha(),
			"walk": utils.Cycler(constants.PLAYER_WALK_DELAY,
				loader.load("sprites/leon/walk-1.png", "image").convert_alpha(),
				loader.load("sprites/leon/walk-2.png", "image").convert_alpha(),
				loader.load("sprites/leon/walk-3.png", "image").convert_alpha(),
				loader.load("sprites/leon/walk-2.png", "image").convert_alpha()),
			"explosion": utils.Cycler(constants.PLAYER_EXPLOSION_DELAY,
				loader.load("sprites/explosion/explosion-1.png", "image").convert_alpha(),
				loader.load("sprites/explosion/explosion-2.png", "image").convert_alpha(),
				loader.load("sprites/explosion/explosion-3.png", "image").convert_alpha(),
				loader.load("sprites/explosion/explosion-4.png", "image").convert_alpha(),
				loader.load("sprites/explosion/explosion-5.png", "image").convert_alpha())
		}

		self.sounds = {
			"die": loader.load("sounds/sfx/player_die.wav", "sound"),
			"jump": loader.load("sounds/sfx/player_jump.wav", "sound"),
		}

		self.image = None

		self.rect = pygame.Rect(position.x, position.y, constants.PLAYER_WIDTH, constants.PLAYER_HEIGHT)

	def update(self, inputmanager, solids):
		if not self.dying and not self.dead:
			if self.on_floor:
				self.velocity.x *= constants.FRICTION
			else:
				self.velocity.x *= constants.RESISTANCE

			self.velocity.y += constants.GRAVITY

			if inputmanager.check_key(pygame.K_LEFT):
				self.velocity.x -= constants.PLAYER_ACCELERATION
				self.direction = self.LEFT

			if inputmanager.check_key(pygame.K_RIGHT):
				self.velocity.x += constants.PLAYER_ACCELERATION
				self.direction = self.RIGHT

			if inputmanager.check_key_single(pygame.K_UP):
				if self.jump_level < constants.PLAYER_MAX_JUMPS:
					self.sounds["jump"].play()
					self.velocity.y = -constants.PLAYER_JUMP_SPEED
					self.jump_level += 1

			self.velocity.x = min(self.velocity.x, constants.PLAYER_MAX_SPEED)
			self.velocity.x = max(self.velocity.x, -constants.PLAYER_MAX_SPEED)

			if abs(self.velocity.x) < 0.5:
				self.velocity.x = 0.0
			if abs(self.velocity.y) < 0.5:
				self.velocity.y = 0.0

			dx = self.velocity.x
			dy = self.velocity.y

			self.on_floor = False
			for solid in solids:
				self._check_collide(solid, utils.Vector(dx, dy))

			self.rect.x += self.velocity.x
			self.rect.y += self.velocity.y

		self._update_sprite()

	def _check_collide(self, solid, displacement):
		dx = displacement.x
		dy = displacement.y

		x_rect = pygame.Rect(self.rect.x + dx, self.rect.y,      self.rect.width, self.rect.height)
		y_rect = pygame.Rect(self.rect.x,      self.rect.y + dy, self.rect.width, self.rect.height)
		rect   = pygame.Rect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height)

		if solid.rect.colliderect(x_rect):
			self.velocity.x = 0.0

		if solid.rect.colliderect(y_rect):
			if dy > 0:
				self.on_floor = True
				self.jump_level = 0
			self.velocity.y = 0.0

		# Handle goddamn pixel retardation
		if self.direction == self.LEFT:
			rect.y -= 1.0

		if self.velocity.x and self.velocity.y:
			if solid.rect.colliderect(rect):
				self.velocity.x = 0.0
				self.velocity.y = 0.0

	def _update_sprite(self):
		# Default: stationary.
		self.image = self.sprites["still"]

		# Flying.
		if not self.on_floor:
			self.image = self.sprites["air"]

		# Moving on floor.
		elif abs(self.velocity.x) > constants.PLAYER_ACCELERATION:
			self.image = self.sprites["walk"].next()

		# All sprites are facing right.
		if self.direction == self.LEFT:
			self.image = pygame.transform.flip(self.image, True, False)

		if self.dying:
			temp_explosion = self.sprites["explosion"]
			temp_image = temp_explosion.next()

			self.image = temp_image
			if (temp_explosion.index // temp_explosion.delay) >= self.sprites["explosion"].length:
				self.dead = True

	def kill(self):
		if self.dying or self.dead:
			return

		self.sounds["die"].play()
		self.dying = True

		self.image = self.sprites["explosion"].items[0]
		self.rect.x -= -(self.rect.width - self.image.get_width()) // 2
		self.rect.y -= -(self.rect.height - self.image.get_height()) // 2

		g.deaths += 1

	def collides(self, other):
		return self.rect.colliderect(other)

	def collision(self):
		pass
