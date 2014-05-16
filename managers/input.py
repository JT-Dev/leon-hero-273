#!/usr/bin/env python3

import pygame.locals

class InputManager(object):
	OFF = 0
	ON = 1
	OLD_ON = 2

	def __init__(self):
		self.keys = {}
		self.click_pos = None
		self.click_state = False

	def handle(self, event):
		if event.type == pygame.locals.KEYDOWN:
			self.keys[event.key] = self.ON
		elif event.type == pygame.locals.KEYUP:
			self.keys[event.key] = self.OFF
		elif event.type == pygame.locals.MOUSEBUTTONDOWN:
			self.click_pos = event.pos
			self.click_state = True
		elif event.type == pygame.locals.MOUSEBUTTONUP:
			self.click_pos = event.pos
			self.click_state = False

	def check_key(self, key):
		return self.keys.get(key, self.OFF) != self.OFF

	def check_key_single(self, key):
		state = self.keys.get(key, self.OFF)

		if state == self.ON:
			self.keys[key] = self.OLD_ON

		return state == self.ON

	def reset(self):
		self.keys = {}
		self.click_pos = None
		self.click_state = False
