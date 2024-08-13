"""
book controller
"""

import pickle
from typing import Callable, List, Tuple

from src.models.address_book import AddressBook, Record
from src.models.fields import PhoneNumberValueError, BirthdayValueError, NameValueError


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
        except (PhoneNumberValueError, BirthdayValueError, NameValueError) as e:
            return e
        except ValueError:
            return """Incorrect input command argument: add [name][phone],
                    change[name][old][new], phone[name],
                    add-birthday[name][date], show-birthday[name],
                    add-note[name][note name][note content],
                    edit-note[name][note name][new content],
                    remove-note[name][note name],
                    show-notes[name], find-notes[keyword]"""
        except KeyError:
            return "Contact not found or no contact information."
        except IndexError:
            return "Enter user name."

    return inner


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    """
        Parse user input into a command and its arguments.
    NameValueError
        Args:
            user_input (str): The raw input from the user.

        Returns:
            Tuple[str, List[str]]: The command and list of arguments.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


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
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


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
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if not record:
        raise KeyError
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
    name, *_ = args
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

    all_contacts = ""
    for _, phone in book.data.items():
        all_contacts += f"{phone}\n"
    return all_contacts.strip()


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
    name, birthday, *_ = args
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
    name, *_ = args
    record = book.find(name)
    if not record or not record.birthday:
        raise KeyError
    return str(record.birthday)


@input_error
def birthdays(_: list[str], book: AddressBook) -> str:
    """
    Show upcoming birthdays.

    Args:
        book (AddressBook): The address book instance.

    Returns:
        str: List of upcoming birthdays or a message indicating none.
    """
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
        raise ValueError("Insufficient arguments provided. Expected contact name, note name, and note content.")
    
    contact_name = args[0]
    note_name = args[1]
    note_content = " ".join(args[2:])  # Join the rest of the arguments as the note content

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
        raise ValueError("Insufficient arguments provided. Expected contact name, note name to edit, and new note content.")
    
    contact_name = args[0]
    note_name = args[1]
    new_note_content = " ".join(args[2:])  # Join the rest of the arguments as the new note content

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
        raise ValueError("Insufficient arguments provided. Expected contact name and note name.")
    
    contact_name = args[0]
    note_name = args[1]

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
    name, *_ = args
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
        raise ValueError("No keyword provided. Please provide a keyword to search.")
    
    keyword = args[0]
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
        return "\n".join(f"Contact: {contact_name}, Note Name: {note_name}, Note: {note_value}" 
                         for contact_name, note_name, note_value in notes_found)
    return "No notes found containing the keyword."
