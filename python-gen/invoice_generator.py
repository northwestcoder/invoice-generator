import os
from datetime import datetime
from decimal import Decimal
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, Polygon
import random
import csv
import io
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
from pdf_distortions import PDFDistorter
import tempfile

# Define available fonts and colors
FONTS = ['Helvetica', 'Times-Roman', 'Courier', 'Helvetica-Bold', 'Times-Bold']
TEXT_COLORS = {
    'black': colors.black,
    'dark grey': colors.Color(0.2, 0.2, 0.2),
    'dark red': colors.Color(0.6, 0, 0),
    'dark green': colors.Color(0, 0.4, 0)
}
FONT_SIZES = [9, 10, 11, 12]

LOGO_TYPES = ['geometric', 'abstract', 'initials']

def generate_random_logo(width=30, height=30):
    """Generate a random logo as a ReportLab Drawing object."""
    drawing = Drawing(width, height)
    logo_type = random.choice(LOGO_TYPES)
    
    # Choose two contrasting colors
    main_color = random.choice([
        colors.Color(0.1, 0.3, 0.5),  # Blue
        colors.Color(0.5, 0.1, 0.1),  # Red
        colors.Color(0.1, 0.5, 0.2),  # Green
        colors.Color(0.4, 0.2, 0.5),  # Purple
        colors.Color(0.5, 0.3, 0.1),  # Orange
    ])
    accent_color = colors.Color(
        min(1, main_color.red + 0.3),
        min(1, main_color.green + 0.3),
        min(1, main_color.blue + 0.3)
    )
    
    if logo_type == 'geometric':
        # Create a geometric pattern
        shapes = []
        # Background shape
        shapes.append(Circle(width/2, height/2, width/2.5, fillColor=main_color))
        # Overlay shape
        shapes.append(Polygon(
            points=[
                width/2, height,
                0, height/3,
                width/2, 0,
                width, height/3
            ],
            fillColor=accent_color
        ))
        
    elif logo_type == 'abstract':
        # Create abstract lines
        shapes = []
        # Background
        shapes.append(Rect(0, 0, width, height, fillColor=main_color))
        # Random lines
        for _ in range(5):
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = random.randint(0, width), random.randint(0, height)
            shapes.append(Line(x1, y1, x2, y2, strokeColor=accent_color, strokeWidth=2))
            
    else:  # initials
        # Create abstract letter-like shapes
        shapes = []
        # Background
        shapes.append(Circle(width/2, height/2, width/2, fillColor=main_color))
        # Vertical line
        shapes.append(Rect(width/3, height/4, width/6, height/2, fillColor=accent_color))
        # Horizontal line
        shapes.append(Rect(width/4, height/2.2, width/2, height/6, fillColor=accent_color))
    
    for shape in shapes:
        drawing.add(shape)
    
    return drawing

def get_random_style():
    """Get random font, color, and size for the invoice."""
    base_size = random.choice(FONT_SIZES)
    return {
        'font': random.choice(FONTS),
        'color': random.choice(list(TEXT_COLORS.values())),
        'size': {
            'base': base_size,
            'header': base_size + 2,  # Header slightly larger
            'small': base_size - 2    # Small text slightly smaller
        }
    }

def load_data_from_csv(filename):
    """Load data from a CSV file and return as a list."""
    with open(f'./inputs/{filename}', 'r') as f:
        return [line.strip() for line in f.readlines()]

# Cache the data to avoid reading files multiple times
COMPANIES = load_data_from_csv('companies.csv')
STREETS = load_data_from_csv('streetnames.csv')
CITIES = load_data_from_csv('cities.csv')
STATES = load_data_from_csv('states.csv')
POSTAL_CODES = load_data_from_csv('postalcodes.csv')

def get_random_company():
    """Get a random company name."""
    return random.choice(COMPANIES)

def get_random_address():
    """Get a random address."""
    return {
        'street': f"{random.randint(100, 9999)} {random.choice(STREETS)}",
        'city': random.choice(CITIES),
        'state': random.choice(STATES),
        'postal_code': random.choice(POSTAL_CODES)
    }

