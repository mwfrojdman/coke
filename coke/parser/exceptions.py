class ParseError(Exception):
    def __init__(self, line: int, column: int, message: str):
        self.line = line
        self.column = column
        self.message = message

    def __str__(self):
        return 'Parse error on line {} column {}: {}'.format(self.line, self.column, self.message)
