from command_parser import parse_command, exception_catcher_decorator
from command_parser import ExcessiveArguments, WrongArgumentFormat
from interface import (
    InformationOutputManager,
    ConsoleUI,
    Manager,
    Menu,
    UserInput,
    ConsoleUserInput,
    ABCRecord,
)
from collections import UserDict
from datetime import datetime, timedelta
import json, re
import logging

logger = logging.getLogger("Address Debugger")
logger.setLevel(logging.DEBUG)
formatter_print = logging.Formatter("%(message)s")
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter_print)

fh = logging.FileHandler("address_log.txt")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

"""Class Field виступає головним класом від якого наслідуються інші класи, такі як: Birthday, Name, Phone, Email, 
Address. Використовується для приведення типів данних."""


class Field:
    def __init__(self, value: str) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"{self._value}"

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        self._value = new_value


"""Class Birthdaay наслідується від Field, приймає день народження формату str і повертає у вигляді date."""


class Birthday(Field):
    def __init__(self, value: str) -> None:
        self.__value = value  # from 10 January 2020

    def _days_to_birthday(self) -> int:
        datenow = datetime.now().date()
        future_bday_date = datetime(
            year=datenow.year, month=self.value.month, day=self.value.day
        ).date()

        if future_bday_date < datenow:
            future_bday_date = datetime(
                year=datenow.year + 1, month=self.value.month, day=self.value.day
            ).date()

        delta = future_bday_date - datenow
        pure_days = delta.days % 365
        return pure_days

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, new_value: str) -> str:
        try:
            self.__value = datetime.strptime(new_value, "%d %B %Y").date()
        except ValueError:
            logger.debug(
                'Your data format is not correct! Please use this one: "10 January 2020"'
            )
            raise WrongArgumentFormat

    def __repr__(self) -> str:
        return f'{self.value.strftime("%d %B %Y")}'


"""Class Name наслідується від Field, приймає ім'я формату str і повертає його."""


class Name(Field):
    def __init__(self, value: str) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"{self._value}"


"""Class Phone наслідується від Field, приймає номер телефону формату str, проводить його валідацію на коректність 
введення, конвертує його до формату +380999999999 та повертає у новому вигляді."""


class Phone(Field):
    def __init__(self, value: str) -> None:
        self.__value = value

    def __repr__(self) -> str:
        return f"{self.__value}"

    @property
    def value(self) -> str:
        return self.__value

    @staticmethod
    def valid_phone(phone: str) -> bool:
        if 10 <= len(phone) <= 13:
            if phone.replace("+", "").isdigit():
                return True

            return False

        else:
            return False

    @staticmethod
    def convert_phone_number(phone: str) -> str:
        correct_phone_number = ""

        if phone.startswith("+380") and len(phone) == 13:
            correct_phone_number = phone
        elif phone.startswith("80") and len(phone) == 11:
            correct_phone_number = "+3" + phone
        elif phone.startswith("0") and len(phone) == 10:
            correct_phone_number = "+38" + phone
        else:
            logger.debug(
                "Number format is not correct! Must contain 10-13 symbols and must match the one of the current "
                "formats: +380001112233 or 80001112233 or 0001112233!"
            )
            raise WrongArgumentFormat

        return correct_phone_number

    @value.setter
    def value(self, new_value: str) -> None:
        is_valid = self.valid_phone(new_value)
        if is_valid:
            self.__value = self.convert_phone_number(new_value)
        else:
            logger.debug(
                "Number format is not correct! Must contain 10-13 symbols and must match the one of the current "
                "formats: +380001112233 or 80001112233 or 0001112233!"
            )
            raise WrongArgumentFormat


"""Class Email наслідується від Field, приймає емейл формату str, проводить його валідацію на коректність 
введення та повертає."""


