"""
class Record
"""

import re
from src.models.fields import Name, Birthday, Phone, Note, PhoneNumberValueError, NoteValueError


class Record:
    """
    Class for storing contact information, including name, phone numbers, and birthday.

    Attributes:
        name (Name): The contact's name.
        phones (list of Phone): The contact's phone numbers.
        birthday (Birthday): The contact's birthday.
    """

    def __init__(self, name: str):
        """
        Initializes the record with the contact's name.

        Args:
            name (str): The contact's name.
        """
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.notes = []


    def add_birthday(self, birthday: str) -> None:
        """
        Adds a birthday to the record.

        Args:
            birthday (str): The birthday to add.
        """
        self.birthday = Birthday(birthday)

    def add_phone(self, phone_number: str) -> None:
        """
        Adds a phone number to the record.

        Args:
            phone_number (str): The phone number to add.
        """
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        """
        Removes a phone number from the record.

        Args:
            phone_number (str): The phone number to remove.
        """
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise PhoneNumberValueError("Phone number not found")

    def edit_phone(self, old_number: str, new_number: str) -> None:
        """
        Edits a phone number in the record.

        Args:
            old_number (str): The old phone number.
            new_number (str): The new phone number.
        """
        phone_to_edit = self.find_phone(old_number)
        if phone_to_edit:
            if not re.fullmatch(r"\d{10}", new_number):
                raise PhoneNumberValueError("Phone number must be 10 digits")
            phone_to_edit.value = new_number
        else:
            raise PhoneNumberValueError("Phone number not found")

    def find_phone(self, phone_number: str) -> Phone:
        """
        Finds a phone number in the record.

        Args:
            phone_number (str): The phone number to find.

        Returns:
            Phone: The phone number if found, or None.
        """
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def add_note(self, note: str, name: str = None) -> None:
        """
        Adds a new note to the record with an optional name.

        Args:
            note (str): The content of the note to add.
            name (str, optional): The name associated with the note.
        """
        self.notes.append(Note(note, name))

    def edit_note(self, old_name: str, new_note: str) -> None:
        """
        Edits an existing note in the record by note name.

        Args:
            old_name (str): The name of the note to be replaced.
            new_note (str): The new content to replace the old note.
        Raises:
            NoteValueError: If the new note is empty or the old note is not found.
        """
        for i, note in enumerate(self.notes):
            if note.name == old_name:
                if not new_note:
                    raise NoteValueError("Note cannot be empty")
                self.notes[i] = Note(new_note, note.name)
                return
        raise NoteValueError("Note with the given name not found")

    def remove_note_by_name(self, name: str) -> None:
        """
        Removes a note from the record by name.

        Args:
            name (str): The name associated with the note to remove.

        Raises:
            NoteValueError: If no note with the given name is found.
        """
        for i, existing_note in enumerate(self.notes):
            if existing_note.name == name:
                del self.notes[i]
                return
        
        raise NoteValueError(f"Note with the name '{name}' not found")
    
    def find_note_by_keyword(self, keyword: str) -> list:
        """
        Finds notes containing a specific keyword.

        Args:
            keyword (str): The keyword to search for in the notes.

        Returns:
            list: A list of notes that contain the keyword.
        """
        return [note for note in self.notes if keyword in note.value]

    def __str__(self) -> str:
        """
        Returns a string representation of the record.

        Returns:
            str: The string representation of the record.
        """
        phone_list = "; ".join(p.value for p in self.phones)
        birthday_str = f", {self.birthday}" if self.birthday else ""
        return (
            f"Contact name: {self.name.value:<10}| phones: {phone_list}{birthday_str}"
        )
