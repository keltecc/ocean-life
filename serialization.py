#!/usr/bin/env python3

from model import *


_BINDINGS = [
    (Empty, ' '),
    (Rock, 'R'),
    (Fish, 'F'),
    (Shrimp, 'S')
]

_SYMBOLS = {cell.TYPE: symbol for cell, symbol in _BINDINGS}
_CELLS = {symbol: cell for cell, symbol in _BINDINGS}


def _field_to_lines(field):
    lines = []
    for y in range(field.height):
        line = []
        for x in range(field.width):
            line.append(_SYMBOLS[field[x, y].TYPE])
        lines.append(''.join(line))
    return lines


def _lines_to_field(width, height, lines):
    field = Field(width, height)
    for y in range(height):
        line = lines[y]
        for x in range(width):
            field[x, y] = _CELLS[line[x]]()
    return field


class BaseSerializer(object):
    def serialize(self, field):
        raise NotImplementedError('serialization is not implemented')

    def unserialize(self, data):
        raise NotImplementedError('unserialization is not implemented')


class FileSerializer(BaseSerializer):
    def serialize(self, field):
        lines = [
            str(field.width),
            str(field.height),
        ]
        lines += _field_to_lines(field)
        return '\n'.join(lines)

    def unserialize(self, data):
        lines = data.split('\n')
        width, height = map(int, lines[:2])
        return _lines_to_field(width, height, lines[2:])


class UISerializer(BaseSerializer):
    HORIZONTAL = '─'
    VERTICAL = '│'
    TOP_LEFT = '┌'
    TOP_RIGHT = '┐'
    BOTTOM_LEFT = '└'
    BOTTOM_RIGHT = '┘'

    def serialize(self, field):
        lines = ['"{0}" - {1}'.format(symbol, cell.__name__) for symbol, cell in _CELLS.items()]
        horizontal = self.HORIZONTAL * field.width
        lines.append(self.TOP_LEFT + horizontal + self.TOP_RIGHT)
        for line in _field_to_lines(field):
            lines.append(self.VERTICAL + line + self.VERTICAL)
        lines.append(self.BOTTOM_LEFT + horizontal + self.BOTTOM_RIGHT)
        return '\n'.join(lines)