class Email(Field):
    def __init__(self, value: str) -> None:
        self.__value = value

    def __repr__(self) -> str:
        return f"{self.__value}"

    @property
    def value(self) -> str:
        return self.__value

    @staticmethod
    def valid_email(email: str) -> bool:
        if re.match(
            r"^[\w.+\-]{1}[\w.+\-]+@\w+\.[a-z]{2,3}\.[a-z]{2,3}$", email
        ) or re.match(r"^[\w.+\-]{1}[\w.+\-]+@\w+\.[a-z]{2,3}$", email):
            return True
        return False

    @value.setter
    def value(self, new_value: str) -> None:
        is_valid = self.valid_email(new_value)
        if is_valid:
            self.__value = new_value
        else:
            logger.debug(
                'The email address is not valid! Must contain min 2 characters before "@" and 2-3 symbols in TLD! '
                "Example: aa@example.net or aa@example.com.ua"
            )
            raise WrongArgumentFormat


"""Class Address наслідується від Field, приймає адресу формату str та повертає."""


class Address(Field):
    def __init__(self, value: str) -> None:
        self.__value = value

    def __repr__(self) -> str:
        return f"{self.__value}"

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, new_value: str) -> None:
        self.__value = new_value


class Record(ABCRecord):
    def __init__(
        self,
        name: Name,
        phone: Phone,
        email_value: Email = None,
        address_value: Address = None,
    ) -> None:
        self.name = name
        self.phones = []
        self.phones.append(phone)
        self.email = None
        self.address = None

        if email_value:
            self.email = Email("")
            self.email = email_value  # add email if not empty

        if address_value:
            self.address = Address("")
            self.address = address_value

        self.birthday = ""

    def __repr__(self) -> None:
        return f"{self.name}; {self.phones}; {self.birthday if self.birthday else ''}; {self.email if self.email else ''}; {self.address if self.address else ''}"

    def add_phone(self, phone: str) -> None:
        new_phone = Phone("")

        # валидация висит на сеттере Phone
        new_phone.value = str(phone)

        if new_phone.value not in [ph for ph in self.phones]:
            self.phones.append(new_phone)
            logger.debug(
                f"{new_phone} record was successfully added for {self.name.value}"
            )
        else:
            logger.debug(
                f"{new_phone} is already actually recorded in {self.name.value}"
            )

    def edit_phone(self, old_phone: str) -> str:
        new_phone_value = ""

        for index, phone in enumerate(self.phones, 0):
            if phone.value == Phone.convert_phone_number(old_phone):
                new_phone_value = input("Please input the new phone number: ")
                new_phone_value = Phone.convert_phone_number(new_phone_value)

                if Phone.valid_phone(new_phone_value):
                    self.phones[index] = new_phone_value
                    break

                else:
                    logger.debug(
                        "Number format is not correct! Must contain 10-13 symbols and must match the one of the current "
                        "formats: +380001112233 or 80001112233 or 0001112233!"
                    )
                    break

        return new_phone_value

    def delete_phone(self, phone: str) -> None:
        for index, record in enumerate(self.phones, 0):
            if record == Phone.convert_phone_number(phone):
                self.phones.pop(index)
                logger.debug(f"{phone} was successfully deleted for {self.name.value}")
                return

        logger.debug("No such phone record!")

    def _days_to_birthday(self) -> None:
        if self.birthday == "":
            logger.debug(f"BDay record is not set for {self.name.value}!")
            return

        days_left = self.birthday._days_to_birthday()
        logger.debug(
            f'{self.name.value}\'s birthday will be roughly in {days_left} days! ({self.birthday.value.strftime("%d %B %Y")})'
        )

    def set_birthday(self, date_val: str) -> None:
        self.birthday = Birthday("")
        self.birthday.value = date_val
        logger.debug(f"{self.birthday} BDay record was added for {self.name.value}!")

    def set_email(self, email_val: str) -> None:
        self.email.value = email_val
        logger.debug(f"{self.email} email record was added for {self.name.value}!")


