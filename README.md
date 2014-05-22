Leon: Hero 273
--------------

A game made for a 48-hour Game Jam.

## Features ##
* Python 3 + PyGame.
* Fully customisable levels (they're all stored as text files in `assets/levels/*.txt`).
* 2D Platformer with basic physics.
* Proper collision detection (better than Game Maker, at the very least).

### Writing Levels ###
Each level is a square (use `*` to make it so). Every entity is represented by a single character.

* ` ` Nothing.
* `*` Invisible wall.
* `P` The player (only one per map). 2 blocks tall.
* `E` End door. 2 blocks tall and 2 blocks wide.
* `a` Aeron (jumping enemy).
* `n` Sandwich (mobile spike).
* `^` Spike.

N.B: Entities do not update if they are outside the camera viewport.

## License ##
The code is licensed under the MIT License.

```
Leon: Hero 273 -- A game made for a 48-hour game jam.
Copyright (C) 2014 JT-Dev

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

The sprites and sound effects are not currently licensed (and therefore are Copyright (C) 2014 Tom Gosby).