class CustomInvoice:
    # Default margins
    TOP = 280  # Increased from 260 to make room for logo
    LEFT = 20
    RIGHT = 20
    BOTTOM = 20

    def __init__(self, customer, transactions, error_rate=0.04):
        self.customer = customer
        self.transactions = transactions
        self.error_rate = error_rate
        self.style = get_random_style()
        self.logo = generate_random_logo()
        self.pdf = None
        self.errors = []

    def generate(self, output_path):
        """Generate the invoice PDF."""
        self.pdf = canvas.Canvas(output_path)
        self.pdf.setPageSize((210 * mm, 297 * mm))  # A4 size
        
        # Draw content
        self._draw_logo()
        self._draw_header()
        self._draw_customer_info()
        self._draw_company_info()
        self._draw_items()
        self._draw_total()
        
        # Save the file
        self.pdf.save()
        
        return {
            'path': output_path,
            'errors': self.errors if self.errors else None
        }

    def _draw_logo(self):
        """Draw the random logo in the upper left corner."""
        renderPDF.draw(self.logo, self.pdf, self.LEFT * mm, (self.TOP - 15) * mm)

    def _draw_header(self):
        """Draw the invoice header."""
        self.pdf.setFont(self.style['font'], self.style['size']['header'])
        self.pdf.setFillColor(self.style['color'])
        self.pdf.drawString(self.LEFT * mm, (self.TOP - 30) * mm, "INVOICE")
        self.pdf.drawString((self.LEFT + 100) * mm, (self.TOP - 30) * mm, f"Date: {datetime.now().strftime('%Y-%m-%d')}")

    def _draw_customer_info(self):
        """Draw the customer information."""
        self.pdf.setFont(self.style['font'], self.style['size']['base'])
        y = self.TOP - 50
        self.pdf.drawString(self.LEFT * mm, y * mm, "Bill To:")
        y -= 15
        self.pdf.drawString(self.LEFT * mm, y * mm, f"{self.customer['first_name']} {self.customer['last_name']}")
        y -= 15
        self.pdf.drawString(self.LEFT * mm, y * mm, self.customer['street'])
        y -= 15
        self.pdf.drawString(self.LEFT * mm, y * mm, f"{self.customer['city']}, {self.customer['state']} {self.customer['zip']}")

    def _draw_company_info(self):
        """Draw the company information."""
        company = get_random_company()
        address = get_random_address()
        
        self.pdf.setFont(self.style['font'], self.style['size']['base'])
        y = self.TOP - 50
        self.pdf.drawString((self.LEFT + 100) * mm, y * mm, company)
        y -= 15
        self.pdf.drawString((self.LEFT + 100) * mm, y * mm, address['street'])
        y -= 15
        self.pdf.drawString((self.LEFT + 100) * mm, y * mm, f"{address['city']}, {address['state']} {address['postal_code']}")

    def _draw_items(self):
        """Draw the line items."""
        # Draw header
        y = self.TOP - 120
        self.pdf.setFont(self.style['font'], self.style['size']['base'])
        self.pdf.drawString(self.LEFT * mm, y * mm, "Description")
        self.pdf.drawString((self.LEFT + 80) * mm, y * mm, "Units")
        self.pdf.drawString((self.LEFT + 110) * mm, y * mm, "Price/Unit")
        self.pdf.drawString((self.LEFT + 150) * mm, y * mm, "Total")
        
        # Draw line
        y -= 5
        self.pdf.line(self.LEFT * mm, y * mm, (210 - self.RIGHT) * mm, y * mm)
        
        # Draw items
        y -= 15
        
        for trans in self.transactions:
            units = int(trans['numberofitems'])
            price_per_unit = float(trans['price_per_unit'])
            total = float(trans['transactiontotal'])  # Use the pre-calculated total that includes errors
            
            # Calculate the correct total for error tracking
            correct_total = units * price_per_unit
            if abs(total - correct_total) > 0.01:  # Check if there's a math error
                self.errors.append(f"Item total should be ${correct_total:.2f}, but shows ${total:.2f}")
            
            self.pdf.drawString(self.LEFT * mm, y * mm, trans['productcategory'])
            self.pdf.drawString((self.LEFT + 80) * mm, y * mm, str(units))
            self.pdf.drawString((self.LEFT + 110) * mm, y * mm, f"${price_per_unit:.2f}")
            self.pdf.drawString((self.LEFT + 150) * mm, y * mm, f"${total:.2f}")
            
            y -= 15

    def _draw_total(self):
        """Draw the total amount."""
        # Use the sum of the pre-calculated totals that include errors
        total = sum(float(t['transactiontotal']) for t in self.transactions)
        y = self.pdf._y - 30
        
        self.pdf.setFont(self.style['font'], self.style['size']['base'])
        self.pdf.drawString((self.LEFT + 110) * mm, y * mm, "Total:")
        self.pdf.drawString((self.LEFT + 150) * mm, y * mm, f"${total:.2f}")

