import sys
from . import tokens

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
