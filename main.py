from models import AddressBook, Record


# Декоратор input_error для обробки помилок
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return 'You entered an incorrect name or phone! Please try again.'
        except IndexError:
            return 'Enter the name.'
        except KeyError:
            return 'Contact not found!'
        except AttributeError:
            return 'Contact not found! Please try again.'
    return inner

# Функція яка приймає рядок вводу користувача
def parse_input(user_input):
    # Повертаємо перше слово як команду та зберігаємо у змінній cmd, решту зберігаємо як список аргументів *args
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

# Функція: add [ім'я] [телефон]: Додає або новий контакт з іменем та телефонним номером,
# або телефонний номер до контакту який вже існує.
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
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
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return f'Contact "{name}" updated.'

# Функція: phone [ім'я]: Показує телефонні номери для вказаного контакту.
@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    return '\n'.join(phone.value for phone in record.phones)

# Функція: add-birthday [ім'я] [дата народження]: Додає дату народження для вказаного контакту.
@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    try:
        record.add_birthday(birthday)
    except ValueError:
        return 'Invalid date format. Use DD.MM.YYYY'
    return f'Birthday for "{name}" added.'

# Функція: show-birthday [ім'я]: Показує дату народження для вказаного контакту.
@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    return record.birthday

# Функція: birthdays: Показує дні народження на найближчі 7 днів з датами, коли їх треба привітати.
@input_error
def birthdays(args, book):
    # return book.get_upcoming_birthdays()
    pass

# Функція: all: Показує всі контакти в адресній книзі.
def show_all(args, book: AddressBook):
    if len(args) == 0:
        return book
    else:
        return 'Enter only "all".'

def main():
    # Створюємо словник контактів
    book = AddressBook()
    print('Welcome to the assistant bot!')
    while True:
        user_input = input('Enter a command: ')
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
