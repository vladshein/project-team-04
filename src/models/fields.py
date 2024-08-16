"""
Fields record in address book.
"""

import re
from datetime import datetime


class NameValueError(Exception):
    """
    custom Error for incorrect input name
    """


class PhoneNumberValueError(Exception):
    """
    custom Error for incorrect input Phone number
    """


class BirthdayValueError(Exception):
    """
    custom Error for incorrect input birthday date
    """


class NoteValueError(Exception):
    """
    Custom error for incorrect input note.
    """


class EmailValueError(Exception):
    """
    custom Error for incorrect input Email
    """


class AddressValueError(Exception):
    """
    custom Error for incorrect input Address
    """


class Field:
    """
    Base class for storing field values of a record.

    Attributes:
        value (str): The value of the field.
    """

    def __init__(self, value: str):
        """
        Initializes the field.

        Args:
            value (str): The value of the field.
        """
        self.value = value

    def __str__(self) -> str:
        """
        Returns a string representation of the field value.

        Returns:
            str: The value of the field as a string.
        """
        return str(self.value)


class Name(Field):
    """
    Class for storing a contact's name. Inherits from Field.
    """

    def __init__(self, name: str) -> None:
        if len(name) < 2:
            raise NameValueError("The name must be more than two characters long")
        super().__init__(name)


class Phone(Field):
    """
    Class for storing a phone number. Inherits from Field.
    Validates the phone number format (10 digits).
    """

    def __init__(self, value: str):
        """
        Initializes the phone number with validation.

        Args:
            value (str): The phone number.

        Raises:
            ValueError: If the phone number does not match the format (10 digits).
        """
        if not re.fullmatch(r"0\d{9}", value):
            raise PhoneNumberValueError(
                "Phone number must be 10 digits in format: 0XXXXXXXXX"
            )
        super().__init__(value)


class Birthday(Field):
    """
    Class for storing and validating a birthday. Inherits from Field.
    """

    def __init__(self, value: str):
        """
        Initializes the birthday with validation.

        Args:
            value (str): The birthday in the format "DD.MM.YYYY".

        Raises:
            ValueError: If the birthday does not match the required format.
        """
        if not re.fullmatch(r"[0123]\d\.[01]\d\.[12][09]\d{2}", value):
            raise BirthdayValueError("Date must be in format: DD.MM.YYYY and age < 120")
        try:
            birthday = self.convert_str_to_date(value)
            super().__init__(birthday)
        except ValueError as exc:
            raise BirthdayValueError("Invalid date format. Use DD.MM.YYYY") from exc
        if birthday <= datetime.now().date():
            super().__init__(birthday)
        else:
            raise BirthdayValueError("The date cannot be in the future ")

    @staticmethod
    def convert_str_to_date(date: str) -> datetime.date:
        """
        Convert date string to date object.

        Args:
            date (str): The date string in the format "DD.MM.YYYY".

        Returns:
            datetime.date: The corresponding date object.
        """
        return datetime.strptime(date, "%d.%m.%Y").date()

    def __str__(self) -> str:
        """
        Returns a string representation of the birthday.

        Returns:
            str: The birthday in the format "DD.MM.YYYY".
        """
        return self.value.strftime("%d.%m.%Y")


class Note(Field):
    """
    Class for storing a note associated with a contact, including a name.
    """

    def __init__(self, value: str, name: str = None):
        if len(value) < 1:
            raise NoteValueError("Note cannot be empty")
        self.name = name
        super().__init__(value)

    def __str__(self) -> str:
        """
        Returns a string representation of the note, including its name if provided.

        Returns:
            str: The note content, and if available, the name.
        """
        if self.name:
            return f"{self.name}: '{self.value}'"
        return f"Note: '{self.value}'"


class Email(Field):
    """
    Class for storing an Email. Inherits from Field.
    Validates the email format (xxxxx@xx.xx).
    """

    def __init__(self, value: str):
        """
        Initializes the Email with validation.

        Args:
            value (str): The Email.

        Raises:
            ValueError: If the Email does not match the format (xxxxx@xx.xx).
        """
        if not re.fullmatch(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$", value):
            raise EmailValueError("Invalid Email. Use xxxxx@xx.xx")
        super().__init__(value)


class Address(Field):
    """
    Class for storing an Address. Inherits from Field.
    Validates that field is not empty.
    """

    def __init__(self, address: str):
        """
        Initializes the Address with validation.

        Args:
            value (str): The Address.

        Raises:
            ValueError: If the Address is empty.
        """
        if len(address) < 4:
            raise AddressValueError(
                "The address must be more than four characters long"
            )
        super().__init__(address)
