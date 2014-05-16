#!/usr/bin/env python3

import pygame

import utils
import constants

class Camera(object):
	"A simple camera object."

	def __init__(self, window, level):
		self.level = level
		self.rect = pygame.Rect((0, 0), (window.width, window.height))
		self.buffer = pygame.Rect((0, 0), (constants.BUFFER_WIDTH, constants.BUFFER_HEIGHT))

	def _center(self, target):
		# Find camera position [painful to say the least]
		x = (target.x + (target.width // 2)) - (self.rect.width // 2)
		y = (target.y + (target.height // 2)) - (self.rect.height // 2)

		# Ensure the camera doesn't go off-screen
		x = max(0, x)
		y = max(0, y)
		x = min(self.level.width - self.rect.width, x)
		y = min(self.level.height - self.rect.height, y)

		self.rect.x = x
		self.rect.y = y

		self.buffer.centerx = self.rect.centerx
		self.buffer.centery = self.rect.centery

	def apply(self, target):
		"Applies the camera offset to the target."
		dx = -self.rect.x
		dy = -self.rect.y

		return pygame.Rect(target.x + dx, target.y + dy, target.width, target.height)

	def update(self, target):
		"Update camera position to center to target."
		self._center(target)
