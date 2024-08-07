"""
AddressBook
"""
from datetime import datetime, timedelta
from collections import UserDict
from src.models.record import Record


class AddressBook(UserDict):
    """
    Class for storing and managing contact records. Inherits from UserDict.
    """

    def add_record(self, record: Record) -> None:
        """
        Adds a record to the address book.

        Args:
            record (Record): The record to add.
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """
        Finds a record by name in the address book.

        Args:
            name (str): The name to search for.

        Returns:
            Record: The record if found, or None.
        """
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """
        Deletes a record by name from the address book.

        Args:
            name (str): The name of the record to delete.
        """
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        """
        Returns a list of users with upcoming birthdays, including the congratulation date.

        Returns:
            list[dict[str, str]]: List of users with upcoming birthdays.
        """
        users_upcoming_birthday = []
        today = datetime.today().date()
        for user_name, user in self.data.items():
            if user.birthday:
                birthday_date = user.birthday.value

                # Set the birthday to the current year
                birthday_this_year = birthday_date.replace(year=today.year)

                # If the birthday this year has already passed, set it to next year
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                # Check if the birthday is within the next 7 days
                if 0 <= (birthday_this_year - today).days <= 7:
                    # Adjust the birthday to avoid weekends
                    while birthday_this_year.weekday() in [5, 6]:
                        birthday_this_year += timedelta(days=1)
                    users_upcoming_birthday.append(
                        {
                            "name": user_name,
                            "congratulation_date": birthday_this_year.strftime(
                                "%d.%m.%Y"
                            ),
                        }
                    )
        return users_upcoming_birthday
