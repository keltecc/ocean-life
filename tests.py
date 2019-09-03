#!/usr/bin/env python3

from model import *
from serialization import FileSerializer


class FieldTests(object):
    @staticmethod
    def empty_initialization():
        field = Field(2, 2)

        assert field[0, 0].TYPE == Empty.TYPE
        assert field[0, 1].TYPE == Empty.TYPE
        assert field[1, 0].TYPE == Empty.TYPE
        assert field[1, 1].TYPE == Empty.TYPE

    @staticmethod
    def out_of_field_empty():
        field = Field(2, 2)

        assert field[-1, 0].TYPE == Empty.TYPE
        assert field[2, 0].TYPE == Empty.TYPE
        assert field[0, -1].TYPE == Empty.TYPE
        assert field[0, 2].TYPE == Empty.TYPE
        assert field[-1, -1].TYPE == Empty.TYPE
        assert field[-1, 2].TYPE == Empty.TYPE
        assert field[2, -1].TYPE == Empty.TYPE
        assert field[2, 2].TYPE == Empty.TYPE

    @staticmethod
    def set_cell():
        field = Field(2, 2)

        field[0, 0] = Fish()

        assert field[0, 0].TYPE == Fish.TYPE

    @staticmethod
    def clear_fills_cells():
        field = Field(2, 2)

        field.clear(Rock)

        assert field[0, 0].TYPE == Rock.TYPE
        assert field[0, 1].TYPE == Rock.TYPE
        assert field[1, 0].TYPE == Rock.TYPE
        assert field[1, 1].TYPE == Rock.TYPE


class CoundAroundTests(object):
    @staticmethod
    def empty_field():
        game = Game(Field(0, 0))

        cells_around = game.count_cells_around(0, 0)

        assert len(cells_around) == 0

    @staticmethod
    def ignore_empty():
        game = Game(Field(2, 2))

        cells_around = game.count_cells_around(0, 0)

        assert cells_around.get(Empty.TYPE, 0) == 0

    @staticmethod
    def ignore_center():
        game = Game(Field(2, 2))
        game.field[0, 0] = Fish()

        cells_around = game.count_cells_around(0, 0)

        assert cells_around.get(Fish.TYPE, 0) == 0

    @staticmethod
    def different_types():
        game = Game(Field(2, 2))
        game.field[0, 0] = Fish()
        game.field[0, 1] = Rock()
        game.field[1, 0] = Shrimp()

        cells_around = game.count_cells_around(1, 1)

        assert cells_around.get(Fish.TYPE, 0) == 1
        assert cells_around.get(Rock.TYPE, 0) == 1
        assert cells_around.get(Shrimp.TYPE, 0) == 1


class TickTests(object):
    @staticmethod
    def empty_constant():
        game = Game(Field(2, 2))

        game.tick()

        assert game.field[0, 0].TYPE == Empty.TYPE
        assert game.field[0, 1].TYPE == Empty.TYPE
        assert game.field[1, 0].TYPE == Empty.TYPE
        assert game.field[1, 1].TYPE == Empty.TYPE

    @staticmethod
    def rock_constant():
        game = Game(Field(2, 2))
        game.field[0, 0] = Rock()

        game.tick()

        assert game.field[0, 0].TYPE == Rock.TYPE

    @staticmethod
    def lifeform_lonely_dying():
        game = Game(Field(2, 2))
        game.field[0, 0] = Lifeform()

        game.tick()

        assert game.field[0, 0].TYPE == Empty.TYPE

    @staticmethod
    def lifeform_overpopulation_dying():
        game = Game(Field(3, 3))
        game.field[0, 1] = Lifeform()
        game.field[1, 1] = Lifeform()
        game.field[2, 1] = Lifeform()
        game.field[1, 0] = Lifeform()
        game.field[1, 2] = Lifeform()

        game.tick()

        assert game.field[1, 1].TYPE == Empty.TYPE

    @staticmethod
    def lifeform_living_1():
        game = Game(Field(2, 2))
        game.field[0, 0] = Lifeform()
        game.field[0, 1] = Lifeform()
        game.field[1, 0] = Lifeform()

        game.tick()

        assert game.field[0, 0].TYPE == Lifeform.TYPE

    @staticmethod
    def lifeform_living_2():
        game = Game(Field(2, 2))
        game.field[0, 0] = Lifeform()
        game.field[0, 1] = Lifeform()
        game.field[1, 0] = Lifeform()
        game.field[1, 1] = Lifeform()

        game.tick()

        assert game.field[0, 0].TYPE == Lifeform.TYPE

    @staticmethod
    def fish_living_while_shrimp_overpopulation():
        game = Game(Field(3, 3))
        game.field[0, 0] = Fish()
        game.field[0, 1] = Fish()
        game.field[0, 2] = Shrimp()
        game.field[1, 0] = Shrimp()
        game.field[1, 1] = Fish()
        game.field[1, 2] = Shrimp()
        game.field[2, 0] = Shrimp()
        game.field[2, 1] = Shrimp()
        game.field[2, 2] = Shrimp()

        game.tick()

        assert game.field[1, 1].TYPE == Fish.TYPE

    @staticmethod
    def fish_spawns_first():
        game = Game(Field(3, 3))
        game.field[0, 0] = Fish()
        game.field[0, 1] = Fish()
        game.field[0, 2] = Fish()
        game.field[2, 0] = Shrimp()
        game.field[2, 1] = Shrimp()
        game.field[2, 2] = Shrimp()

        game.tick()

        assert game.field[1, 1].TYPE == Fish.TYPE

    @staticmethod
    def shrimp_spawns_second():
        game = Game(Field(3, 3))
        game.field[0, 0] = Fish()
        game.field[0, 1] = Fish()
        game.field[2, 0] = Shrimp()
        game.field[2, 1] = Shrimp()
        game.field[2, 2] = Shrimp()

        game.tick()

        assert game.field[1, 1].TYPE == Shrimp.TYPE        


