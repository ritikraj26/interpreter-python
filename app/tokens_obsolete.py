TOKEN_MAP = {
    "(": "LEFT_PAREN",
    ")": "RIGHT_PAREN",
    "{": "LEFT_BRACE",
    "}": "RIGHT_BRACE",
    "*": "STAR",
    ".": "DOT",
    ",": "COMMA",
    "+": "PLUS",
    "-": "MINUS",
    ";": "SEMICOLON",
    "/": "SLASH",
    "=": "EQUAL",
    "==": "EQUAL_EQUAL",
    "!": "BANG",
    "!=": "BANG_EQUAL",
    "<": "LESS",
    "<=": "LESS_EQUAL",
    ">": "GREATER",
    ">=": "GREATER_EQUAL",
    "/": "SLASH",
    "//": "COMMENT",
}

def get_token_type(token):
    return TOKEN_MAP.get(token, None)