# Lower Entity Classes
class AddressBook(UserDict):
    def __init__(self) -> None:
        super().__init__()
        self.is_finished = False
        self._load()

    def add_record(self, record: Record, *_) -> None:
        self.data.update({record.name.value: record})

    def delete_record(self, contact_name: Name) -> None:
        if str(contact_name) in self.data:
            del self.data[str(contact_name)]
            return None

    def _save(self) -> None:
        file_data = []

        for record in self.data.values():
            write_dict = {}
            write_dict["name"] = record.name.value
            write_dict["Phone number"] = [str(ph) for ph in record.phones]
            write_dict["Date of birth"] = (
                record.birthday.value.strftime("%d %B %Y") if record.birthday else ""
            )
            write_dict["email"] = str(record.email) if record.email else ""
            write_dict["address"] = str(record.address) if record.address else ""
            file_data.append(write_dict)

        with open("save.json", "w") as writer:
            json.dump(file_data, writer, indent=4)

    def iterator(self, n: int) -> None:
        counter = 0

        if n > len(self.data):
            n = len(self.data)
            logger.debug(
                f"Seems like there is only {len(self.data)} items in the book!"
            )
            counter = len(self.data) + 1

        for key, value in self.data.items():
            recorded_phones = ""
            recorded_phones = ", ".join([str(ph) for ph in value.phones])
            logger.debug(
                f"{key}| Phones: {recorded_phones} | BDay: {value.birthday} | Email: {value.email} | Address: {value.address}"
            )
            counter += 1

            if counter == n:
                counter = 0
                logger.debug("*" * 10)
                yield

        logger.debug("This was the end of the address book!")
        return

    def _load(self) -> None:
        try:
            with open("save.json") as reader:
                try:
                    file_data = json.load(reader)

                    for item in file_data:
                        name = Name(item["name"])
                        row_phones = item["Phone number"]
                        row_email = Email(item["email"])
                        row_address = Address(item["address"])
                        record = Record(
                            name, Phone(row_phones[0]), row_email, row_address
                        )

                        iter = 1
                        while iter < len(row_phones):
                            record.add_phone(row_phones[iter])
                            iter += 1

                        if item["Date of birth"] == "":
                            record.birthday = ""
                        else:
                            record.set_birthday(item["Date of birth"])

                        self.data[item["name"]] = record

                except json.decoder.JSONDecodeError:
                    file_data = []

        except FileNotFoundError:
            with open("save.json", "w"):
                ...


# Interface Classes
# '''Main IU class that user directly should work with'''
class AddressBookConsoleUI(ConsoleUI):
    def __init__(
        self,
        output_interface: InformationOutputManager,
        manager_interface: Manager,
        menu_interface: Menu,
        input_interface: UserInput,
    ) -> None:
        super().__init__(
            output_interface, manager_interface, menu_interface, input_interface
        )

        # available command list
        self.command_list = {
            "not save": manager_interface._close_without_saving,
            "good bye": manager_interface._finish_session,
            "close": manager_interface._finish_session,
            "hello": output_interface._hello,
            "add": manager_interface._add_record,
            "add phone": manager_interface._add_phone,
            "edit phone": manager_interface._edit_phone,
            "show all": output_interface._show_all_items,
            "show some": output_interface._show_some_items,
            "delete phone": manager_interface._delete_phone,
            "delete contact": manager_interface._delete_record,
            "set bday": manager_interface._set_birthday,
            "set email": manager_interface._set_email,
            "set address": manager_interface._set_address,
            "show bday": output_interface._show_birthday,
            "show email": output_interface._show_email,
            "show address": output_interface._show_address,
            "find": output_interface._find,
            "help": self.display_menu,
            "bday in": output_interface._show_bday_in_days,
        }

    # Universal command performer/handler
    @exception_catcher_decorator
    def perform_command(self, command: str, adr_book, *args, **kwargs) -> None:
        self.command_list[command](adr_book, *args, **kwargs)

    def get_user_input(self) -> str:
        return self.input_interface.get_user_input()

    def display_menu(self, *_) -> None:
        self.menu_interface.show_menu()


