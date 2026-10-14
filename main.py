from models import AddressBook, Record


# Декоратор input_error для обробки помилок
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e) # Текст помилки береться з models.py
        except KeyError as e:
            return f'Contact "{e.args[0]}" not found.'
        except IndexError:
            return 'Not enough arguments. Please enter all required values.'
    return inner

# Функція яка приймає рядок вводу користувача
def parse_input(user_input):
    # Повертаємо перше слово як команду та зберігаємо у змінній cmd, решту зберігаємо як список аргументів *args
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

# Допоміжна функція яка знаходить контакт, а якщо його немає, піднімає KeyError
def get_record(book: AddressBook, name):
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    return record

# Функція: add [ім'я] [телефон]: Додає або новий контакт з іменем та телефонним номером,
# або телефонний номер до контакту який вже існує.
@input_error
def add_contact(args, book: AddressBook):
    name = args[0]
    phone = args[1]
    record = book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return f'Contact "{name}" added.'
    # Перевірка якщо телефон вже привʼязаний до контакта
    if record.find_phone(phone):
        return f'The phone: "{phone}" is already in use.'
    record.add_phone(phone)
    return f'Contact "{name}" updated.'

# Функція: change [ім'я] [старий телефон] [новий телефон]: Змінює телефонний номер для вказаного контакту.
@input_error
def change_contact(args, book: AddressBook):
    name = args[0]
    old_phone = args[1]
    new_phone = args[2]
    record = get_record(book, name)
    record.edit_phone(old_phone, new_phone)
    return f'Contact "{name}" updated.'

# Функція: phone [ім'я]: Показує телефонні номери для вказаного контакту.
@input_error
def show_phone(args, book: AddressBook):
    record = get_record(book, args[0])
    return '\n'.join(phone.value for phone in record.phones)

# Функція: add-birthday [ім'я] [дата народження]: Додає дату народження для вказаного контакту.
@input_error
def add_birthday(args, book: AddressBook):
    name = args[0]
    birthday = args[1]
    record = get_record(book, name)
    record.add_birthday(birthday)
    return f'Birthday for "{name}" added.'

# Функція: show-birthday [ім'я]: Показує дату народження для вказаного контакту.
@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = get_record(book, name)
    if record.birthday is None:
        return f'The birthday for "{name}" does not exist. Please add birthday for "{name}".'
    return record.birthday

# Функція: birthdays: Показує дні народження на найближчі 7 днів з датами, коли їх треба привітати.
@input_error
def birthdays(args, book: AddressBook):
    if len(args) != 0:
        return 'Enter only command "birthdays".'
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return 'No birthdays in the next 7 days.'
    return '\n'.join(f'{item['name']}: {item['birthday']}' for item in upcoming)

# Функція: all: Показує всі контакти в адресній книзі.
def show_all(args, book: AddressBook):
    if len(args) != 0:
        return 'Enter only command "all".'
    return book

def main():
    book = AddressBook()
    print('Welcome to the assistant bot!')
    while True:
        user_input = input('Enter a command: ')
        # Перевірка на ввід команди без тексту
        if not user_input.strip():
            continue
        # Змінна command отримує перше введене слово та стає командою, а змінна args списком з усіх інших значень
        command, args = parse_input(user_input)
        # Команда close або exit зупиняємо цикл і виходить з програми
        if command in ['close', 'exit']:
            print('Good bye!')
            break

        # Команди програми
        elif command == 'hello':
            print('How can I help you?')
        elif command == 'add':
            print(add_contact(args, book))
        elif command == 'change':
            print(change_contact(args, book))
        elif command == 'phone':
            print(show_phone(args, book))
        elif command == 'all':
            print(show_all(args, book))
        elif command == 'add-birthday':
            print(add_birthday(args, book))
        elif command == 'show-birthday':
            print(show_birthday(args, book))
        elif command == 'birthdays':
            print(birthdays(args, book))
        else:
            print('Invalid command.')


if __name__ == '__main__':
    main()

