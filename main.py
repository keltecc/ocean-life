#!/usr/bin/env python3

from argparse import ArgumentParser

from view.ui import UI
from model.game import Game
from serialization import FieldSerializer


def parse_args():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--tick-time', metavar='milliseconds', type=int, default=200, help='tick time')
    group.add_argument('-c', '--confirm', action='store_true', help='confirm each step by pressing ENTER')
    parser.add_argument('-s', '--save', metavar='filename', help='after execution save field to file')
    parser.add_argument('-f', '--field', metavar='filename', required=True, help='path to file with field')
    return parser.parse_args()


def load_field(filename, serializer):
    with open(filename, 'r') as file:
        data = file.read()
    return serializer.unserialize(data)


def save_field(field, filename, serializer):
    data = serializer.serialize(field)
    with open(filename, 'w') as file:
        file.write(data)


def main():
    args = parse_args()
    serializer = FieldSerializer()
    field = load_field(args.field, serializer)
    game = Game(field)
    ui = UI(game, serializer)
    ui.run(args.tick_time, args.confirm)
    if args.save:
        save_field(game.field, args.save, serializer)
        print('Field saved.')


if __name__ == '__main__':
    main()