# '''User Input Manager Class'''
class AddressBookUserInput(ConsoleUserInput):
    ...


# '''Information Output Manager Class'''
class AdressBookInformationOutput(InformationOutputManager):
    @exception_catcher_decorator
    def _find(self, adr_book: AddressBook, line_list: list) -> None:
        if len(line_list) > 3:
            raise ExcessiveArguments

        str_to_find = line_list[1]
        is_empty = True
        logger.debug(f"Looking for {str_to_find}. Found...")

        for record in adr_book.data.values():
            phones_string = ", ".join([str(ph) for ph in record.phones])

            if record.name.value.find(str_to_find) != -1:
                is_empty = False
                logger.debug(
                    f"Name: {record.name} | Phones: {phones_string} | Birthday: {record.birthday} | Email: {record.email} | Address: {record.address}"
                )
                continue

            elif record.email.value.find(str_to_find) != -1:
                is_empty = False
                logger.debug(
                    f"Name: {record.name} | Phones: {phones_string} | Birthday: {record.birthday} | Email: {record.email} | Address: {record.address}"
                )
                continue

            elif record.address.value.find(str_to_find) != -1:
                is_empty = False
                logger.debug(
                    f"Name: {record.name} | Phones: {phones_string} | Birthday: {record.birthday} | Email: {record.email} | Address: {record.address}"
                )
                continue

            for phone in record.phones:
                if phone.value.find(str_to_find) != -1:
                    is_empty = False
                    logger.debug(
                        f"Name: {record.name} | Phones: {phones_string} | Birthday: {record.birthday} | Email: {record.email} | Address: {record.address}"
                    )
                    break

        if is_empty:
            logger.debug("Nothing!")

    @exception_catcher_decorator
    def _hello(self, *_) -> None:
        logger.debug("How can I help you?")

    @exception_catcher_decorator
    def _show_all_items(self, adr_book, *_) -> None:
        if bool(adr_book.data) == False:
            logger.debug("Your list is empty!")
            return

        for record in adr_book.data:
            if bool(adr_book.data[record].phones) == False:
                logger.debug(f"Your list for {record} is empty!")
                continue

            logger.debug(
                f'Phones for {record} (email = "{adr_book.data[record].email.value}", address = "{adr_book.data[record].address.value}", BDay = "{adr_book.data[record].birthday}"):'
            )
            for id, phone in enumerate(adr_book.data[record].phones, 1):
                logger.debug(f"{id}) - {phone}")

    @exception_catcher_decorator
    def _show_some_items(self, adr_book, *_) -> None:
        n = input("How much records to show at a time? ")
        logger.debug("*" * 10)
        iterator = adr_book.iterator(int(n))

        try:
            next(iterator)
        except StopIteration:
            return

        while True:
            action = input("Show next part? (Y/N): ").casefold()

            if action == "y":
                try:
                    logger.debug("*" * 10)
                    next(iterator)
                except StopIteration:
                    return
            elif action == "n":
                return
            else:
                logger.debug("I do not understand the command!")

    @exception_catcher_decorator
    def _show_email(self, adr_book: AddressBook, line_list: list, *_) -> None:
        record_name = line_list[1]

        if adr_book.data[record_name].email.value:
            logger.debug(f"It is {adr_book.data[record_name].email}")
        else:
            logger.debug("It is EMPTY!")

    @exception_catcher_decorator
    def _show_birthday(self, adr_book: AddressBook, line_list: list, *_) -> None:
        record_name = line_list[1]
        adr_book.data[record_name]._days_to_birthday()

    @exception_catcher_decorator
    def _show_address(self, adr_book: AddressBook, line_list: list, *_) -> None:
        record_name = line_list[1]
        address = adr_book.data[record_name].address

        if address:
            logger.debug(f"Address for {record_name}: {address}")
        else:
            logger.debug(f"No address is set for {record_name}")

    @exception_catcher_decorator
    def _show_bday_in_days(self, adr_book: AddressBook, line_list: list, *_) -> None:
        days_timeframe = line_list[1]

        try:
            days_timeframe = int(days_timeframe)
        except ValueError:
            logger.debug("Timeframe should be a number!")
            raise WrongArgumentFormat
        except TypeError:
            logger.debug("Timeframe should be a number!")
            raise WrongArgumentFormat

        if days_timeframe < 0:
            logger.debug("Timeframe could not be a negative number!")
            raise WrongArgumentFormat

        datetime_timedelta = timedelta(days=int(days_timeframe))
        is_empty = True

        logger.debug(f"You wanted to see Bdays in {days_timeframe} days! Here we go: ")

        for record in adr_book.data.values():
            if type(record.birthday) == str:
                continue

            record_timedelta = timedelta(days=record.birthday._days_to_birthday())

            if record_timedelta <= datetime_timedelta:
                recorded_phones = ", ".join([str(ph) for ph in record.phones])

                logger.debug("=" * 10)
                logger.debug(
                    f"{record.name} will have a BDay in {record_timedelta.days}! ({record.birthday})"
                )
                logger.debug(
                    f"His data: phones - {recorded_phones}, email - {record.email}, address - {record.address}"
                )

                is_empty = False

        if is_empty:
            logger.debug("Sorry! Seems like nobody have BDays in the set timeframe!")


