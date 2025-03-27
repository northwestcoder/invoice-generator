import random
import string
import csv
from datetime import datetime, timedelta
import os

def load_data_from_csv(filename):
    """Load data from a CSV file and return as a list."""
    data = []
    with open(os.path.join('inputs', filename), 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # Skip empty rows
                data.append(row[0])  # Assuming single column
    return data

# Load input data
FIRST_NAMES_MALE = load_data_from_csv('firstnames_male.csv')
FIRST_NAMES_FEMALE = load_data_from_csv('firstnames_female.csv')
LAST_NAMES = load_data_from_csv('lastnames.csv')
STREETS = load_data_from_csv('streetnames.csv')
CITIES = load_data_from_csv('cities.csv')
STATES = load_data_from_csv('states.csv')
JOBS = load_data_from_csv('jobs.csv')

def generate_id():
    """Generate a random 16-character alphanumeric ID."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

def generate_phone():
    """Generate a random phone number in XXX-XXX-XXXX format."""
    return f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"

def generate_email(first_name, last_name):
    """Generate an email address from first and last name."""
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'example.com']
    separators = ['', '.', '_']
    separator = random.choice(separators)
    domain = random.choice(domains)
    return f"{first_name.lower()}{separator}{last_name.lower()}@{domain}"

def generate_zip():
    """Generate a random 5-digit ZIP code."""
    return f"{random.randint(10000,99999)}"

def generate_person():
    """Generate a single person's data."""
    gender = random.choice(['M', 'F'])
    first_name = random.choice(FIRST_NAMES_MALE if gender == 'M' else FIRST_NAMES_FEMALE)
    last_name = random.choice(LAST_NAMES)
    street = f"{random.randint(100,9999)} {random.choice(STREETS)}"
    city = random.choice(CITIES)
    state = random.choice(STATES)
    zip_code = generate_zip()
    phone = generate_phone()
    email = generate_email(first_name, last_name)
    job = random.choice(JOBS)
    customer_id = generate_id()

    return {
        'customer_id': customer_id,
        'first_name': first_name,
        'last_name': last_name,
        'street': street,
        'city': city,
        'state': state,
        'zip': zip_code,
        'phone': phone,
        'email': email,
        'job': job
    }

def createData(include_headers=True, num_customers=10, generate_transactions=True, transactions_per_customer=3, error_rate=0.0):
    """Generate customer data and optionally transactions."""
    # Generate people data
    people = [generate_person() for _ in range(num_customers)]
    
    # Create CSV content for people
    people_csv = ""
    if include_headers:
        people_csv = "customer_id,first_name,last_name,street,city,state,zip,phone,email,job\n"
    
    for person in people:
        people_csv += f"{person['customer_id']},{person['first_name']},{person['last_name']},{person['street']},"
        people_csv += f"{person['city']},{person['state']},{person['zip']},{person['phone']},{person['email']},{person['job']}\n"
    
    # Generate transactions if requested
    transactions_csv = ""
    if generate_transactions:
        if include_headers:
            transactions_csv = "customer_id,orderid,purchasedatetime,transactiontotal,numberofitems,productcode,productcategory,cc_number,price_per_unit\n"
        
        # Import here to avoid circular import
        from transactions import generateTransactions
        for person in people:
            transactions_csv += generateTransactions(person['customer_id'], transactions_per_customer, error_rate)
    
    # Generate social interactions only if we have more than one person
    social_csv = ""
    if include_headers:
        social_csv = "interaction_id,person1_id,person2_id,interaction_type,interaction_date\n"
    
    # Generate some random social interactions between people
    if num_customers > 1:
        for _ in range(num_customers * 2):  # Generate twice as many interactions as people
            person1 = random.choice(people)
            person2 = random.choice([p for p in people if p['customer_id'] != person1['customer_id']])
            
            interaction_types = ['email', 'phone', 'meeting', 'video_call']
            interaction_type = random.choice(interaction_types)
            
            # Generate a random date in the last 30 days
            days_ago = random.randint(0, 30)
            interaction_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
            
            social_csv += f"{generate_id()},{person1['customer_id']},{person2['customer_id']},{interaction_type},{interaction_date}\n"
    
    return people_csv, transactions_csv, social_csv 