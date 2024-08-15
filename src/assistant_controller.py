"""
assistant controller
"""

from difflib import get_close_matches
from prompt_toolkit.completion import Completer, Completion
from src.models.address_book import AddressBook
from src.book_controller import (
    add_contact,
    remove_contact,
    remove_phone,
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
    add_email,
    add_address,
)

COMMANDS = {
    "add": add_contact,
    "remove-contact": remove_contact,
    "remove-phone": remove_phone,
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
    "exit": "",
    "close": "",
    "hello": "",
    "add-email": add_email,
    "add-address": add_address,
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


class CommandCompleter(Completer):
    """
    Command completer for providing dynamic suggestions based on input.

    This class is designed to work with `prompt_toolkit` to offer command
    suggestions as the user types. It suggests the closest matching commands
    based on the text entered before the cursor.

    Methods
    -------
    get_completions(document, complete_event)
        Generates command completions based on the current input.

    Parameters
    ----------
    document : Document
        The `prompt_toolkit` document object representing the current state
        of the text input, including the text before the cursor.

    complete_event : CompleteEvent
        The `prompt_toolkit` event object representing the current state of the
        completion event, which includes flags and settings about the
        completion process.

    Yields
    ------
    Completion
        A `Completion` object for each matching command, providing the
        completion text and the position where it should be inserted.

    """

    def get_completions(self, document, complete_event):
        # Split input to get the command part only
        text_before_cursor = document.text_before_cursor
        words = text_before_cursor.strip().split()

        # Only suggest completions for the first word (command)
        if len(words) == 1 and " " not in text_before_cursor:
            matches = get_close_matches(
                words[0].lower(), COMMANDS.keys(), n=5, cutoff=0.1
            )
            for match in matches:
                yield Completion(match, start_position=-len(words[0]))


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
            suggested_command = suggest_command(command, list(COMMANDS.keys()))
            if suggested_command:
                return f"Invalid command. Did you mean '{suggested_command}'?"

            return "Invalid command."
