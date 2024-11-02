from collections import UserDict
from exceptions import PhoneException, RecordNotFound


def main():
    class Field:
        """
        Base class for record fields
        """

        def __init__(self, value: str):
            self.value = value

        def __str__(self):
            return str(self.value)


    class Name(Field):
        """
        Class for record's Name field
        """

        def __init__(self, name: str):
            super().__init__(name)


    class Phone(Field):
        """
        Class for record's Phone field
        """

        def __init__(self, phone: str):
            if len(phone) != 10:
                raise PhoneException("The phone number must contain 10 characters.")
            super().__init__(phone)


    class Record:
        """
        Class for the Record in the Address Book
        """

        def __init__(self, name: str):
            self.name = Name(name)
            self.phones = []

        def __str__(self):
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

        def add_phone(self, phone: str):
            if phone in [phone.value for phone in self.phones]:
                raise PhoneException("This phone already exists")
            self.phones.append(Phone(phone))

        def remove_phone(self, phone):
            phones = [p.value for p in self.phones]
            phone_index = phones.index(phone)
            self.phones.pop(phone_index)

        def edit_phone(self, *args):
            phones = [p.value for p in self.phones]
            try:
                old_phone_idx = phones.index(args[0])
                self.phones.pop(old_phone_idx)
                self.phones.insert(old_phone_idx, Phone(args[1]))
            except ValueError:
                raise PhoneException("Phone not found")

        def find_phone(self, phone: str):
            for record_phone in self.phones:
                if record_phone.value == phone:
                    return record_phone.value
            return "Phone not found"


    class AddressBook(UserDict):
        """
        Class for the Address Book that stores and manages all records
        """

        records = 0

        def add_record(self, record: Record):
            self.data[record] = AddressBook.records
            AddressBook.records += 1

        def find(self, name: str):
            for record in self.data.keys():
                record_name = record.name.value
                if record_name == name:
                    return record

        def delete(self, name: str):
            records = list(
                filter(lambda record: record.name.value == name, self.data.keys())
            )
            if not len(records):
                raise RecordNotFound("The Record with this name not found.")
            self.data.pop(records[0])
            AddressBook.records -= 1

    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_phone("5555566666")
    print(
        [p.value for p in john_record.phones] # Виведення ['1234567890', '5555555555', '5555566666']
    )  
    john_record.remove_phone("5555566666")
    print(
        [p.value for p in john_record.phones] # Виведення ['1234567890', '5555555555']
    )  

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for record in book.data.keys():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name.value}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
