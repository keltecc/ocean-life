#!/usr/bin/env python3

from .cells import Empty


class Field(object):
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._field = None
        self._out_of_field_cell = Empty()
        self.clear()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @classmethod
    def load(self, cells):
        width = len(cells)
        height = len(cells[0])
        field = Field(width, height)
        for x in range(width):
            for y in range(height):
                field[x, y] = cells[x][y]
        return field

    def clear(self, cell_class=Empty):
        self._field = []
        for x in range(self._width):
            self._field.append([])
            for y in range(self._height):
                self._field[x].append(cell_class())

    def _check_key(self, key):
        if not isinstance(key, tuple) and not isinstance(key, list):
            raise TypeError('wrong key type')
        if len(key) != 2:
            raise ValueError('wrong key length')

    def _check_bounds(self, x, y):
        return 0 <= x < self._width and \
               0 <= y < self._height

    def __getitem__(self, key):
        self._check_key(key)
        x, y = key
        if self._check_bounds(x, y):
            return self._field[x][y]
        return self._out_of_field_cell

    def __setitem__(self, key, value):
        self._check_key(key)
        x, y = key
        if not self._check_bounds(x, y):
            raise ValueError('cell is out of field')
        self._field[x][y] = value
