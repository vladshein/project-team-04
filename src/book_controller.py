"""
book controller
"""

import pickle
import os
from typing import Callable, List, Tuple
from tabulate import tabulate

from src.models.address_book import AddressBook, Record
from src.models.fields import (
    PhoneNumberValueError,
    BirthdayValueError,
    NameValueError,
    EmailValueError,
    AddressValueError,
    NoteValueError,
)


def input_error(func: Callable) -> Callable:
    """
    Decorator to handle common input errors for bot commands.

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: The wrapped function with error handling.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (
            PhoneNumberValueError,
            BirthdayValueError,
            NameValueError,
            EmailValueError,
            AddressValueError,
            NoteValueError,
        ) as e:
            return e
        except ValueError as e:
            return e
        except KeyError:
            return "Contact not found or no contact information."

    return inner


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    """
    Parse user input into a command and its arguments.

    Args:
        user_input (str): The raw input from the user.

    Returns:
        Tuple[str, List[str]]: The command and list of arguments.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


def clear_screen():
    """
    Clear screen
    """
    # For Windows
    if os.name == "nt":
        os.system("cls")
    # For macOS and Linux
    else:
        os.system("clear")


@input_error
def add_contact(args: List[str], book: AddressBook) -> str:
    """
    Add a new contact or update an existing one with a phone number.

    Args:
        args (List[str]): List containing the name and phone number.
        book (AddressBook): The address book instance.

    Returns:
        str: Success message indicating contact addition or update.
    """
    try:
        name, phone, *_ = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'add [name] [phone_number]'"
        ) from e
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        if record.find_phone(phone):
            return "This phone number already exists."
        try:
            record.add_phone(phone)
        except PhoneNumberValueError:
            if message == "Contact updated.":
                message = "The contact was not updated because you\
                            entered an incorrect phone number."
            else:
                message = "Contact added without a phone number because\
                             you entered an incorrect phone number."
    return message


@input_error
def remove_contact(args: List[str], book: AddressBook) -> str:
    """
    Delete contact.

    Args:
        args (List[str]): List containing the name and phone number.
        book (AddressBook): The address book instance.

    Returns:
        str: Success message indicating contact deleted.
    """
    try:
        name, *_ = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'remove-contact [name]'"
        ) from e
    record = book.find(name)
    if not record:
        raise KeyError
    answer = input("Are you sure you want to delete a contact ? y/n \n")
    if answer.lower() == "y":
        book.delete(name)
        return f"Contact {name} deleted"
    return f"Contact {name} not deleted"


@input_error
def remove_phone(args: List[str], book: AddressBook) -> str:
    """Remove the phone number of existing contact.
        Args:
        args (List[str]): List containing the name, old phone number, and new phone number.
        book (AddressBook): The address book instance.

    Returns:
        str: Success or error message.
    """
    try:
        name, phone, *_ = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'remove-phone [name] [phone]'"
        ) from e
    record = book.find(name)
    if not record:
        raise KeyError
    record.remove_phone(phone)
    return "Phone number deleted"


@input_error
def change_contact(args: List[str], book: AddressBook) -> str:
    """
    Change the phone number of an existing contact.

    Args:
        args (List[str]): List containing the name, old phone number, and new phone number.
        book (AddressBook): The address book instance.

    Returns:
        str: Success or error message.
    """
    try:
        name, old_phone, new_phone, *_ = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'change [name] [old_number] [new_number]'"
        ) from e
    record = book.find(name)
    if not record:
        raise KeyError
    if record.find_phone(new_phone):
        return f"This phone number: {new_phone} already exists."
    record.edit_phone(old_phone, new_phone)
    return f"Contact {name} updated."


@input_error
def show_phone(args: List[str], book: AddressBook) -> str:
    """
    Show the phone number of a contact.

    Args:
        args (List[str]): List containing the name.
        book (AddressBook): The address book instance.

    Returns:
        str: The phone number or an error message.
    """
    try:
        name, *_ = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'phone [name] [old_number] [new_number]'"
        ) from e
    record = book.find(name)
    if not record:
        raise KeyError
    return str(record)


