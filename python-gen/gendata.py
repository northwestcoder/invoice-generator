import time
import os
import csv
import json
import random
import argparse

import people
from invoice_generator import generate_invoice

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate synthetic customer data and invoices with optional errors.')
    
    parser.add_argument(
        '--num-customers',
        type=int,
        default=10,
        help='Number of customers to generate (default: 10)'
    )
    
    parser.add_argument(
        '--transactions-per-customer',
        type=int,
        default=3,
        help='Number of transactions to generate per customer (default: 3)'
    )
    
    parser.add_argument(
        '--error-rate',
        type=float,
        default=0,
        help='Percentage of invoices that should contain calculation errors (0-100)'
    )

    parser.add_argument(
        '--dirty-rate',
        type=float,
        default=0,
        help='Percentage of visual distortions to apply to PDFs (0-100). Adds realistic imperfections like misalignments, ink issues, and stains.'
    )
    
    parser.add_argument(
        '--include-headers',
        action='store_true',
        default=True,
        help='Include headers in output CSV files (default: True)'
    )
    
    parser.add_argument(
        '--no-headers',
        action='store_false',
        dest='include_headers',
        help='Do not include headers in output CSV files'
    )
    
    parser.add_argument(
        '--generate-transactions',
        action='store_true',
        default=True,
        help='Generate transaction data (default: True)'
    )
    
    parser.add_argument(
        '--no-transactions',
        action='store_false',
        dest='generate_transactions',
        help='Do not generate transaction data'
    )
    
    args = parser.parse_args()
    
    # Validate numeric parameters
    if args.num_customers <= 0:
        parser.error("Number of customers must be greater than 0")
    
    if args.transactions_per_customer <= 0:
        parser.error("Number of transactions per customer must be greater than 0")
    
    if args.transactions_per_customer > 15:
        parser.error("Maximum number of transactions per customer is 15")
    
    if not 0 <= args.error_rate <= 100:
        parser.error("Error rate must be between 0 and 100")
    
    return args

# Start timing the data generation
t_start = time.time()

# Parse command line arguments
args = parse_arguments()

# Data generation configuration
INCLUDE_CSV_HEADERS = args.include_headers
NUM_CUSTOMERS = args.num_customers
GENERATE_TRANSACTIONS = args.generate_transactions
TRANSACTIONS_PER_CUSTOMER = args.transactions_per_customer

# Print configuration
print("\nData Generation Configuration:")
print(f"Number of customers: {NUM_CUSTOMERS}")
print(f"Include CSV headers: {INCLUDE_CSV_HEADERS}")
print(f"Generate transactions: {GENERATE_TRANSACTIONS}")
if GENERATE_TRANSACTIONS:
    print(f"Transactions per customer: {TRANSACTIONS_PER_CUSTOMER}")
print(f"Invoice error rate: {args.error_rate}%")
print(f"PDF distortion rate: {args.dirty_rate}%\n")

# Generate the data
newdata = people.createData(
    INCLUDE_CSV_HEADERS,
    NUM_CUSTOMERS,
    GENERATE_TRANSACTIONS,
    TRANSACTIONS_PER_CUSTOMER,
    args.error_rate  # Pass the error rate percentage
)

# Create output directories if they don't exist
output_dir = os.path.dirname(__file__)
pdf_dir = os.path.join(output_dir, 'pdf_output')
os.makedirs(pdf_dir, exist_ok=True)

# Write people data
output_people_path = os.path.join(output_dir, 'output_people.csv')
with open(output_people_path, 'w') as f:
    f.write(newdata[0])
    print("Finished writing people data")

# Write and process transactions
output_transactions_path = os.path.join(output_dir, 'output_transactions.csv')
with open(output_transactions_path, 'w') as f:
    f.write(newdata[1])
    print("Finished writing transaction data")

output_social_path = os.path.join(output_dir, 'output_social.csv')
with open(output_social_path, 'w') as f:
    f.write(newdata[2])
    print("Finished writing social interaction data")

# Now generate invoices for each person
print(f"\nGenerating {NUM_CUSTOMERS} invoices with {args.error_rate}% error rate...")

# Read people data
people_data = []
with open(output_people_path, 'r') as f:
    reader = csv.DictReader(f)
    people_data = list(reader)

# Read transactions data
transactions_data = []
with open(output_transactions_path, 'r') as f:
    reader = csv.DictReader(f)
    transactions_data = list(reader)

# Group transactions by customer_id
transactions_by_customer = {}
for trans in transactions_data:
    customer_id = trans['customer_id']
    if customer_id not in transactions_by_customer:
        transactions_by_customer[customer_id] = []
    transactions_by_customer[customer_id].append(trans)

# Track number of invoices with errors
error_count = 0
total_invoices = 0

# Generate an invoice for each person
for person in people_data:
    customer_id = person['customer_id']
    if customer_id in transactions_by_customer:
        total_invoices += 1
        if generate_invoice(person, transactions_by_customer[customer_id], error_rate=args.error_rate, dirty_rate=args.dirty_rate):
            error_count += 1

print(f"\nGenerated {total_invoices} invoices, {error_count} ({(error_count/total_invoices)*100:.1f}%) contain calculation errors.")

t_end = time.time()
total_time = t_end - t_start
print(f"\nTotal execution time: {total_time:.2f} seconds") 