class FiguresTests(object):
    @staticmethod
    def compare(field1, field2):
        assert field1.width == field2.width
        assert field1.height == field2.height

        for x in range(field1.width):
            for y in range(field1.height):
                assert field1[x, y].TYPE == field2[x, y].TYPE

    @staticmethod
    def block():
        game = Game(Field.load([
            [Fish(), Fish()],
            [Fish(), Fish()]
        ]))

        game.tick()

        expected = Field.load([
            [Fish(), Fish()],
            [Fish(), Fish()]
        ])
        FiguresTests.compare(game.field, expected)

    @staticmethod
    def blinker():
        game = Game(Field.load([
            [Empty(), Empty(), Empty()],
            [Fish(), Fish(), Fish()],
            [Empty(), Empty(), Empty()]
        ]))

        game.tick()

        expected = Field.load([
            [Empty(), Fish(), Empty()],
            [Empty(), Fish(), Empty()],
            [Empty(), Fish(), Empty()]
        ])
        FiguresTests.compare(game.field, expected)

    @staticmethod
    def glider():
        game = Game(Field.load([
            [Empty(), Fish(), Empty()],
            [Empty(), Empty(), Fish()],
            [Fish(), Fish(), Fish()],
            [Empty(), Empty(), Empty()]
        ]))

        game.tick()

        expected = Field.load([
            [Empty(), Empty(), Empty()],
            [Fish(), Empty(), Fish()],
            [Empty(), Fish(), Fish()],
            [Empty(), Fish(), Empty()]
        ])
        FiguresTests.compare(game.field, expected)


class SerializationTests(object):
    @staticmethod
    def serialize_empty():
        field = Field(0, 0)

        data = FileSerializer().serialize(field)

        assert data == '0\n0'

    @staticmethod
    def serialize_different_types():
        field = Field(2, 2)
        field[0, 1] = Rock()
        field[1, 0] = Fish()
        field[1, 1] = Shrimp()

        data = FileSerializer().serialize(field)

        assert data == '2\n2\n F\nRS'

    @staticmethod
    def unserialize_empty():
        data = '0\n0'

        field = FileSerializer().unserialize(data)

        assert field.width == 0
        assert field.height == 0

    @staticmethod
    def unserialize_different_types():
        data = '2\n2\n F\nRS'

        field = FileSerializer().unserialize(data)

        assert field.width == 2
        assert field.height == 2
        assert field[0, 0].TYPE == Empty.TYPE
        assert field[0, 1].TYPE == Rock.TYPE
        assert field[1, 0].TYPE == Fish.TYPE
        assert field[1, 1].TYPE == Shrimp.TYPE


if __name__ == '__main__':
    print('Start testing...')

    FieldTests.empty_initialization()
    FieldTests.out_of_field_empty()
    FieldTests.set_cell()
    FieldTests.clear_fills_cells()

    CoundAroundTests.empty_field()
    CoundAroundTests.ignore_empty()
    CoundAroundTests.ignore_center()
    CoundAroundTests.different_types()

    TickTests.empty_constant()
    TickTests.rock_constant()
    TickTests.lifeform_lonely_dying()
    TickTests.lifeform_overpopulation_dying()
    TickTests.lifeform_living_1()
    TickTests.lifeform_living_2()
    TickTests.fish_living_while_shrimp_overpopulation()
    TickTests.fish_spawns_first()
    TickTests.shrimp_spawns_second()

    FiguresTests.block()
    FiguresTests.blinker()
    FiguresTests.glider()

    SerializationTests.serialize_empty()
    SerializationTests.serialize_different_types()
    SerializationTests.unserialize_empty()
    SerializationTests.unserialize_different_types()

    print('All tests passed!')
