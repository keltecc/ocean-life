#!/usr/bin/env python3

from .cells import Empty
from .field import Field


class Game(object):
    def __init__(self, field):
        self._field = field

    @property
    def field(self):
        return self._field

    def tick(self):
        new_field = Field(self._field.width, self._field.height)
        for x in range(self._field.width):
            for y in range(self._field.height):
                cells_around = self.count_cells_around(x, y)
                new_field[x, y] = self._field[x, y].update(cells_around)
        self._field = new_field

    def count_cells_around(self, center_x, center_y, delta=1, ignore_type=Empty.TYPE):
        cells_around = dict()
        for x in range(center_x-delta, center_x+delta+1):
            for y in range(center_y-delta, center_y+delta+1):
                if x == center_x and y == center_y:
                    continue
                cell_type = self._field[x, y].TYPE
                if cell_type == ignore_type:
                    continue
                if cell_type not in cells_around:
                    cells_around[cell_type] = 0
                cells_around[cell_type] += 1
        return cells_around
