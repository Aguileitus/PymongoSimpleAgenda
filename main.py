"""Simple Python script to interact with MongoDB"""

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

client = MongoClient()
db: Database = client['agenda']
db_contacts: Collection = db['contacts']

# Keys constants
ID_KEY = "_id"
NAME_KEY = "name"
AGE_KEY = "age"
PHONE_KEY = "phone"
EMAIL_KEY = "email"

def create_contact() -> None:
    """Stores the new contact in the database"""
    _id = None
    name = None
    age = None
    phone = None
    email = None

    while True:
        try:
            _id = int(input("Enter ID: "))
            break
        except ValueError:
            print("ID must be a number. Please try again.")

    name = input("Enter name: ").lower()

    while True:
        try:
            age = int(input("Enter age: "))
            break
        except ValueError:
            print("Age must be a number. Please try again.")
    phone = input("Enter phone number: ").lower()
    email = input("Enter email: ").lower()

    try:
        result = db_contacts.insert_one(
            {
                ID_KEY: _id,
                NAME_KEY: name,
                AGE_KEY: age,
                PHONE_KEY: phone,
                EMAIL_KEY: email
            }
        )
        # insert_one() returns a InsertOneResult object that contains:
        # acknowledged: Is this the result of a acknowledged write operation?
        # inserted_id: The inserted document's _id

        if result.acknowledged:
            print(f"Successfully created with id: {result.inserted_id}")
        else:
            print("Insert not acknowledged.")
    except DuplicateKeyError:
        print(f"The id {_id} already exists, please enter an unique ID.")
# end create_contact

def print_contact(contact: dict) -> None:
    """Prints one contact"""
    print(f"ID:    {contact[ID_KEY]}\n"
          f"Name:  {contact[NAME_KEY].capitalize()}\n"
          f"Age:   {contact[AGE_KEY]}\n"
          f"Phone: {contact[PHONE_KEY]}\n"
          f"Email: {contact[EMAIL_KEY]}")

def search_one() -> None:
    """Searches one contact by name and prints it"""
    name = input("Enter name to search: ").lower()
    contact = db_contacts.find_one({NAME_KEY: name})
    # find_one() returns the contact as a dictionary or None if the search gave no results

    if contact:
        print("-----------------------------")
        print_contact(contact)
        print("-----------------------------")
    else:
        print(f"Contact {name.capitalize()} not found, please try again.")

def show_all() -> None:
    """Searches and prints all contacts stored"""
    if db_contacts.count_documents({}) == 0:
        print("-----------------------------")
        print("No data found.")
        print("-----------------------------")
        return

    contacts = db_contacts.find()
    # find() does not result a list of contacts but a DB cursor that can be iterated
    # to get contact by contact.
    for contact in contacts:
        print("-----------------------------")
        print_contact(contact)

    print("-----------------------------")

def update() -> None:
    """Searches and updates one attribute of a contact"""
    name = input("Enter name to search: ").lower()

    contact = db_contacts.find_one({NAME_KEY: name})
    # find_one() returns the contact as a dictionary or None if the search gave no results

    if not contact:
        print(f"Contact {name.capitalize()} not found, please try again.")
        return

    print("-------------------")
    print_contact(contact)
    print("-------------------")

    while True:
        field = input("What field do you want to update? ").lower().strip()
        if field == "id":
            print("You can't modify the ID. (It's immutable!)")
            continue

        if field in ["phone number"]:
            field = PHONE_KEY

        if field in ["e-mail"]:
            field = EMAIL_KEY

        if field not in [NAME_KEY, AGE_KEY, PHONE_KEY, EMAIL_KEY]:
            print(f"Field {field} does not exist.")
            continue

        break

    while True:
        value = input("Enter the value: ").lower()

        if field in[AGE_KEY]:
            try:
                value = int(value)
                break
            except ValueError:
                print("Age must be a number. Please try again.")

    result = db_contacts.update_one({ID_KEY: contact[ID_KEY]}, {"$set": {field: value}})
    # update_one() returns a UpdateResult object that contains:
    # acknowledged: Is this the result of a acknowledged write operation?
    # matched_count: The number of documents matched for this update
    # raw_result: The raw result document returned by the server
    # upserted_id: The _id of the inserted document if an upsert took place}

    if result.acknowledged:
        print(f"Successfully updated. [{result.matched_count}] [{result.upserted_id}]")
        print(f"Raw result: {result.raw_result}")
    else:
        print("Insert not acknowledged.")
# end update

def delete() -> None:
    """Deletes a contact from the DB"""
    name = input("Enter name to delete: ")
    contact = db_contacts.find_one({NAME_KEY: name})
    # find_one() returns the contact as a dictionary or None if the search gave no results

    if not contact:
        print(f"Contact {name.capitalize()} not found, please try again.")
        return

    print("-------------------")
    print_contact(contact)
    print("-------------------")

    if input("Are you sure you want to delete this contact? (Y/N) > ").lower() in ["y", "yes"]:
        db_contacts.delete_one({ID_KEY: contact[ID_KEY]})
        print("Contact deleted.")

# Options constants
EXIT_OPT = 0
CREATE_OPT = 1
SEARCH_OPT = 2
SHOW_ALL_OPT = 3
UPDATE_OPT = 4
DELETE_OPT = 5

def main():
    """Runs the menu."""
    while True:
        print("Menu:")
        print("  0. Exit")
        print("  1. Create")
        print("  2. Search")
        print("  3. Show All")
        print("  4. Update")
        print("  5. Delete")

        try:
            opt = int(input("Select option> "))
        except ValueError:
            print("*** The option must be a number. Please try again. ***")
            continue

        if opt == EXIT_OPT:
            break
        if opt == CREATE_OPT:
            create_contact()
        elif opt == SEARCH_OPT:
            search_one()
        elif opt == SHOW_ALL_OPT:
            show_all()
        elif opt == UPDATE_OPT:
            update()
        elif opt == DELETE_OPT:
            delete()
        else:
            print("*** Not a valid option. Please try again. ***")

    print("Thanks for using this app! Cya!")


if __name__ == "__main__":
    main()
