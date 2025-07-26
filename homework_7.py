from collections import UserDict
from datetime import datetime, timedelta

class AddressBook(UserDict):





    def find(self, name):
        return self.data.get(name)


    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"No contact with name '{name}' found.")

    def __str__(self):
        if not self.data:
            return "AddressBook is empty."
        return '\n'.join(str(record) for record in self.data.values())
    
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        end_date = today + timedelta(days=7)
        upcoming_birthday = []
        
        for record in self.data.values():
            if not record.birthday:
                continue
            
            birthday_this_year = record.birthday.value.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            elif today <= birthday_this_year <= end_date:
                congratulation_date = birthday_this_year
                if birthday_this_year.weekday() == 5:
                    congratulation_date = birthday_this_year + timedelta(days=2)
                elif birthday_this_year.weekday() == 6:
                    congratulation_date = birthday_this_year + timedelta(days=1)

            upcoming_birthday.append({
                "name": record.name.value,
                "birthday": congratulation_date.strftime("%d.%m.%Y")
            })
        return upcoming_birthday



def parse_input(user_input):
    return user_input.strip().split()



class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):

        return str(self.value)

class Name(Field):
		pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)


    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return
        raise ValueError("Phone number not found.")


    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
class Birthday(Field):
    def __init__(self, value):
        try :
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Phone {phone} not found.")

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone {old_phone} not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones_str = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)





def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
    return inner

@input_error
def add_contact(command_parts, book):
    name, phone = command_parts[1], command_parts[2]
    record = book.find(name)
    if record:
        record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
    return "Contact added."

@input_error
def change_contact(command_parts, book):
    name, old_phone, new_phone = command_parts[1], command_parts[2], command_parts[3]
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        
    else:
        return f"Contact {name} not found."
    return "Contact changed."

@input_error
def show_phone(command_parts, book):
    name = command_parts[1]
    record = book.find(name)
    if record:
        return f"Phone numbers for {name}: {', '.join(phone.value for phone in record.phones)}"
    else:
        return f"Contact {name} not found."

@input_error
def add_birthday(args, book):
    name, birthday = args[1], args[2]
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday for {name} added."
    else:
        return f"Contact {name} not found."
    
    

@input_error
def show_birthday(args, book):
    name = args[1]
    record = book.find(name)
    if record:
        return f"Birthday for {name}: {record.birthday.value}"
    else:
        return f"Contact {name} not found."

  

@input_error
def birthdays(args, book):
    bdays= book.get_upcoming_birthdays()
    if not bdays:   
        return "No upcoming birthdays in the next 7 days."
    return "\n".join([f"{bd['name']}: {bd['birthday']}" for bd in bdays])



@input_error
def hello(args, book):
    return "Hello, how can I help you?"

@input_error
def exit(args, book):
    return "Good bye!"




def show_all(book):
    return str(book)

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input(">>> ")
        command_parts = parse_input(user_input)

        if not command_parts:
            print("Invalid command.")
            continue

        command = command_parts[0].lower()
        result = ""

        if command == "add":
            result = add_contact(command_parts, book)
        elif command == "change":
            result = change_contact(command_parts, book)
        elif command == "phone":
            result = show_phone(command_parts, book)
        elif command == "birthday":
            result = show_birthday(command_parts, book)
        elif command == "add-birthday":
            result = add_birthday(command_parts, book)
        elif command == "birthdays":
            result = birthdays(command_parts, book)
        elif command == "hello":
            result = hello(command_parts, book)
        elif command in ["exit", "close"]:
            print(exit(command_parts, book))
            break
        elif command == "all":
            result = show_all(book)
        else:
            result = "Unknown command. Please try again."

        if result:
            print(result)








if __name__ == "__main__":
    main()







