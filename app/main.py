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
        for c in file_contents:
            token_type = tokens.get_token_type(c)
            if token_type:
                print(f"{token_type} {c} null")
            else:
                error = True
                line_number = file_contents.count("\n", 0, file_contents.index(c)) + 1
                # print(
                #     "[line %s] Error: Unexpected character: %s" %(line_number, c),
                #     file = sys.stderr
                # )
                print(
                    f"[line {line_number}] Error: Unexpected character: {c}",
                    file = sys.stderr
                )
    print("EOF  null")
    if error:
        exit(65)
    else:
        exit(0)


if __name__ == "__main__":
    main()
