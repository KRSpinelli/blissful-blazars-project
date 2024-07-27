class UnsupportedEmoji(Exception):
    """Raised when any color entry argument of a method within EmojiGrid is not of permitted type."""
    pass


class InvalidCoordinates(Exception):
    """Raised when update fails at a location due to incorrect coordinates."""
    pass


class EmojiGrid:
    RED = "🟥"
    ORANGE = "🟧"
    YELLOW = "🟨"
    GREEN = "🟩"
    BLUE = "🟦"
    PURPLE = "🟪"
    BROWN = "🟫"
    BLACK = "⬛"
    WHITE = "⬜"
    PERMITTED_EMOJIS = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪", "🟫", "⬛", "⬜"]

    def __init__(self, rows: int = 10, cols: int = 10, fill_emoji: "EmojiGrid" = BLACK, show_rows: bool = False):
        self.show_rows_on_output: bool = show_rows
        self.rows = rows
        self.cols = cols
        self.grid = [[f"{fill_emoji}" for _ in range(cols)] for _ in range(rows)]

    def get(self, row: int, col: int) -> str:
        return self.grid[row][col]

    def update(self, row: int, col: int, color: str):
        """Updates the color at the requested position.
        :raises UnsupportedEmoji: if color is not in PERMITTED_EMOJIS.
        :raises InvalidCoordinates: if self.grid[row][col] is out of bounds.
        :arg color: String of the desired Emoji color.
        """
        if color not in self.PERMITTED_EMOJIS:
            raise UnsupportedEmoji(f"Color Entry of \"{color}\" is not supported. "
                                   f"Must be one of the permitted colors within EmojiGrid (Example: EmojiGrid.RED)")
        else:
            try:
                self.grid[row][col] = color
            except (IndexError, LookupError) as e:
                raise InvalidCoordinates(str(e) + f". Ensure you are indexing from neg(max-1) to 0 OR 0 to pos(max-1). "
                                         f"The maximum indexes in both pos/neg for row lookups is +/-{self.rows-1} and +/-{self.cols-1} for col.")

    def get_grid(self):
        return self.grid
    def __str__(self):
        output_str = ""
        for row, row_content in enumerate(self.grid):
            output_str += (f"ROW {str(row+1).zfill(2)} " if self.show_rows_on_output else "") + "".join(row_content) + "\n"
        return output_str
