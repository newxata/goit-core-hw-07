from collections import UserDict
from datetime import datetime, timedelta, date


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
            # Перевірка формату: якщо рядок не відповідає DD.MM.YYYY, виникне ValueError
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')
        super().__init__(value)

# Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Метод який додає телефон у список контактів
    def add_phone(self, phone):
        if self.find_phone(phone):
            return
        self.phones.append(Phone(phone))

    # Метод видалення телефону зі списку контактів
    def remove_phone(self, phone):
        p = self.find_phone(phone)
        # Перевірка на випадок якщо номеру телефону немає в списку контактів
        if p is None:
            raise ValueError(f'The phone: {phone} not found in contact name: {self.name}')
        self.phones.remove(p)
        return p

    # Метод зміни номера телефону контакту
    def edit_phone(self, old_phone, new_phone):
        p = self.find_phone(old_phone)
        # Перевірка на випадок якщо номеру телефону немає в списку контактів
        if p is None:
            raise ValueError(f'The phone: {old_phone} not found in contact name: {self.name}')
        p.value = Phone(new_phone).value

    # Метод для пошуку номера телефона в списку контактів. Якщо не знайдено, то повертає None
    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    # Метод додавання дати народження контакту, необовʼязкове поле
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        result = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        if self.birthday:
            result += f", birthday: {self.birthday.value}"
        return result

# Клас для зберігання та управління записами
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    # Метод пошуку контакту за імʼям
    def find(self, name):
        return self.data.get(name)

    # Метод видалення контакту за ім'ям
    def delete(self, name):
        del self.data[name]

    # Метод який змінює рік у невисокосному році, та для дня народження 29.02 повертає 28.02
    @staticmethod
    def _replace_year(d: date, year: int) -> date:
        try:
            return d.replace(year=year)
        except ValueError:
            return d.replace(year=year, day=28)

    # Метод визначення контактів, у яких день народження припадає вперед на 7 робочих днів
    def get_upcoming_birthdays(self, days=7):
        today = datetime.now().date()
        birthday_list = []
        for record in self.data.values():
            if record.birthday is None:
                continue
            # Перетворюємо рядок дати народження в обʼєкт date
            birth_date = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
            # Приводимо рік дати народження у відповідність до поточного
            birthday = self._replace_year(birth_date, today.year)
            if birthday < today:
                birthday = self._replace_year(birth_date, today.year + 1)
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
                    'birthday': birthday.strftime('%d.%m.%Y')
                })
        return birthday_list

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