# '''Manager Class That Apply Changes To The Book'''
class AddressBookManager(Manager):
    @exception_catcher_decorator
    def _add_record(self, adr_book: AddressBook, line_list: list) -> None:
        if len(line_list) < 3:
            logger.debug("Not enough arguments for add_record!")
            return

        name = Name(line_list[1])
        phone_number = Phone("")
        phone_number.value = line_list[2]

        email = Email("")
        address = Address("")

        for item in line_list[3:]:
            if "@" in item:
                email.value = item
            else:
                address.value += " " + item

        record = Record(name, phone_number, email, address)
        adr_book.add_record(record)
        logger.debug(
            f"Added record for {name.value} with {phone_number.value}, email '{email.value}', and address '{address.value}' my lord."
        )

    @exception_catcher_decorator
    def _add_phone(self, adr_book: AddressBook, line_list: list):
        if len(line_list) > 3:
            raise ExcessiveArguments

        record_name = line_list[1]
        phone = line_list[2]

        try:
            adr_book.data[record_name]
        except KeyError:
            logger.debug(f"Cannot find name {record_name} in the list!")
            return

        adr_book.data[record_name].add_phone(phone)

    @exception_catcher_decorator
    def _edit_phone(self, adr_book: AddressBook, line_list: list) -> None:
        if len(line_list) > 3:
            raise ExcessiveArguments

        try:
            record_name = line_list[1]
            adr_book.data[record_name]
        except KeyError:
            logger.debug(f"Cannot find name {record_name} in the list!")
            return

        old_phone = line_list[2]
        new_phone = adr_book.data[record_name].edit_phone(old_phone)

        if new_phone:
            logger.debug(
                f"{old_phone} was successfully changed to {new_phone} for {record_name}"
            )
        else:
            logger.debug(f"{old_phone} phone number was not found for {record_name}!")

    @exception_catcher_decorator
    def _delete_phone(self, adr_book: AddressBook, line_list: list) -> None:
        if len(line_list) > 3:
            raise ExcessiveArguments

        record_name = line_list[1]
        phone = line_list[2]

        try:
            adr_book.data[record_name]
        except KeyError:
            logger.debug(f"Cannot find name {record_name} in the list!")
            return

        adr_book.data[record_name].delete_phone(phone)

    @exception_catcher_decorator
    def _delete_record(self, adr_book: AddressBook, line_list: list) -> None:
        if len(line_list) > 3:
            raise ExcessiveArguments
        if line_list[1] in adr_book.data:
            name = Name(line_list[1])
            adr_book.delete_record(name)
            logger.debug(f"Removed record for {line_list[1]}, my lord.")
        else:
            logger.debug("No such phone record!")

    def _close_without_saving(self, adr_book, *_):
        adr_book.is_finished = True
        logger.debug("Will NOT save! BB!")

    def _finish_session(self, adr_book, *_) -> bool:
        adr_book._save()
        adr_book.is_finished = True
        logger.debug("Good bye!")

    @exception_catcher_decorator
    def _set_email(self, adr_book: AddressBook, line_list: list, *_) -> None:
        record_name = line_list[1]

        try:
            adr_book.data[record_name]
        except KeyError:
            logger.debug(f"Cannot find name {record_name} in the list!")
            return

        email_val = input('Please set the email like "myemail@google.com": ')

        if email_val:
            adr_book.data[record_name].set_email(email_val)

    @exception_catcher_decorator
    def _set_birthday(self, adr_book: AddressBook, line_list: list, *_):
        record_name = line_list[1]

        try:
            adr_book.data[record_name]
        except KeyError:
            logger.debug(f"Cannot find name {record_name} in the list!")
            return

        date_val = input('Please set the birthday date like "10 January 2020": ')
        adr_book.data[record_name].set_birthday(date_val)

    @exception_catcher_decorator
    def _set_address(self, adr_book: AddressBook, line_list: list, *_) -> None:
        record_name = line_list[1]

        try:
            adr_book.data[record_name]
        except KeyError:
            logger.debug(f"Cannot find name {record_name} in the list!")
            return
        address_val = input("Please set the address: ")
        adr_book.data[record_name].address = address_val
        logger.debug(f"Address {address_val} was set successfully for {record_name}!")


