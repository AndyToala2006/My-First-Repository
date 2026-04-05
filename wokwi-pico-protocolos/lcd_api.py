import time

# Minimal LCD API for HD44780-compatible displays

class LcdApi:
    LCD_CLR = 0x01
    LCD_HOME = 0x02
    LCD_ENTRY_MODE = 0x04
    LCD_ENTRY_INC = 0x02
    LCD_ENTRY_SHIFT = 0x01
    LCD_ON_CTRL = 0x08
    LCD_ON_DISPLAY = 0x04
    LCD_ON_CURSOR = 0x02
    LCD_ON_BLINK = 0x01
    LCD_MOVE = 0x10
    LCD_MOVE_DISP = 0x08
    LCD_MOVE_RIGHT = 0x04
    LCD_FUNCTION = 0x20
    LCD_FUNCTION_8BIT = 0x10
    LCD_FUNCTION_2LINES = 0x08
    LCD_FUNCTION_10DOTS = 0x04
    LCD_CGRAM = 0x40
    LCD_DDRAM = 0x80

    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0
        self._init_lcd()

    def _init_lcd(self):
        raise NotImplementedError

    def _write_cmd(self, cmd):
        raise NotImplementedError

    def _write_data(self, data):
        raise NotImplementedError

    def clear(self):
        self._write_cmd(self.LCD_CLR)
        time.sleep_ms(2)
        self.move_to(0, 0)

    def home(self):
        self._write_cmd(self.LCD_HOME)
        time.sleep_ms(2)
        self.move_to(0, 0)

    def move_to(self, col, row):
        if row > self.num_lines:
            row = self.num_lines - 1
        if col > self.num_columns:
            col = self.num_columns - 1
        self.cursor_x = col
        self.cursor_y = row
        addr = col + (0x40 * row)
        self._write_cmd(self.LCD_DDRAM | addr)

    def putchar(self, char):
        self._write_data(ord(char))
        self.cursor_x += 1
        if self.cursor_x >= self.num_columns:
            self.cursor_x = 0
            self.cursor_y += 1
            if self.cursor_y >= self.num_lines:
                self.cursor_y = 0
            self.move_to(self.cursor_x, self.cursor_y)

    def putstr(self, string):
        for char in string:
            self.putchar(char)
