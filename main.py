from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для зберігання імені контакту. Обов'язкове поле
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError('Name is required') # Помилка якщо імʼя не додане
        super().__init__(value)

# Клас для зберігання номера телефону
class Phone(Field):
    def __init__(self, value):
        # Перевірка - номер телефону повинен складатися з цифр і мати довжину 10 знаків
        if not value.isdigit() or len(value) != 10:
            raise ValueError(f'Phone number: "{value}" is incorrect')
        super().__init__(value)

# Клас для зберігання дня народження контакту
class Birthday(Field):
    def __init__(self, value):
        try:
            # Перетворення даних у формат date з перевіркою на помилку
            self.value = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')

# Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Метод який додає телефон у список контактів
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Метод видалення телефону зі списку контактів
    def remove_phone(self, phone):
        p = self.find_phone(phone)
        if p:
            self.phones.remove(p)
        return p

    # Метод зміни номера телефону контакту
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return Phone(new_phone) # Валідація формату нового номеру телефону
        # Вивід помилки в разі якщо старий номер телефону не знайдено в списку контактів
        raise ValueError(f'The phone: {old_phone} not found in contact name: {self.name}')

    # Метод для пошуку номера телефона в списку контактів. Якщо не знайдено, то повертає None
    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    # Метод додавання дати народження контакту, необовʼязкове поле
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

# Клас для зберігання та управління записами
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    # Метод пошуку контакту за імʼям. Якщо імʼя не знайдено, повертає None
    def find(self, name):
        return self.data.get(name, None)

    # Метод видалення контакту за ім'ям
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            print(f'Contact name: {name} not found') # Виводить повідомлення в разі якщо імʼя не існує

    # Метод визначення контактів, у яких день народження припадає вперед на 7 робочих днів
    def get_upcoming_birthdays(self, days=7):
        today = datetime.now().date()
        birthday_list = []
        for record in self.data.values():
            if record.birthday is None:
                continue
            # Приводимо рік дати народження у відповідність до поточного
            birthday = record.birthday.value.replace(year=today.year)
            if birthday < today:
                birthday = record.birthday.value.replace(year=today.year + 1)
            # Розрахунок днів до дати дня народження контакту
            delta_days = birthday.toordinal() - today.toordinal()
            # Додаємо в список контакти у яких день народження припадає вперед на 7 робочих днів
            if delta_days <= days:
                if birthday.weekday() == 5:
                    birthday += timedelta(days=2)
                elif birthday.weekday() == 6:
                    birthday += timedelta(days=1)
                birthday_list.append({
                    'name': record.name.value,
                    'birthday': record.birthday.value.strftime('%d.%m.%Y')
                })
        return birthday_list

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())