# '''Menu Class That Works With Menu'''
class AddressBookMenu(Menu):
    def __init__(self) -> None:
        # command vocab with descriptions
        self.command_description = {
            "not save": "Close adress book without saving",
            "good bye": "Save changes and close address book",
            "close": "Save changes and close address book",
            "hello": "Hear some greeting from me",
            "add": "Add a new record",
            "add phone": "Add new phone to the existing record",
            "edit phone": "Edit a phone of the existing record",
            "show all": "Show all the records",
            "show some": "Show some number of the records at a time",
            "delete phone": "Delete the phone of the existing record",
            "delete contact": "Delete record completely",
            "set bday": "Set a BDay for the existing record",
            "set email": "Set an email for the existing record",
            "set address": "Set an adress for the existing record",
            "show bday": "Show a BDay for the existing record",
            "show email": "Show an email for the existing record",
            "show address": "Show an address for the existing record",
            "find": "Find record that contains ...",
            "help": "Show full list of available commands",
            "bday in": "Show records that have BDay in set timeframe of days",
        }

    def show_menu(self, *_) -> None:
        logger.debug(f"Available commands:")
        for command, description in self.command_description.items():
            logger.debug(f"{command} - {description}")


# MAIN func
def main() -> None:
    output_interface = AdressBookInformationOutput()
    manager_interface = AddressBookManager()
    menu_interface = AddressBookMenu()
    input_interface = AddressBookUserInput()
    ui = AddressBookConsoleUI(
        output_interface, manager_interface, menu_interface, input_interface
    )

    adr_book = AddressBook()

    logger.debug("*" * 10)
    ui.output_interface._hello()
    logger.debug("*" * 10)
    ui.menu_interface.show_menu()

    while True:
        logger.debug("*" * 10)
        user_input = ui.get_user_input()
        line_list = parse_command(user_input, ui.command_list)
        current_command = line_list[0].casefold()
        ui.perform_command(current_command, adr_book, line_list)

        # checker to return to jason.py, bcz decorator over 'perform_command' returns None and makes it tricky
        if adr_book.is_finished:
            break


# EXECUTE
if __name__ == "__main__":
    main()