@input_error
def show_all(_: List[str], book: AddressBook) -> str:
    """
    Show all contacts.

    Args:
        book (AddressBook): The address book instance.

    Returns:
        str: All contacts formatted as a string, or an error message if empty.
    """
    if not book.data:
        return "Sorry, your phone book is empty."

    header_list = ["Name", "Phones", "Birthday", "E-mail", "Address"]

    record_list = []
    for _, phone in book.data.items():
        record = []
        record.append(phone.name.value.capitalize())
        record.append("; ".join(p.value for p in phone.phones))
        record.append(phone.birthday.value if phone.birthday else "")
        record.append(phone.email.value if phone.email else "")
        record.append(phone.address.value if phone.address else "")
        record_list.append(record)

    print(tabulate(record_list, header_list, tablefmt="fancy_grid"))
    return "End of contacts list"


@input_error
def add_birthday(args: List[str], book: AddressBook) -> str:
    """
        Add a birthday to an existing contact.
    args
        Args:
            args (List[str]): List containing the name and birthday.
            book (AddressBook): The address book instance.

        Returns:
            str: Success message indicating birthday addition.
    """
    try:
        name, birthday, *_ = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'add_birthday [name] [DD.MM.YYYY]'"
        ) from e
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_birthday(birthday)
    return "Contact birthday added"


@input_error
def show_birthday(args: List[str], book: AddressBook) -> str:
    """
    Show the birthday of a contact.

    Args:
        args (List[str]): List containing the name.
        book (AddressBook): The address book instance.

    Returns:
        str: The birthday or an error message.
    """
    try:
        name, *_ = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'show_birthday [name]'"
        ) from e
    record = book.find(name)
    if not record or not record.birthday:
        raise KeyError
    return str(record.birthday)


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    """
    Show upcoming birthdays.

    Args:
        book (AddressBook): The address book instance.

    Returns:
        str: List of upcoming birthdays or a message indicating none.
    """
    if args:
        days = int(args[0])
        upcoming_birthdays = book.get_upcoming_birthdays(days)
    else:
        upcoming_birthdays = book.get_upcoming_birthdays()
    upcoming = ""
    if upcoming_birthdays:
        for birthday in upcoming_birthdays:
            upcoming += f"Name : {birthday['name']:<10} - congratulation_date: \
            {birthday['congratulation_date']}\n"
        return upcoming.strip()
    return "No upcoming birthdays"


