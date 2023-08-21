import copy
import pickle
import re
from collections import UserDict
from datetime import date

from field import Field


class RecordAlreadyExists(Exception):
    pass


class PhoneAlreadyExistsError(Exception):
    pass


class PhoneNotFoundError(Exception):
    pass


class InvalidPhoneError(Exception):
    pass


class InvalidNameError(Exception):
    pass


class InvalidDateError(Exception):
    pass


class Name(Field):
    def is_valid(self, value):
        if type(value) == str:
            return True
        else:
            raise InvalidNameError


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self) -> str:
        return self.normalize_number(self.value)

    def __repr__(self) -> str:
        return self.normalize_number(self.value)

    def is_valid(self, value):

        value = value.strip()
        if re.match(r"(\+380\(\d{2}\)\d{3}\-(?:(?=\d{2}-)(\d{2}-\d{2})|(\d-\d{3})))", value):
            return value
        elif re.match(r"^\d{12}$", value):
            return f'{value}'
        elif re.match(r"^\+?\d{12}$", value):
            return value
        elif re.match(r"\+\d{2}\(\d{3}\)\d{7}", value):
            return value
        else:
            raise InvalidPhoneError

    def normalize_number(self, number):
        number = self.is_valid(number)
        number = re.sub(r'\D', '', number)
        return f'+{number[-12:]}'


class Birthday(Field):
    def is_valid(self, value):
        try:
            year, month, day = value.split('.')
            d = date(int(year), int(month), int(day))
            return True
        except:
            raise InvalidDateError

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid(value):
            year, month, day = value.split('.')
            self.__value = date(int(year), int(month), int(day))


class Record(Field):
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = None
        if phone:
            self.phones.append(phone)
        if birthday:
            self.birthday = birthday

    def add_phone(self, phone):
        for i in self.phones:
            if i.value == phone.value:
                raise PhoneAlreadyExistsError
        self.phones.append(phone)

    def change_phone(self, phone, new_phone):
        # I haven't find a better way to do it
        for i in self.phones:
            if i.value == phone.value:
                self.phones.remove(i)
                self.phones.append(new_phone)
                return
        raise PhoneNotFoundError

    def delete_phone(self, phone):
        for i in self.phones:
            if i.value == phone.value:
                self.phones.remove(i)
                return
        raise PhoneNotFoundError

    def days_to_birthday(self):
        if self.birthday:
            today = date.today()
            if today.month > self.birthday.value.month or \
                    (today.month == self.birthday.value.month and today.day > self.birthday.value.day):
                # if birthday is next year
                next_birthday = self.birthday.value.replace(year=today.year + 1)
            else:
                next_birthday = self.birthday.value.replace(year=today.year)
            return (next_birthday - today).days
        else:
            return None


class ContactsIterator():
    def __init__(self, contacts, N=3):
        self.contacts = contacts
        self.N = N
        self.current_index = 0

    def __next__(self):
        if self.current_index < len(self.contacts):
            start = self.current_index
            page = []
            for c in self.contacts[start: min(start + self.N, len(self.contacts))]:
                page.append(c)
                self.current_index += 1
            return page
        raise StopIteration


class AddressBook(UserDict):
    save_file = "contacts.bin"

    def add_record(self, name, phone=None, birthday=None):
        # only adds new records
        if name.value in self.data:
            raise RecordAlreadyExists
        else:
            self.data[name.value] = Record(name, phone, birthday)

    def __iter__(self):
        return ContactsIterator(list(self.data.values()))

    def find_records(self, str=""):
        if str:
            matches = []
            for r in self.data:
                if r.find(str) != -1:
                    matches.append(self.data[r])
                else:
                    record = self.data[r]
                    for p in record.phones:
                        if p.value.find(str) != -1:
                            matches.append(self.data[r])
                            break
            return matches

        return None

    def save_contacts(self):
        with open(self.save_file, "wb") as file:
            pickle.dump(self.data, file)

    def read_contacts(self):
        try:
            with open(self.save_file, "rb") as file:
                content = pickle.load(file)
                if content:
                    self.data = copy.deepcopy(content)
        except:
            pass

    def get_data_list(self):
        data_list = []
        for k in self.data:
            data_list.append(k)
        return data_list
