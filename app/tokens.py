TOKEN_MAP = {
    "(": "LEFT_PAREN",
    ")": "RIGHT_PAREN",
    "{": "LEFT_BRACE",
    "}": "RIGHT_BRACE",
}

def get_token_type(token):
    return TOKEN_MAP.get(token, None)