#!/usr/bin/env python3


class Cell(object):
    TYPE = None

    def update(self, cells_around):
        return self


class Empty(Cell):
    TYPE = 0

    def update(self, cells_around):
        if cells_around.get(Fish.TYPE, 0) == Fish.SPAWN_COUNT:
            return Fish()
        if cells_around.get(Shrimp.TYPE, 0) == Shrimp.SPAWN_COUNT:
            return Shrimp()
        return super().update(cells_around)


class Rock(Cell):
    TYPE = 1


class Lifeform(Cell):
    TYPE = 2
    SPAWN_COUNT = 3

    def __init__(self):
        super().__init__()
        self._live = [2, 3]

    def update(self, cells_around):
        if cells_around.get(self.TYPE, 0) not in self._live:
            return Empty()
        return super().update(cells_around)


class Fish(Lifeform):
    TYPE = 3


class Shrimp(Lifeform):
    TYPE = 4
