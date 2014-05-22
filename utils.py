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

import constants
import sys
import os

def verbose(*args, **kwargs):
	if constants.PRINT_LEVEL >= constants.VERBOSE:
		print("[%s:V]" % constants.GAME_NAME, *args)

def debug(*args, **kwargs):
	if constants.PRINT_LEVEL >= constants.DEBUG:
		print("[%s:D]" % constants.GAME_NAME, *args)

def info(*args, **kwargs):
	if constants.PRINT_LEVEL >= constants.INFO:
		print("[%s:I]" % constants.GAME_NAME, *args)

def warn(*args, **kwargs):
	if constants.PRINT_LEVEL >= constants.WARN:
		print("[%s:W]" % constants.GAME_NAME, *args)

def error(*args, **kwargs):
	if constants.PRINT_LEVEL >= constants.ERROR:
		print("[%s:E]" % constants.GAME_NAME, *args)
		sys.exit()


class Cycler(object):
	def __init__(self, delay=10, *items):
		self.items = items
		self.length = len(items)
		self.index = 0
		self.delay = delay

	def next(self):
		if self.index // self.delay >= self.length:
			self.index = 0

		item = self.items[self.index // self.delay]
		self.index += 1

		return item

class FileLoader(object):
	def __init__(self, assetdir):
		self.cache = {}
		self.assetdir = assetdir

	def load(self, asset, ftype="text", size=12):
		path = os.path.join(self.assetdir, asset)

		if ftype == "text":
			return open(path, "rU")

		f = open(path, "rb")

		e_asset = asset
		if ftype == "font":
			e_asset = "%s:%d" % (asset, size)

		if e_asset in self.cache:
			return self.cache[e_asset]

		if ftype == "image":
			obj = pygame.image.load(f, path)
			self.cache[e_asset] = obj
			return obj

		elif ftype == "sound":
			obj = pygame.mixer.Sound(path)
			self.cache[e_asset] = obj
			return obj

		elif ftype == "font":
			obj = pygame.font.Font(path, size)
			self.cache[e_asset] = obj
			return obj

class TextWrapping:
	def __init__(self):
		pass

	def render_textrect(self, string, font, rect, text_color, background_color=0, justification=0):
		"""Returns a surface containing the passed text string, reformatted
		to fit within the given rect, word-wrapping as necessary. The text
		will be anti-aliased.

		Takes the following arguments:

		string - the text you wish to render. \n begins a new line.
		font - a Font object
		rect - a rectstyle giving the size of the surface requested.
		text_color - a three-byte tuple of the rgb value of the
			 text color. ex (0, 0, 0) = BLACK
		background_color - a three-byte tuple of the rgb value of the surface.
		justification - 0 (default) left-justified
				1 horizontally centered
				2 right-justified

		Returns the following values:

		Success - a surface object with the text rendered onto it.
		Failure - raises a TextRectException if the text won't fit onto the surface.
		"""
		final_lines = []

		requested_lines = string#.splitlines()

		# Create a series of lines that will fit on the provided
		# rectangle.

		for requested_line in requested_lines:
			if font.size(requested_line)[0] > rect.width:
				words = requested_line.split(' ')
				# if any of our words are too long to fit, return.
				for word in words:
					if font.size(word)[0] >= rect.width:
						error("The word " + word + " is too long to fit in the rect passed.")
				# Start a new line
				accumulated_line = ""
				for word in words:
					test_line = accumulated_line + word + " "
					# Build the line while the words fit.
					if font.size(test_line)[0] < rect.width:
						accumulated_line = test_line
					else:
						final_lines.append(accumulated_line)
						accumulated_line = word + " "
				final_lines.append(accumulated_line)
			else:
				final_lines.append(requested_line)

		# Let's try to write the text out on the surface.

		surface = pygame.Surface(rect.size)
		surface.fill(background_color)

		accumulated_height = 0
		for line in final_lines:
			if accumulated_height + font.size(line)[1] >= rect.height:
				error("Once word-wrapped, the text string was too tall to fit in the rect.")
			if line != "":
				tempsurface = font.render(line, 1, text_color)
				if justification == 0:
					surface.blit(tempsurface, (0, accumulated_height))
				elif justification == 1:
					surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
				elif justification == 2:
					surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
				else:
					error("Invalid justification argument: " + str(justification))
			accumulated_height += font.size(line)[1]

		return surface


class Size(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height


class Vector(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y


class Position(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