def draw_header(canvas, person, style):
    """Draw the invoice header."""
    # Draw company logo
    logo = generate_random_logo()
    renderPDF.draw(logo, canvas, 20 * mm, 260 * mm)
    
    # Draw INVOICE text
    canvas.setFont(style['font'], style['size']['header'])
    canvas.setFillColor(style['color'])
    canvas.drawString(20 * mm, 240 * mm, "INVOICE")
    
    # Draw invoice date
    canvas.setFont(style['font'], style['size']['base'])
    canvas.drawString(120 * mm, 240 * mm, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    
    # Draw customer info
    canvas.setFont(style['font'], style['size']['base'])
    canvas.drawString(20 * mm, 220 * mm, "Bill To:")
    canvas.drawString(20 * mm, 205 * mm, f"{person['first_name']} {person['last_name']}")
    canvas.drawString(20 * mm, 190 * mm, person['street'])
    canvas.drawString(20 * mm, 175 * mm, f"{person['city']}, {person['state']} {person['zip']}")

def draw_company_info(canvas, style):
    """Draw the company information."""
    company = get_random_company()
    address = get_random_address()
    
    canvas.setFont(style['font'], style['size']['base'])
    canvas.setFillColor(style['color'])
    canvas.drawString(120 * mm, 220 * mm, company)
    canvas.drawString(120 * mm, 205 * mm, address['street'])
    canvas.drawString(120 * mm, 190 * mm, f"{address['city']}, {address['state']} {address['postal_code']}")

def draw_invoice_details(canvas, customer_id, style):
    """Draw invoice details."""
    canvas.setFont(style['font'], style['size']['base'])
    canvas.setFillColor(style['color'])
    canvas.drawString(20 * mm, 150 * mm, "Invoice Details")
    canvas.drawString(20 * mm, 135 * mm, f"Invoice #: INV-{customer_id[:8]}")
    canvas.drawString(120 * mm, 135 * mm, f"Customer ID: {customer_id}")

def draw_transactions(canvas, transactions, should_have_errors, style):
    """Draw transaction items and calculate totals."""
    # Draw header
    y = 110
    canvas.setFont(style['font'], style['size']['base'])
    canvas.setFillColor(style['color'])
    canvas.drawString(20 * mm, y * mm, "Description")
    canvas.drawString(80 * mm, y * mm, "Units")
    canvas.drawString(110 * mm, y * mm, "Price/Unit")
    canvas.drawString(150 * mm, y * mm, "Total")
    
    # Draw separator line
    y -= 5
    canvas.line(20 * mm, y * mm, 190 * mm, y * mm)
    
    # Draw items
    y -= 10
    canvas.setFont(style['font'], style['size']['base'])
    grand_total = 0
    has_errors = False
    
    for trans in transactions:
        units = int(trans['numberofitems'])
        price_per_unit = float(trans['price_per_unit'])
        total = float(trans['transactiontotal'])
        
        # Check if this transaction has a math error
        correct_total = units * price_per_unit
        if abs(total - correct_total) > 0.01:
            has_errors = True
        
        grand_total += total
        
        canvas.drawString(20 * mm, y * mm, trans['productcategory'])
        canvas.drawString(80 * mm, y * mm, str(units))
        canvas.drawString(110 * mm, y * mm, f"${price_per_unit:.2f}")
        canvas.drawString(150 * mm, y * mm, f"${total:.2f}")
        
        y -= 10
    
    # Draw total
    y -= 10
    canvas.line(20 * mm, y * mm, 190 * mm, y * mm)
    y -= 10
    canvas.setFont(style['font'], style['size']['header'])
    canvas.setFillColor(style['color'])
    canvas.drawString(110 * mm, y * mm, "Total:")
    canvas.drawString(150 * mm, y * mm, f"${grand_total:.2f}")
    
    return has_errors

def generate_invoice(person, transactions, error_rate=0.0, dirty_rate=0.0):
    """Generate a PDF invoice for the given customer and transactions."""
    customer_id = person['customer_id']
    output_dir = os.path.join('pdf_output')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'invoice_{customer_id}.pdf')
    
    # Create the PDF document
    width, height = letter
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # Get random style for this invoice
    style = get_random_style()
    c.setFont(style['font'], style['size']['base'])
    c.setFillColor(style['color'])
    
    # Initialize PDF distorter if dirty_rate > 0
    distorter = None
    if dirty_rate > 0 and random.random() < dirty_rate/100:
        distorter = PDFDistorter(100)  # If we're applying distortions, apply them fully
    
    # Create a separate layer for distortions
    if distorter:
        # Save state before distortions
        c.saveState()
        # Apply visual effects first as background
        distorter.apply_distortions(c, width, height)
        # Restore state to ensure effects don't affect content
        c.restoreState()
        
        # Apply rotation after background effects
        skew_angle = distorter.get_page_skew()
        c.translate(width/2, height/2)
        c.rotate(skew_angle)
        c.translate(-width/2, -height/2)
    
    # Draw invoice content with consistent style
    c.setFont(style['font'], style['size']['header'])  # Larger size for header
    c.setFillColor(style['color'])
    draw_header(c, person, style)
    
    c.setFont(style['font'], style['size']['base'])  # Base size for rest
    c.setFillColor(style['color'])
    draw_company_info(c, style)
    draw_invoice_details(c, customer_id, style)
    
    # Check for math errors in any transaction
    has_errors = False
    for trans in transactions:
        units = int(trans['numberofitems'])
        price_per_unit = float(trans['price_per_unit'])
        total = float(trans['transactiontotal'])
        correct_total = round(units * price_per_unit, 2)
        if abs(total - correct_total) > 0.01:
            has_errors = True
            break
    
    draw_transactions(c, transactions, error_rate > 0, style)
    
    # Finalize the PDF
    c.showPage()
    c.save()
    return has_errors 