"""
assistant controller
"""

from difflib import get_close_matches
from src.models.address_book import AddressBook
from src.book_controller import (
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
    add_note_to_contact,
    edit_note_in_contact,
    remove_note_from_contact,
    show_notes_for_contact,
    find_notes_by_keyword,
)

COMMANDS = {
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": show_all,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
    "add-note": add_note_to_contact,
    "edit-note": edit_note_in_contact,
    "remove-note": remove_note_from_contact,
    "show-notes": show_notes_for_contact,
    "find-notes": find_notes_by_keyword,
}


def suggest_command(command, available_commands):
    """
    Suggest the closest matching command based on user input.

    Args:
        command (str): The command to match.
        available_commands (list): List of available command strings.

    Returns:
        str: The closest matching command.
    """
    matches = get_close_matches(command, available_commands, n=1, cutoff=0.6)
    return matches[0] if matches else None


def execute_command(command: str, args: list, book: AddressBook) -> str:
    """
    Execute the given command with the provided arguments and address book.

    Args:
        command (str): The command to execute.
        args (list): The arguments for the command.
        book (AddressBook): The address book data.

    Returns:
        str: The result of the command execution.
    """

    match command:
        case "hello":
            return "How can I help you?"

        case command if command in COMMANDS:
            return COMMANDS[command](args, book)

        case _:
            suggested_command = suggest_command(
                command, list(COMMANDS.keys()) + ["hello", "close", "exit"]
            )
            if suggested_command:
                return f"Invalid command. Did you mean '{suggested_command}'?"
            else:
                return "Invalid command."
