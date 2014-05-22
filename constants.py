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

import utils

# Assets
ASSET_DIR = "assets"

# Full of dem constants
GAME_NAME = "leon-hero-273"

# Splash
SPLASH_LENGTH = 3.14

# Windows
WIN_WIDTH = 640
WIN_HEIGHT = 480

# Cells
CELL_WIDTH = 32
CELL_HEIGHT = 32

# Physics
GRAVITY = 1.3
FRICTION = 0.6
RESISTANCE = 0.75

# Player
PLAYER_HEIGHT = CELL_HEIGHT * 2
PLAYER_WIDTH = CELL_WIDTH

PLAYER_ACCELERATION = 3.0
PLAYER_JUMP_SPEED = 20.0
PLAYER_MAX_JUMPS = 2.0
PLAYER_MAX_SPEED = 24.0
PLAYER_TERMINAL_SPEED = 35.0

PLAYER_WALK_DELAY = 7
PLAYER_EXPLOSION_DELAY = 7

#Aeron Enemy
ENEMY_AERON_JUMP_SPEED = 10
ENEMY_AERON_MOVE_SPEED = 7

#Sandwich Enemy
ENEMY_SANDWICH_MOVE_SPEED = 2
ENEMY_SANDWICH_MAX_SPEED = 10

# Win screen
WIN_PLAYER_SIZE = (320, 640)

# End door
END_WIDTH = 64
END_HEIGHT = 64

# Print levels
VERBOSE = 0
DEBUG   = 1
INFO	= 2
WARN	= 4
ERROR   = 8

# XXX: Change this to WARN in production.
PRINT_LEVEL = DEBUG
