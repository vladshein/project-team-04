"""
class Record
"""

import re
from src.models.fields import Name, Birthday, Phone, PhoneNumberValueError


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
