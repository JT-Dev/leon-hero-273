#!/usr/bin/env python3

import pygame

class Entity(pygame.sprite.Sprite):
	"The base 'entity' object."

	rect = None

	def __init__(self):
		super().__init__()

	def collides(self, other):
		return self.rect.colliderect(other.rect)
