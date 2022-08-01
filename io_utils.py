import curses
import re

from exceptions import QuitException


class IO:
    VALID_EMAIL = r"[^@]+@[^@]+\.[^@]+"
    VALID_PHONE = r"^\d{3}-\d{3}-\d{4}$"
    VALID_PRICE = r"^\d{1,3}(,\d{3})*(\.\d{2})?$"
    VALID_URL = r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
    ANY = r".*"

    COLOR_DEFAULT = 1
    COLOR_WARNING = 2
    COLOR_ERROR = 3
    COLOR_SUCCESS = 4
    COLOR_REVERSE = 5

    def __init__(self):
        self.text = ''
        self.selection = ''

    def __init_color_scheme(self) -> None:
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def __render_options(self, stdscr: any, selected_row_idx: int, options: list[str], style: int = COLOR_REVERSE) -> None:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        for idx, row in enumerate(options):
            x = max(w // 2 - len(row) // 2, 0)
            y = h // 2 + idx

            if idx == selected_row_idx:
                stdscr.attron(curses.color_pair(style))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(style))
            else:
                stdscr.addstr(y, x, row)

        stdscr.refresh()

    def __handle_option_selection(self, stdscr: any, options: list[str], header: str) -> None:
        self.__init_color_scheme()
        first_row_idx = current_row_idx = 1 if header else 0
        if header:
            options = [header] + options

        self.__render_options(stdscr, current_row_idx, options)

        while True:
            key = stdscr.getch()
            stdscr.clear()

            if key == curses.KEY_UP and current_row_idx > first_row_idx:
                current_row_idx -= 1
            elif key == curses.KEY_DOWN and current_row_idx < len(options) - 1:
                current_row_idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.selection = options[current_row_idx]
                break

            self.__render_options(stdscr, current_row_idx, options)

    def __render_center_print(self, stdscr: any, style: int) -> None:
        self.__init_color_scheme()
        stdscr.clear()

        h, w = stdscr.getmaxyx()

        split_text = self.text.split('\n')

        for idx, row in enumerate(split_text):
            x = max(w // 2 - len(row) // 2, 0)
            y = h // 2 + idx

            stdscr.attron(curses.color_pair(style))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(style))

        stdscr.refresh()
        stdscr.getch()

    def __capture_raw_input(self, stdscr: any, prompt_string: str) -> str:
        stdscr.clear()
        curses.echo()

        h, w = stdscr.getmaxyx()

        x = max(w // 2 - len(prompt_string) // 2, 0)
        y = h // 2

        stdscr.addstr(y, x, prompt_string)
        stdscr.refresh()

        input = str(stdscr.getstr(y + 1, x, 500))[2:-1]

        if input.lower().strip() == 'q' or input.lower().strip() == 'quit':
            raise QuitException()

        return input

    def __is_valid_input(self, input_string: str, regex: str) -> bool:
        return re.match(regex, input_string) is not None

    def input(self, prompt_string: str, regex: str = ANY) -> str:
        input = curses.wrapper(self.__capture_raw_input, prompt_string)

        while not self.__is_valid_input(input, regex):
            self.print("Invalid input. Please try again.", self.COLOR_ERROR)
            input = curses.wrapper(
                self.__capture_raw_input, prompt_string)

        return input

    def print(self, text: str, style: int = COLOR_DEFAULT) -> None:
        self.text = text
        curses.wrapper(self.__render_center_print, style)

    def print_options(self, options: list[str], header: str = None) -> str:
        curses.wrapper(self.__handle_option_selection, options, header)

        return self.selection
