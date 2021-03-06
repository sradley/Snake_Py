"""
snake/snake_game_obj.py

author:         Stephen Radley
date:           2018/07/05
package:        snake
version:        0.0.1
"""

import curses, sys, time

from snake.functions import is_allowed_key, is_opposite_key
from snake.snake_obj import Snake
from snake.food_obj import Food

VERSION = "0.0.1"


"""
SnakeGame ...
"""
class SnakeGame:
    SCORE = 0
    COLOR_WHITE = 1
    COLOR_RED = 2
    GAME_SPEED = 0.075
    SNAKE_START_LEN = 1

    """
    __init__ ...
    """
    def __init__(self):
        self.score = self.SCORE

        # create screen
        self.scr = curses.initscr()

        # cursor and color config
        curses.curs_set(False)
        curses.noecho()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(self.COLOR_WHITE, curses.COLOR_WHITE,
            curses.COLOR_WHITE)
        curses.init_pair(self.COLOR_RED, curses.COLOR_RED, curses.COLOR_RED)

        # get screen dimensions
        max_y, max_x = self.scr.getmaxyx()
        self.dim_x = max_x - 2
        self.dim_y = max_y - 2

        # add info
        self.scr.addstr(0, 1, 'snake-py ' + VERSION)
        quitInstructions = 'press ctrl-C to quit'
        scoreMeter = 'score %d ' % self.score
        if max_x - 2 < len(quitInstructions + scoreMeter):
            self.scr.addstr(self.dim_y + 1, 1, scoreMeter)
        else:
            self.scr.addstr(self.dim_y + 1, 1, scoreMeter +
                ' ' * (self.dim_x - len(scoreMeter) - len(quitInstructions)) +
                quitInstructions)

        # create window
        self.win = curses.newwin(self.dim_y, self.dim_x, 1, 1)
        self.win.keypad(True)
        self.win.box()
        self.win.timeout(int(self.GAME_SPEED * 1000))

        self.refresh()

    """
    run ...
    """
    def run(self):
        # create snake
        snake = Snake(self.dim_x, self.dim_y, self.SNAKE_START_LEN)
        self.render_snake(snake)

        # create a food
        food = Food(self.dim_x, self.dim_y, snake)
        self.render_food(food)

        # set current direction
        curr_key = curses.KEY_RIGHT

        while True:
            old_snake = snake.copy()
            if not snake.move_in_direction(curr_key):
                self.quit_game()

            if food.loc.collided(snake.locs[0]):
                snake.eat()
                self.score += 1
                food = Food(self.dim_x, self.dim_y, snake)

            self.render_snake(snake, old_snake)
            self.render_food(food)

            t = time.time()
            key = self.win.getch()
            if time.time() - t < self.GAME_SPEED:
                time.sleep(self.GAME_SPEED - (time.time() - t))
            if key != -1:
                if (is_allowed_key(key) and
                        not is_opposite_key(curr_key, key)):
                    curr_key = key

            self.refresh()

    """
    render_snake ...
    """
    def render_snake(self, snake, old_snake=None):
        # remove old snake tail
        if old_snake is not None:
            self.win.delch(old_snake.locs[-1].y, old_snake.locs[-1].x)
            self.win.insch(old_snake.locs[-1].y, old_snake.locs[-1].x, ' ')

        # render new snake head
        self.win.addch(snake.locs[0].y, snake.locs[0].x, curses.ACS_BOARD,
            curses.color_pair(self.COLOR_WHITE))

    """
    render_food
    """
    def render_food(self, food):
        self.win.addch(food.loc.y, food.loc.x, curses.ACS_BOARD,
            curses.color_pair(self.COLOR_RED))

    """
    refresh ...
    """
    def refresh(self):
        # update score
        self.scr.addstr(self.dim_y + 1, 1, 'score: %d' % self.score)

        # refresh windows
        self.scr.refresh()
        self.win.refresh()

    """
    quit ...
    """
    def quit_game(self):
        curses.endwin()
        sys.exit()
