class Stats:
    def __init__(self):
        self.total = 0
        self.min = None
        self.max = None
        self.count = 0

    def add_number(self, number: int) -> None:
        self.total += number
        self.count += 1

        if self.min is None:
            self.min = number
            self.max = number
            return

        if number < self.min:
            self.min = number
        if number > self.max:
            self.max = number

    def print_stats(self) -> None:
        print(f"Count: {self.count}")
        print(f"Total: {self.total}")
        print(f"Min: {self.min}")
        print(f"Max: {self.max}")


def parse_valid_number(text: str) -> int | None:
    try:
        number = int(text)
    except ValueError:
        return None

    if -100 <= number <= 100:
        return number
    return None
