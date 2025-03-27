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

# Load product data
PRODUCT_NAMES = load_data_from_csv('product_names.csv')

# Define product categories with their properties
PRODUCT_CATEGORIES = [
    {
        'name': 'Electronics',
        'code': 'ELEC',
        'min_price': 100,
        'max_price': 2000,
        'min_units': 1,
        'max_units': 3
    },
    {
        'name': 'Books',
        'code': 'BOOK',
        'min_price': 10,
        'max_price': 100,
        'min_units': 1,
        'max_units': 5
    },
    {
        'name': 'Clothing',
        'code': 'CLTH',
        'min_price': 20,
        'max_price': 200,
        'min_units': 1,
        'max_units': 4
    },
    {
        'name': 'Home & Garden',
        'code': 'HOME',
        'min_price': 50,
        'max_price': 500,
        'min_units': 1,
        'max_units': 3
    },
    {
        'name': 'Sports',
        'code': 'SPRT',
        'min_price': 30,
        'max_price': 300,
        'min_units': 1,
        'max_units': 4
    }
]

def generate_cc_number():
    """Generate a random credit card number."""
    prefix = random.choice(['4', '5', '3'])  # Visa, Mastercard, Amex
    if prefix == '3':
        length = 15
    else:
        length = 16
    remaining_digits = ''.join(random.choices(string.digits, k=length-1))
    return f"{prefix}{remaining_digits}"

def generate_transaction(customer_id, should_have_error=False):
    """Generate a single transaction."""
    category = random.choice(PRODUCT_CATEGORIES)
    product_name = random.choice(PRODUCT_NAMES)
    units = random.randint(category['min_units'], category['max_units'])
    price_per_unit = round(random.uniform(category['min_price'], category['max_price']), 2)
    
    # Calculate correct total first
    correct_total = round(units * price_per_unit, 2)
    
    # If this transaction should have an error, inflate the total by 20-50%
    if should_have_error:
        error_multiplier = 1 + random.uniform(0.2, 0.5)  # 20-50% increase
        total = round(correct_total * error_multiplier, 2)
    else:
        total = correct_total
    
    # Generate a random date in the last 30 days
    days_ago = random.randint(0, 30)
    purchase_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
    
    order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    product_code = f"{category['code']}-{random.randint(100, 999)}"
    cc_number = generate_cc_number()
    
    return f"{customer_id},{order_id},{purchase_date},{total},{units},{product_code},{category['name']},{cc_number},{price_per_unit}\n"

def generateTransactions(customer_id, max_transactions, error_rate=0.0):
    """Generate multiple transactions for a customer."""
    num_transactions = random.randint(1, max_transactions)
    transactions = ""
    
    # Convert error_rate from percentage to decimal
    error_rate = error_rate / 100.0
    
    # Decide if this customer's transactions should have errors
    should_have_errors = random.random() < error_rate
    
    for _ in range(num_transactions):
        transactions += generate_transaction(customer_id, should_have_errors)
    
    return transactions 