from main import AddressBook, Record


# Декоратор input_error для обробки помилок
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return 'Give me name and phone please.'
        except IndexError:
            return 'Enter the name.'
        except KeyError:
            return 'Contact not found!'
    return inner

# Функція яка приймає рядок вводу користувача
def parse_input(user_input):
    # Повертаємо перше слово як команду та зберігаємо у змінній cmd, решту зберігаємо як список аргументів *args
    cmd, *args = user_input.split(' ')
    # Видаляємо зайві пробіли та перетворюємо на нижній регістр
    cmd = cmd.strip().lower()
    return cmd, args

# Функція додавання нового контакту
@input_error # Декоратор обробки помилок
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = 'Contact updated.'
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = 'Contact added.'
    if phone:
        record.add_phone(phone)
    return message

# Функція зміни номера телефону контакту зі списку контактів
@input_error # Декоратор обробки помилок
def change_contact(args, contacts):
    name, phone = args
    # Перевірка існування імені в списку контактів
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return 'Contact updated!'

# Функція виведення номера телефону контакту
@input_error # Декоратор обробки помилок
def show_phone(args, contacts):
    # Обмеження на введення більше ніж одного значення
    if len(args) == 1:
        name = args[0]
        return contacts[name]
    else:
        raise IndexError

@input_error
def add_birthday(args, book):
    name, birthday = args
    book[name] = birthday
    return 'Birthday added!'

@input_error
def show_birthday(args, book):
    pass



@input_error
def birthdays(args, book):
    # return book.get_upcoming_birthdays()
    pass





# Функція виведення всіх збережених контактів
def show_all(args, contacts):
    # Команда виведення всіх збережених контактів має складатись з одного значення
    if len(args) == 0:
        return '\n'.join(f'{name}: {phone}' for name, phone in contacts.items())
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
