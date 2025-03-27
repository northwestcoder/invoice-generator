# Python Invoice Data Generator

This is the Python version of the synthetic data generator for invoices. It generates customer data, transactions, and PDF invoices with optional calculation errors.

## Prerequisites

- Python 3.8 or higher
- Required Python packages (install using pip):
  ```bash
  pip install -r requirements.txt
  ```

## Usage

Run the script from the command line:

```bash
python gendata.py [options]
```

### Command Line Options

- `--num-customers` or `-n`: Number of customers to generate (default: 10)
- `--transactions-per-customer` or `-t`: Number of transactions per customer (default: 3)
- `--error-rate` or `-e`: Percentage of invoices that should contain calculation errors (default: 4)
- `--include-headers`: Include headers in output CSV files (default: True)
- `--generate-transactions`: Generate transaction data (default: True)

### Example

```bash
python gendata.py --num-customers 5 --transactions-per-customer 3 --error-rate 10
```

## Output

The script generates the following files:

1. `output_people.csv`: Contains generated customer data
2. `output_transactions.csv`: Contains generated transaction data
3. PDF invoices in the `pdf_output` directory (one per customer)

## Directory Structure

```
python-gen/
├── inputs/           # Input data files
├── pdf_output/       # Generated PDF invoices
├── gendata.py        # Main script
├── invoice_generator.py
├── requirements.txt
└── README.md
``` 