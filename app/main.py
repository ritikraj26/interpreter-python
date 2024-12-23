import sys
from . import tokens
import enum
from typing import Any


class TokenType(enum.Enum):
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    STAR = "STAR"
    DOT = "DOT"
    COMMA = "COMMA"
    PLUS = "PLUS"
    MINUS = "MINUS"
    SEMICOLON = "SEMICOLON"
    SLASH = "SLASH"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    STRING = "STRING"
    NUMBER = "NUMBER"
    EOF = "EOF"

class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: Any | None, line: int) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"

class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.errors: list[str] = []
    def scan_tokens(self) -> tuple[list[Token], list[str]]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens, self.errors

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        char = self.advance()
        match char:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case "*":
                self.add_token(TokenType.STAR)
            case ".":
                self.add_token(TokenType.DOT)
            case ",":
                self.add_token(TokenType.COMMA)
            case "+":
                self.add_token(TokenType.PLUS)
            case "-":
                self.add_token(TokenType.MINUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "!":
                self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
            case "=":
                self.add_token(TokenType.EQUAL_EQUAL) if self.match("=") else self.add_token(TokenType.EQUAL)
            case "<":
                self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
            case ">":
                self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case " ", "\r", "\t":
                pass
            case "\n":
                self.line += 1
            case "\"":
                self.string()
            case _:
                self.error(f"Unexpected character: {char}")

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type: TokenType, literal: Any | None = None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def string(self) -> None:
        while self.peek() != "\"" and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.errors.append(f"[line {self.line}] Error: Unterminated string.")
            return

        self.advance()

        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def error(self, message: str) -> None:
        self.errors.append(f"[line {self.line}] Error: {message}")




def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Program logs appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    error = False

    if file_contents:
        file_length = len(file_contents)
        i = 0
        while i < file_length:
            c = file_contents[i]
            if c == " " or c == "\t" or c == "\n":
                i += 1
                continue
            cc = file_contents[i:i+2] if i + 1 < file_length else None
            # check for comment
            if cc == "//":
                i += 2
                while i < file_length and file_contents[i] != "\n":
                    i += 1
                continue
            if c == "\"":
                i += 1
                value = ""
                while i < file_length and file_contents[i] != "\"":
                    value += file_contents[i]
                    i += 1
                if i == file_length:
                    error = True
                    line_number = file_contents.count("\n", 0, i) + 1
                    print(
                        f"[line {line_number}] Error: Unterminated string.",
                        file = sys.stderr
                    )
                else:
                    print(f"""STRING "{value}" {value}""")
                    i += 1
                continue
            if cc and cc in tokens.TOKEN_MAP:
                print(f"{tokens.TOKEN_MAP[cc]} {cc} null")
                i += 2
                continue
            if c in tokens.TOKEN_MAP:
                print(f"{tokens.TOKEN_MAP[c]} {c} null")
                i += 1
            else:
                error = True
                line_number = file_contents.count("\n", 0, i) + 1
                print(
                    f"[line {line_number}] Error: Unexpected character: {c}",
                    file = sys.stderr
                )
                i += 1

    print("EOF  null")
    if error:
        exit(65)
    else:
        exit(0)


if __name__ == "__main__":
    main()
