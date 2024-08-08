"""
Homework 08
"""

from src.assistant_controller import execute_command
from src.book_controller import parse_input, save_data, load_data


def main():
    """
    Main function to run the assistant bot.
    """

    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break

        result = execute_command(command, args, book)
        print(result)


if __name__ == "__main__":
    main()
