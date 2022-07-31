import curses
from logging import ERROR
import re

from exceptions import QuitException


class IO:
    VALID_EMAIL = r"[^@]+@[^@]+\.[^@]+"
    VALID_PHONE = r"^\d{3}-\d{3}-\d{4}$"
    ANY = r".*"

    STYLE_DEFAULT = 1
    STYLE_HIGHLIGHT = 2
    STYLE_ERROR = 3

    def __init__(self):
        self.text = ''
        self.options: list[str] = []
        self.selection = ''

    def __render_options(self, stdscr: any, selected_row_idx: int) -> None:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        for idx, row in enumerate(self.options):
            x = w // 2 - len(row) // 2
            y = h // 2 + idx

            if idx == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        stdscr.refresh()

    def __handle_option_selection(self, stdscr: any) -> None:
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        current_row_idx = 0

        self.__render_options(stdscr, current_row_idx)

        while True:
            key = stdscr.getch()
            stdscr.clear()

            if key == curses.KEY_UP and current_row_idx > 0:
                current_row_idx -= 1
            elif key == curses.KEY_DOWN and current_row_idx < len(self.options) - 1:
                current_row_idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.selection = self.options[current_row_idx]
                break

            self.__render_options(stdscr, current_row_idx)

    def __render_center_print(self, stdscr: any, style:int) -> None:
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        curses.curs_set(0)
        h, w = stdscr.getmaxyx()

        x = w // 2 - len(self.text) // 2
        y = h // 2

        stdscr.clear()
        stdscr.attron(curses.color_pair(style))
        stdscr.addstr(y, x, self.text)
        stdscr.attroff(curses.color_pair(style))

        stdscr.refresh()
        stdscr.getch()

    def __capture_raw_input(self, stdscr: any, r: int, c: int, prompt_string: str) -> str:
        stdscr.clear()
        curses.echo()
        stdscr.addstr(r, c, prompt_string)
        stdscr.refresh()

        input = str(stdscr.getstr(r + 1, c, 40))[2:-1]

        if input.lower() == 'q' or input.lower() == 'quit':
            raise QuitException()

        return input

    def __is_valid_input(self, input_string: str, regex: str) -> bool:
        return re.match(regex, input_string) is not None

    def input(self, prompt_string:str, regex: str=ANY) -> str:
        input = curses.wrapper(self.__capture_raw_input, 0, 0, prompt_string)

        while not self.__is_valid_input(input, regex):
            self.print("Invalid input. Please try again.", self.STYLE_ERROR)
            input = curses.wrapper(self.__capture_raw_input, 0, 0, prompt_string)

        return input

    def print(self, text: str, style:int=STYLE_DEFAULT) -> None:
        self.text = text
        curses.wrapper(self.__render_center_print, style)

    def print_options(self, options: list[str]) -> str:
        self.options = options
        curses.wrapper(self.__handle_option_selection)

        return self.selection
