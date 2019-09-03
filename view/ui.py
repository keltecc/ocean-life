#!/usr/bin/env python3

import os

from time import sleep


class UI(object):
    def __init__(self, game, serializer):
        self._game = game
        self._serializer = serializer

    def run(self, tick_time, need_confirmation):
        while True:
            try:
                text = self._serializer.serialize(self._game.field)
                self._clear_screen()
                print('Press Ctrl+C to stop:')
                print(text)
                if need_confirmation:
                    input('Press ENTER to continue:\n')
                else:
                    sleep(tick_time / 1000)
                self._game.tick()
            except KeyboardInterrupt:
                break
        print('Stopped.')

    def _clear_screen(self):
        # print('\n' * 100)
        if os.name == 'nt':
            cmd = 'cls'
        else:
            cmd = 'clear'
        os.system(cmd)
