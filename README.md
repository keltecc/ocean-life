# Ocean Life

## Description

It's like [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), but using more types of cells.

Tested on **Python 3.6.5**.

## Usage

```
usage: main.py [-h] [-t milliseconds | -c] [-s filename] -f filename

optional arguments:
  -h, --help            show this help message and exit
  -t milliseconds, --tick-time milliseconds
                        tick time
  -c, --confirm         confirm each step by pressing ENTER
  -s filename, --save filename
                        after execution save field to file
  -f filename, --field filename
                        path to file with field
```

## Run tests

```sh
python3 tests.py
```


## Examples

Just "print" hello world:

```sh
python3 main.py -f examples/hello_world
```


Run glider with 1 second tick:

```sh
python3 main.py -f examples/glider -t 1000
```


Run glider and ask for confirmation at every tick:

```sh
python3 main.py -f examples/glider -c
```


Launch two gliders and save updated field to "two_gliders_new":

```sh
python3 main.py -f examples/two_gliders -s two_gliders_new
```


## Interface

```
Press Ctrl+C to stop:
" " - Empty
"R" - Rock
"F" - Fish
"S" - Shrimp
┌──────────────────────────────────────────────────┐
│                                                  │
│                                                  │
│                                                  │
│    F                                             │
│     F                                            │
│   FFF                                            │
│                                                  │
│                                                  │
│                                                  │
│                                                  │
│                                                  │
│                                                  │
│                                                  │
│                                                  │
│                                                  │
│                                                  │
│                                                  │
│                                                  │
│                                                  │
│                                                  │
└──────────────────────────────────────────────────┘
Press ENTER to continue:
```


## Features

- You can skip trailing spaces when creating a field. Parser would be automatically complete them.
