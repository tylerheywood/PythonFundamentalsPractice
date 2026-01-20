from stats import Stats, parse_valid_number

def main() -> None:
    stats = Stats()

    user_input = input("Enter a number: ")
    while user_input != "q":
        number = parse_valid_number(user_input)

        if number is None:
            print("Invalid input")
        else:
            stats.add_number(number)

        user_input = input("Enter a number: ")

    stats.print_stats()

if __name__ == "__main__":
    main()
