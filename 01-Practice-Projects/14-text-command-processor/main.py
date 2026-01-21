"""
🎯 Goal
Build a simple command-driven program that processes text commands
and maintains internal state.

The program should behave like a tiny CLI tool that accepts commands,
updates a running total, and responds appropriately.

📥 Inputs
The user repeatedly enters commands as text.

Supported commands:
- add <number>     → adds the number to the total
- remove <number>  → subtracts the number from the total
- clear            → resets the total to 0
- total            → prints the current total
- quit             → exits the program

Rules:
- <number> must be a valid integer
- Commands are case-sensitive
- Any invalid command or malformed input should be rejected

📤 Outputs
- The `total` command prints:
  Total: <current total>

- Invalid commands print:
  Invalid command

- The program runs until `quit` is entered

⚠️ Constraints
- No lists or dictionaries to store command history
- No use of eval
- No external libraries
- Use a while loop for input handling
- Use string parsing (e.g. split)
- Prioritise clarity over cleverness
"""
total = 0


def string_parser(user_input: str) -> list[object]:
    split_input = user_input.split()
    if len(split_input) == 2:
        try:
            split_input[1] = int(split_input[1])
            return split_input
        except ValueError:
            return split_input
    else:
        return split_input

def valid_command_parser(split_input: list):

    if len(split_input) == 2 and split_input[0] in ("add", "remove"):
        if type(split_input[1]) == int: # could have used 'if isInstance(split_input[1],int)' <- returns true or false
            return True
        else:
            return False
    elif len(split_input) == 1 and split_input[0] in ("clear", "total"):
        return True
    else:
        return False

def add_to_total(total, parsed) -> int:
    total += parsed[1]
    return total

def remove_from_total(total, parsed) -> int:
    total -= parsed[1]
    return total

user_input = input("Please enter a command: ")

while user_input != 'quit':

    parsed = string_parser(user_input)

    if valid_command_parser(parsed):
        if parsed[0] == "add":
            total = add_to_total(total, parsed)
        elif parsed[0] == "remove":
            total = remove_from_total(total, parsed)
        elif parsed[0] == "clear":
            total = 0
        elif parsed[0] == "total":
            print(f"Total: {total}")
    else:
        print("Invalid command")

    user_input = input("Please enter a command: ")

