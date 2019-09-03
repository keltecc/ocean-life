#!/usr/bin/env python3

from argparse import ArgumentParser

from view.ui import UI
from model.game import Game
from serialization import FileSerializer, UISerializer


def parse_args():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--tick-time', metavar='milliseconds', type=int, default=200, help='tick time')
    group.add_argument('-c', '--confirm', action='store_true', help='confirm each step by pressing ENTER')
    parser.add_argument('-s', '--save', metavar='filename', help='after execution save field to file')
    parser.add_argument('-f', '--field', metavar='filename', required=True, help='path to file with field')
    return parser.parse_args()


class FieldIO(object):
    def __init__(self, serializer):
        self._serializer = serializer

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            data = file.read()
        return self._serializer.unserialize(data)

    def save_to_file(self, filename, field):
        data = self._serializer.serialize(field)
        with open(filename, 'w') as file:
            file.write(data)


def main():
    args = parse_args()
    field_io = FieldIO(FileSerializer())
    field = field_io.load_from_file(args.field)
    game = Game(field)
    ui = UI(game, UISerializer())
    ui.run(args.tick_time, args.confirm)
    if args.save:
        field_io.save_to_file(args.save, game.field)
        print('Field saved.')


if __name__ == '__main__':
    main()
