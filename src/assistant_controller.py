"""
assistant controller
"""

from src.book_controller import (
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
)


def execute_command(command, args, book):
    """
    Execute the given command with the provided arguments and address book.
    
    Args:
        command (str): The command to execute.
        args (list): The arguments for the command.
        book (dict): The address book data.
        
    Returns:
        str: The result of the command execution.
    """
    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
    }
    match command:
        case "hello":
            return "How can I help you?"

        case command if command in commands:
            return commands[command](args, book)
        
        case _:
            return "Invalid command."
