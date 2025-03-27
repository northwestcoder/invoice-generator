# Thunk Data Generator

A Python-based tool for generating synthetic customer data and invoices with realistic imperfections. This tool is designed to create datasets that include both mathematical errors in calculations and visual distortions in PDF outputs, making it useful for testing data validation and OCR systems.

## Features

### Data Generation
- Generates synthetic customer profiles with realistic names and addresses
- Creates transaction records with varying product categories and quantities
- Supports configurable error rates for mathematical calculations
- Generates social interaction data between customers

### Invoice Generation
- Creates PDF invoices with professional layouts
- Supports multiple font styles and sizes
- Includes company logos and branding elements
- Generates unique invoice numbers and customer IDs

### PDF Distortions
The tool can apply various realistic distortions to PDF outputs, including:

1. Paper Texture Effects
   - Subtle paper grain simulation
   - Random texture variations
   - Light color variations

2. Coffee/Tea Stains
   - Realistic stain shapes with natural edges
   - Multiple color layers for depth
   - Splatter effects around main stains
   - Varying opacity levels

3. Ink Bleeding
   - Natural ink spread patterns
   - Multiple layers for depth
   - Varying opacity and color
   - Irregular edge patterns

4. Printer Artifacts
   - Wavy vertical lines
   - Fading effects at page edges
   - Varying line thickness
   - Subtle color variations

5. Paper Damage
   - Fold and crease effects
   - Shadow lines for depth
   - Both horizontal and vertical creases
   - Varying opacity levels

6. Page Alignment
   - Subtle page skew
   - Random rotation angles
   - Natural-looking misalignment

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/thunk-datagen.git
cd thunk-datagen
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python gendata.py --num-customers 100 --transactions-per-customer 10
```

### Advanced Options
```bash
python gendata.py \
    --num-customers 100 \
    --transactions-per-customer 10 \
    --error-rate 50 \
    --dirty-rate 50 \
    --include-headers \
    --generate-transactions
```

### Command Line Arguments
- `--num-customers`: Number of customers to generate (default: 10)
- `--transactions-per-customer`: Number of transactions per customer (default: 3)
- `--error-rate`: Percentage of invoices with calculation errors (0-100)
- `--dirty-rate`: Percentage of PDFs with visual distortions (0-100)
- `--include-headers`: Include headers in CSV files (default: True)
- `--generate-transactions`: Generate transaction data (default: True)

## Output Files

1. `output_people.csv`: Customer profile data
2. `output_transactions.csv`: Transaction records
3. `output_social.csv`: Social interaction data
4. `pdf_output/`: Directory containing generated PDF invoices

## PDF Distortion Features

The PDF distortion system applies various effects with configurable probabilities:

### Base Effects (Always Applied)
- Paper texture simulation
- Random ink bleeding spots

### Conditional Effects (Based on dirty_rate)
- Coffee/tea stains (40% chance)
- Printer line artifacts (30% chance)
- Paper folds/creases (30% chance)
- Page skew (variable angle)

### Effect Parameters
- All effects use natural color palettes
- Opacity levels are carefully tuned for realism
- Effects are layered for depth and authenticity
- Random variations ensure unique outputs

## Requirements

- Python 3.8+
- reportlab==4.0.4
- pdfkit==1.0.0
- python-dateutil==2.8.2
- Pillow==10.0.0
- Faker==24.2.0
- names==0.3.0
- InvoiceGenerator>=1.1.0
- qrcode>=7.3.1
- numpy>=1.24.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.