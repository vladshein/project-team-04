"""
Project team 04
"""

import os
from prompt_toolkit import PromptSession
from src.assistant_controller import execute_command, CommandCompleter
from src.book_controller import parse_input, save_data, load_data, clear_screen


def main():
    """
    Main function to run the assistant bot.
    """
    home_dir = os.path.expanduser("~")
    path = os.path.join(home_dir, "Documents", "addressbook.pkl")
    # Set up a Completer for dynamic suggestions
    command_completer = CommandCompleter()
    session = PromptSession(completer=command_completer)
    book = load_data(path)
    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = session.prompt("Enter a command: ")
            command, args = parse_input(user_input)
        except (KeyboardInterrupt, ValueError):
            continue  # Control-C pressed. Try again.
        except EOFError:
            save_data(book, path)
            break  # Control-D pressed. Exit the loop.
        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book, path)
            break
        if command in ["cls", "clear"]:
            clear_screen()
            continue
        result = execute_command(command, args, book)
        print(result)


if __name__ == "__main__":
    main()