def save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
    """
    Save the address book to a file.
    """
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = "addressbook.pkl"):
    """
    Load the address book from a file.
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


@input_error
def add_note_to_contact(args: List[str], book: AddressBook) -> str:
    """
    Add a note to an existing contact.

    Args:
        args (List[str]): List containing the contact name, note name, and note content.
        book (AddressBook): The address book instance.

    Returns:
        str: Success message indicating note addition.
    """
    if len(args) < 3:
        raise ValueError(
            "Incorrect input command argument. Use: 'add-note [name] [note_name] [note_content]'"
        )

    try:
        contact_name = args[0]
        note_name = args[1]
        note_content = " ".join(
            args[2:]
        )  # Join the rest of the arguments as the note content
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'add-note [name] [note_name] [note_content]'"
        ) from e

    record = book.find(contact_name)
    if not record:
        raise KeyError(f"Contact with name '{contact_name}' not found.")

    record.add_note(note_content, note_name)
    return "Note added."


@input_error
def edit_note_in_contact(args: List[str], book: AddressBook) -> str:
    """
    Edit a note in an existing contact.

    Args:
        args (List[str]): List containing the contact name, note name to edit, and new note content.
        book (AddressBook): The address book instance.

    Returns:
        str: Success message indicating note update.
    """
    if len(args) < 3:
        raise ValueError(
            "Incorrect input command argument. Use: 'edit-note [name][note_name][new_note_content]'"
        )

    try:
        contact_name = args[0]
        note_name = args[1]
        new_note_content = " ".join(
            args[2:]
        )  # Join the rest of the arguments as the note content
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'edit-note [name][note_name][new_note_content]'"
        ) from e

    record = book.find(contact_name)
    if not record:
        raise KeyError(f"Contact with name '{contact_name}' not found.")

    record.edit_note(note_name, new_note_content)
    return "Note updated."


@input_error
def remove_note_from_contact(args: List[str], book: AddressBook) -> str:
    """
    Remove a note from an existing contact by note name.

    Args:
        args (List[str]): List containing the contact name and note name.
        book (AddressBook): The address book instance.

    Returns:
        str: Success message indicating note removal.
    """
    if len(args) < 2:
        raise ValueError(
            "Incorrect input command argument. Use: 'remove-note [name] [note_name]'"
        )

    try:
        contact_name = args[0]
        note_name = args[1]
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'remove-note [name] [note_name]'"
        ) from e

    record = book.find(contact_name)
    if not record:
        raise KeyError(f"Contact with name '{contact_name}' not found.")

    record.remove_note_by_name(note_name)
    return "Note removed."


@input_error
def show_notes_for_contact(args: List[str], book: AddressBook) -> str:
    """
    Show all notes for a contact.

    Args:
        args (List[str]): List containing the name.
        book (AddressBook): The address book instance.

    Returns:
        str: All notes for the contact or an error message.
    """
    try:
        name, *_ = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'show-notes [name]'"
        ) from e

    record = book.find(name)
    if not record or not record.notes:
        raise KeyError
    notes = "\n".join(str(note) for note in record.notes)
    return f"Notes for {name}:\n{notes}"


@input_error
def find_notes_by_keyword(args: List[str], book: AddressBook) -> str:
    """
    Find notes containing a specific keyword.

    Args:
        args (List[str]): List containing the keyword.
        book (AddressBook): The address book instance.

    Returns:
        str: List of notes containing the keyword or a message indicating none.
    """
    if not args:
        raise ValueError(
            "No keyword provided. Please provide a keyword to search. Use: 'find-notes [keyword]'"
        )

    try:
        keyword = args[0]
    except ValueError as e:
        raise ValueError(
            "No keyword provided. Please provide a keyword to search. Use: 'find-notes [keyword]'"
        ) from e

    notes_found = []

    # Iterate through all records in the address book
    for record in book.data.values():
        # Find notes in each record that contain the keyword
        notes = record.find_note_by_keyword(keyword)
        if notes:
            for note in notes:
                notes_found.append((record.name.value, note.name, note.value))

    # Format the output
    if notes_found:
        return "\n".join(
            f"Contact: {contact_name}, Note Name: {note_name}, Note: {note_value}"
            for contact_name, note_name, note_value in notes_found
        )
    return "No notes found containing the keyword."


@input_error
def add_email(args, book: AddressBook):
    """
    Add a email to an existing contact.
    """
    try:
        name, email = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'add-email [name] [email]'"
        ) from e
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_email(email)
    return "Email added."


@input_error
def add_address(args, book: AddressBook):
    """
    Add a address to an existing contact.
    """
    try:
        name, *address = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'add-address [name] [address]'"
        ) from e
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_address(address)
    return "Address added."


@input_error
def add_tag_to_contact(args: List[str], book: AddressBook):
    """
    Add a tag to a note within an existing contact.
    """
    if len(args) < 3:
        raise ValueError(
            "Incorrect input command argument. Use: 'add-tag [name] [note_name] [tag_name]'"
        )

    try:
        contact_name, note_name, tag_name, *_ = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'add-tag [name] [note_name] [tag_name]'"
        ) from e

    contact = book.data.get(contact_name)
    if not contact:
        raise KeyError(f"Contact with name '{contact_name}' not found.")

    note = next((note for note in contact.notes if note.name == note_name), None)
    if not note:
        raise KeyError(
            f"Note with name '{note_name}' not found in contact '{contact_name}'."
        )

    note.add_tag(tag_name)
    return "Tag added successfully."


@input_error
def remove_tag_from_contact(args: List[str], book: AddressBook):
    """
    Remove a tag from a note within an existing contact.
    """
    if len(args) < 3:
        raise ValueError(
            "Incorrect input command argument. Use: 'remove-tag [name] [note_name] [tag_name]'"
        )

    try:
        contact_name, note_name, tag_name, *_ = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'remove-tag [name] [note_name] [tag_name]'"
        ) from e

    contact = book.data.get(contact_name)
    if not contact:
        return f"Contact with name '{contact_name}' not found."

    note = next((note for note in contact.notes if note.name == note_name), None)
    if not note:
        record = book.find(contact_name)
        if not record:
            raise KeyError(
                f"Note with name '{note_name}' not found in contact '{contact_name}'."
            )
        return f"Note with name '{note_name}' not found in contact '{contact_name}'."

    try:
        note.remove_tag(tag_name)
        return "Tag removed successfully."
    except ValueError as e:
        return str(e)


@input_error
def find_notes_by_tag(args: List[str], book: AddressBook):
    """
    Find notes containing a specific tag.
    """
    if len(args) < 1:
        raise ValueError(
            "Incorrect input command argument. Use: 'find-notes-by-tag [tag_name]'"
        )

    try:
        tag, *_ = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'find-notes-by-tag [tag_name]'"
        ) from e

    notes = book.find_notes_by_tag(tag)
    if notes:
        return "\n".join(str(note) for note in notes)
    return "No notes found with the specified tag."


@input_error
def show_tags_for_contact(args: List[str], book: AddressBook) -> str:
    """
    Show all tags associated with a contact's notes.

    Args:
        args (List[str]): List containing the contact name.
        book (AddressBook): The address book instance.

    Returns:
        str: A list of tags or a message indicating none.
    """
    if len(args) < 1:
        raise ValueError(
            "Incorrect input command argument. Use: 'show-all-tags [name]'"
        )

    try:
        contact_name, *_ = args
    except ValueError as e:
        raise ValueError(
            "Incorrect input command argument. Use: 'show-all-tags [name]'"
        ) from e

    contact = book.data.get(contact_name)

    if not contact:
        raise KeyError(f"Contact with name '{contact_name}' not found.")

    tags = []
    for note in contact.notes:
        tags.extend(note.tags)

    if tags:
        return f"Tags for {contact_name}: {', '.join(tags)}"
    return f"No tags found for contact '{contact_name}'."


@input_error
def show_all_sorted_tags(_: List[str], book: AddressBook) -> str:
    """
    Show all unique tags from all contacts, sorted alphabetically.

    Args:
        args (List[str]): List of arguments (not used here).
        book (AddressBook): The address book instance.

    Returns:
        str: A list of all unique tags sorted alphabetically.
    """
    tags = set()

    for contact in book.data.values():
        for note in contact.notes:
            tags.update(note.tags)

    sorted_tags = sorted(tags)

    if sorted_tags:
        return "All tags sorted alphabetically:\n" + ", ".join(sorted_tags)
    return "No tags found in the address book."


@input_error
def show_all_notes_sorted_by_tags(_: List[str], book: AddressBook) -> str:
    """
    Show all notes sorted by tags across all contacts.

    Args:
        args (List[str]): An empty list as this function does not require any input arguments.
        book (AddressBook): The address book instance.

    Returns:
        str: A list of notes sorted by tags or a message indicating none.
    """
    all_notes = []

    # Collect all notes and tags
    for record in book.data.values():
        for note in record.notes:
            all_notes.append((note, record.name.value))

    # Sort notes by tags
    sorted_notes = sorted(all_notes, key=lambda x: (x[0].tags, x[0].value))

    # Formation of the result
    if sorted_notes:
        result = []
        for note, contact_name in sorted_notes:
            tags_str = f"[Tags: {', '.join(note.tags)}]" if note.tags else ""
            result.append(f"Contact: {contact_name}, Note: '{note.value}' {tags_str}")
        return "\n".join(result)

    return "No notes found in the address book."
