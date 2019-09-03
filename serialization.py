#!/usr/bin/env python3

from model import *


class FieldSerializer(object):
    BINDINGS = [
        (Empty, ' '),
        (Rock, 'R'),
        (Fish, 'F'),
        (Shrimp, 'S')
    ]

    def __init__(self):
        self._symbols = {cell.TYPE: symbol for cell, symbol in self.BINDINGS}
        self._cells = {symbol: cell for cell, symbol in self.BINDINGS}

    def serialize(self, field):
        lines = [
            str(field.width),
            str(field.height)
        ]
        for y in range(field.height):
            line = []
            for x in range(field.width):
                line.append(self._symbols[field[x, y].TYPE])
            lines.append(''.join(line))
        return '\n'.join(lines)

    def unserialize(self, data):
        lines = data.split('\n')
        width, height = map(int, lines[:2])
        field = Field(width, height)
        for y in range(height):
            line = lines[y + 2]
            for x in range(width):
                field[x, y] = self._cells[line[x]]()
        return field
