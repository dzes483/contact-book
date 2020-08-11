from __future__ import print_function, unicode_literals
from sqlalchemy import create_engine, Sequence, Column, Integer, String, or_, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from PyInquirer import prompt, print_json



START_MENU_CHOICES = ['V', 'A', 'D', 'S', 'U', 'X']

start_menu = ("[V] -- View all entries\n"
              "[A] -- Add new contact\n"
              "[D] -- Delete a contact\n"
              "[S] -- Search the address book\n"
              "[U] -- Update contact information\n"
              "[X] -- Exit the program\n")

print('---------------Contact Book---------------')
print(start_menu)


# Connect to the engine.
engine = create_engine('sqlite:///contact_book.db', echo=False)

# Declare a mapping
Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'

    fields = ['last_name', 'first_name', 'address_line_1', 'address_line_2',
             'city', 'state', 'zipcode', 'country', 'phone_number', 'email']

    id = Column(Integer, Sequence('contact_id_seq'), primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    address_line_1 = Column(String)
    address_line_2 = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(String)
    country = Column(String)


    def address(self):
        return self.address_line_1 + '\n' + self.address_line_2 + '\n' + \
                self.city + ', ' + self.state + ' ' + self.zipcode + \
                '\n' + self.country

    def __repr__(self):
        return self.last_name + ', ' + self.first_name

# Create a schema
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

# Instantiate when you need to connect with the database
session = Session()

# def check_choice(menu, options):
#     """"Validates a user's choice among menu options"""
#     while True:
#         choice = input()
#         if len(choice) > 1:
#             print('Please enter only one letter.')
#             print(menu)
#             continue
#         elif choice.upper() not in options or choice.isalpha() == False:
#             print('Invalid selection. Please choose an option from the below: ')
#             print(menu)
#             continue
#         else:
#             break
#     return choice




def add_contact():
    """
    Save a new contact to the database.
    """
    contact_fields = [
        {
        'type': 'input',
        'name': 'first_name',
        'message': 'First Name: ',
        },
        {
        'type': 'input',
        'name': 'last_name',
        'message': 'Last Name: ',
        },
        {
        'type': 'input',
        'name': 'email',
        'message': 'Email Address: ',
        },
        {
        'type': 'input',
        'name': 'phone_number',
        'message': 'Phone Number: ',
        },
        {
        'type': 'input',
        'name': 'address_line_1',
        'message': 'Address Line 1: ',
        },
        {
        'type': 'input',
        'name': 'address_line_2',
        'message': 'Address Line 2: ',
        },
        {
        'type': 'input',
        'name': 'city',
        'message': 'City: ',
        },
        {
        'type': 'input',
        'name': 'state',
        'message': 'State: ',
        },
        {
        'type': 'input',
        'name': 'zipcode',
        'message': 'Zipcode: ',
        },
        {
        'type': 'input',
        'name': 'country',
        'message': 'Country: ',
        },
    ]
    answers = prompt(contact_fields)
    print(answers)
    new_contact = Contact(first_name=answers['first_name'],
                          last_name=answers['last_name'],
                          email=answers['email'],
                          phone_number=answers['phone_number'],
                          address_line_1=answers['address_line_1'],
                          address_line_2=answers['address_line_2'],
                          city=answers['city'],
                          state=answers['state'],
                          zipcode=answers['zipcode'],
                          country=answers['country'])
    print(new_contact.first_name)
    session.add(new_contact)


def search_contacts():
    search_field = [
        {
        'type': 'input',
        'name': 'search',
        'message': 'Enter a name: ',
        },
    ]
    search_prompt = prompt(search_field)
    search_query = search_prompt['search']
    print(search_query)

    search_results = session.query(Contact).filter(
                     or_(
                     (Contact.last_name.ilike(f'%{search_query}%')),
                     (Contact.first_name.ilike(f'%{search_query}%'))
                ))
    return search_results
    print("Search done.")

choice = input()


# View all entries
if choice.upper() == 'V':
    for instance in session.query(Contact).order_by(Contact.last_name):
        print(instance.last_name + ', ' + instance.first_name + ' | ' +
              instance.phone_number + ' | ' + instance.email)

# Add a new contact

elif choice.upper() == 'A':
    add_contact()
    while True:
        add_another = [
            {
            'type': 'confirm',
            'message': 'Would you like to add another contact?',
            'name': 'add_another',
            'default': True,
            },
        ]
        answer = prompt(add_another)
        if answer['add_another'] == False:
            break
        else:
            add_contact()
    session.commit()

# Delete a contact
elif choice.upper() == 'D':
    search_contacts()

# Search the contact book
elif choice.upper() == 'S':
    search_results = search_contacts()
    print("RESULT:")
    print(*search_results.all())

    # TODO: Present fields to fill in
    # session.query(Contact).filter_by()

# Update contact information
elif choice == 'U':
    pass

# Exit the program.
elif choice == 'X':
    pass