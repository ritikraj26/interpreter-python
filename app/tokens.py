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
}

def get_token_type(token):
    return TOKEN_MAP.get(token, None)