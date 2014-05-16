#!/usr/bin/env python3

import pygame

import g
import managers
import constants
import entities
import utils

from . import camera

class Hud(object):
	def __init__(self, loader):
		self.font = loader.load("fonts/kenvector_future.ttf", "font", size=18)
		self.colour = (0, 0, 0)
		self.pos = (10, 10)

	def draw(self, surface):
		outsurface = self.font.render("Deaths: %d" % g.deaths, True, self.colour)
		surface.blit(outsurface, self.pos)

class World(object):
	def __init__(self, window, index, level, loader):
		self.loader = loader

		self.entities = pygame.sprite.Group()
		self.solids = []
		self.enemies = []
		self.end_doors = []
		self.old_time = 0
		self.player = None

		self.index = index
		self.running = True

		width = max(len(line) * constants.CELL_WIDTH for line in level)
		height = len(level) * constants.CELL_HEIGHT
		self.level = utils.Size(width, height)

		self.hud = Hud(loader)
		self.window = window
		self.camera = camera.Camera(self.window, self.level)

		self._level = level
		self._parse_level()

	def _parse_level(self):
		x = y = 0

		for row in self._level:
			for col in row:
				pos = utils.Position(x, y)

				if col == "S":
					solid = entities.Solid(pos, self.loader, "grass")
					self.solids.append(solid)
					self.entities.add(solid)

				elif col == "s":
					solid = entities.Solid(pos, self.loader, "dirt")
					self.solids.append(solid)
					self.entities.add(solid)

				elif col == "_":
					solid = entities.Solid(pos, self.loader, "platform")
					self.solids.append(solid)
					self.entities.add(solid)

				elif col == "*":
					solid = entities.Solid(pos, self.loader, "invisible")
					self.solids.append(solid)

				elif col == "P":
					player = entities.Player(pos, self.loader)
					self.player = player

				elif col == "a":
					aeron = entities.Aeron(pos, self.loader)
					self.enemies.append(aeron)
					self.entities.add(aeron)

				elif col == "n":
					sandwich = entities.Sandwich(pos, self.loader)
					self.enemies.append(sandwich)
					self.entities.add(sandwich)

				elif col == "E":
					end_door = entities.EndDoor(pos, self.loader)
					self.end_doors.append(end_door)
					self.entities.add(end_door)

				elif col == "^":
					spike = entities.Spike(pos, self.loader)
					self.enemies.append(spike)
					self.entities.add(spike)

				x += constants.CELL_WIDTH
			y += constants.CELL_HEIGHT
			x = 0

		if not self.player:
			utils.error("no player in map")

	def update(self, inputmanager):
		self.player.update(inputmanager, self.solids)

		# Entities shouldn't care about solids outside screen.
		solids = [solid for solid in self.solids if solid.rect.colliderect(self.camera.buffer)]

		for door in self.end_doors:
			if self.player.collides(door):
				self.running = False
				g.screen = g.screen_map.get(self.index + 1, g.screen_map["win"])
				return

		if self.player.rect.left < 0 or self.player.rect.right > self.level.width:
			self.player.kill()

		if self.player.rect.top < 0 or self.player.rect.bottom > self.level.height:
			self.player.kill()

		remove_enemy = []
		for enemy in self.enemies:
			if not enemy.rect.colliderect(self.camera.rect):
				continue

			enemy.update(solids)

			if not enemy.dead and self.player.collides(enemy):
				enemy.collision(self.player)

			if enemy.dying_timer == 0:
				remove_enemy.append(enemy)

		for enemy in remove_enemy:
			self.enemies.remove(enemy)
			self.entities.remove(enemy)

		if self.player.dead:
			self.running = False
			g.screen = g.screen_map[self.index]
			return

	def draw(self, surface):
		surface.fill((0x87, 0xCE, 0xEB))
		if not (self.player.dying or self.player.dead):
			self.camera.update(self.player.rect)

		for entity in self.entities:
			if not entity.rect.colliderect(self.camera.rect):
				continue

			surface.blit(entity.image, self.camera.apply(entity.rect))

		surface.blit(self.player.image, self.camera.apply(self.player.rect))
		self.hud.draw(surface)

	def peek(self):
		return not self.running
