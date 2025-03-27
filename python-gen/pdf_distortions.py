import random
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import io
import math
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.lib import colors
import numpy as np

class PDFDistorter:
    def __init__(self, dirty_rate):
        """Initialize the PDF distorter with a given dirty rate (0-100)."""
        self.dirty_rate = dirty_rate / 100.0  # Convert to decimal
        
        # Define color palettes for various effects
        self.coffee_colors = [
            (139, 69, 19, 30),   # Dark brown with alpha
            (160, 82, 45, 25),   # Sienna with alpha
            (101, 67, 33, 20),   # Darker brown with alpha
            (210, 180, 140, 15)  # Tan with alpha
        ]
        
        self.ink_colors = [
            (5, 5, 5, 2),       # Almost black, very transparent
            (20, 20, 40, 3),    # Dark blue-black
            (30, 10, 10, 2)     # Dark red-black
        ]
        
        # Paper texture colors
        self.paper_colors = [
            (250, 250, 250, 2),  # Almost white
            (245, 245, 240, 2),  # Slight cream
            (248, 248, 245, 2)   # Off-white
        ]

    def should_apply_effect(self):
        """Determine if an effect should be applied based on dirty_rate."""
        return random.random() < (self.dirty_rate * 2)  # Double the chance of effects

    def get_page_skew(self):
        """Get random skew angle for the whole page."""
        direction = random.choice([-1, 1])
        return direction * random.uniform(0.1, 0.8)  # Reduced max angle for subtlety

    def apply_paper_texture(self, canvas, width, height):
        """Apply subtle paper texture effect."""
        width = int(width)
        height = int(height)
        num_spots = random.randint(1000, 2000)
        canvas.setFillAlpha(0.02)  # Very subtle
        
        for _ in range(num_spots):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.uniform(0.2, 0.8)
            color = random.choice(self.paper_colors)
            canvas.setFillColor(colors.Color(color[0]/255, color[1]/255, color[2]/255))
            canvas.circle(x, y, size, fill=1)

    def apply_fold_crease(self, canvas, width, height):
        """Apply paper fold or crease effect."""
        # Horizontal or vertical fold
        is_horizontal = random.random() < 0.5
        
        if is_horizontal:
            y = height * random.uniform(0.3, 0.7)
            # Main crease line
            canvas.setStrokeColor(colors.Color(0.8, 0.8, 0.8))
            canvas.setStrokeAlpha(0.1)
            canvas.setLineWidth(0.5)
            canvas.line(0, y, width, y)
            
            # Shadow effect
            num_shadow_lines = random.randint(3, 5)
            for i in range(num_shadow_lines):
                offset = random.uniform(-2, 2)
                canvas.setStrokeAlpha(0.05 - (abs(offset) * 0.01))
                canvas.line(0, y + offset, width, y + offset)
        else:
            x = width * random.uniform(0.3, 0.7)
            canvas.setStrokeColor(colors.Color(0.8, 0.8, 0.8))
            canvas.setStrokeAlpha(0.1)
            canvas.setLineWidth(0.5)
            canvas.line(x, 0, x, height)
            
            num_shadow_lines = random.randint(3, 5)
            for i in range(num_shadow_lines):
                offset = random.uniform(-2, 2)
                canvas.setStrokeAlpha(0.05 - (abs(offset) * 0.01))
                canvas.line(x + offset, 0, x + offset, height)

    def apply_ink_bleeding(self, canvas, x, y, size):
        """Apply realistic ink bleeding effect."""
        num_points = random.randint(8, 12)
        bleed_points = []
        
        # Create irregular shape for bleeding
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            r = random.uniform(0.7, 1.3) * size
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            bleed_points.append((px, py))
        
        # Draw multiple layers with varying opacity
        for _ in range(3):
            canvas.setFillColor(random.choice(self.ink_colors))
            canvas.setFillAlpha(random.uniform(0.01, 0.03))
            
            path = canvas.beginPath()
            path.moveTo(bleed_points[0][0], bleed_points[0][1])
            
            # Use quadratic curves for more natural bleeding
            for i in range(1, len(bleed_points)):
                cp_x = (bleed_points[i-1][0] + bleed_points[i][0]) / 2
                cp_y = (bleed_points[i-1][1] + bleed_points[i][1]) / 2
                path.curveTo(cp_x, cp_y, cp_x, cp_y, bleed_points[i][0], bleed_points[i][1])
            
            path.close()
            canvas.drawPath(path, fill=1)

    def apply_coffee_stain(self, canvas, width, height):
        """Apply realistic coffee/tea stain effect."""
        width = int(width)
        height = int(height)
        # Create main stain
        x = random.randint(width//4, 3*width//4)
        y = random.randint(height//4, 3*height//4)
        size = random.randint(30, 50)
        
        # Create irregular shape for main stain
        num_points = random.randint(12, 16)
        points = []
        
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            r = random.uniform(0.7, 1.3) * size
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            points.append((px, py))
        
        # Draw multiple layers with varying colors and opacity
        for color in self.coffee_colors:
            canvas.setFillColor(colors.Color(color[0]/255, color[1]/255, color[2]/255))
            canvas.setFillAlpha(color[3]/255)
            
            path = canvas.beginPath()
            path.moveTo(points[0][0], points[0][1])
            
            # Use quadratic curves for more natural stain edges
            for i in range(1, len(points)):
                cp_x = (points[i-1][0] + points[i][0]) / 2
                cp_y = (points[i-1][1] + points[i][1]) / 2
                path.curveTo(cp_x, cp_y, cp_x, cp_y, points[i][0], points[i][1])
            
            path.close()
            canvas.drawPath(path, fill=1)
        
        # Add splatter effects
        num_splatters = random.randint(5, 8)
        for _ in range(num_splatters):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(size * 0.8, size * 1.5)
            splat_x = x + distance * math.cos(angle)
            splat_y = y + distance * math.sin(angle)
            splat_size = random.uniform(2, 5)
            
            color = random.choice(self.coffee_colors)
            canvas.setFillColor(colors.Color(color[0]/255, color[1]/255, color[2]/255))
            canvas.setFillAlpha(color[3]/255 * 0.7)  # Slightly more transparent
            canvas.circle(splat_x, splat_y, splat_size, fill=1)

    def apply_printer_lines(self, canvas, width, height):
        """Apply enhanced printer line artifacts."""
        width = int(width)
        height = int(height)
        num_lines = random.randint(1, 2)  # Reduced number for subtlety
        section_width = width / num_lines
        
        for i in range(num_lines):
            x = i * section_width + random.uniform(0, section_width/2)
            line_width = random.uniform(0.3, 0.8)  # Thinner lines
            
            # Main line with varying opacity
            canvas.setStrokeColor(colors.Color(0.2, 0.2, 0.2))
            canvas.setStrokeAlpha(random.uniform(0.05, 0.1))
            canvas.setLineWidth(line_width)
            
            # Create slight waviness
            num_segments = random.randint(10, 15)
            segment_height = height / num_segments
            
            for j in range(num_segments):
                y1 = j * segment_height
                y2 = (j + 1) * segment_height
                offset = random.uniform(-0.5, 0.5)  # Subtle offset
                canvas.line(x + offset, y1, x - offset, y2)
            
            # Add fading effect at ends
            canvas.setStrokeAlpha(0.03)
            canvas.line(x, 0, x, height/10)  # Top fade
            canvas.line(x, height*0.9, x, height)  # Bottom fade

    def apply_distortions(self, canvas, width, height):
        """Apply enhanced distortions directly to the PDF canvas."""
        # Convert dimensions to integers
        width = int(width)
        height = int(height)
        
        # Save the canvas state
        canvas.saveState()
        
        # Apply paper texture first
        self.apply_paper_texture(canvas, width, height)
        
        # Random chance to apply each effect
        if random.random() < 0.3:
            self.apply_fold_crease(canvas, width, height)
        
        if random.random() < 0.4:
            self.apply_coffee_stain(canvas, width, height)
        
        # Apply printer lines with reduced frequency
        if random.random() < 0.3:
            self.apply_printer_lines(canvas, width, height)
        
        # Add random ink bleeding effects
        num_bleeds = random.randint(2, 4)
        for _ in range(num_bleeds):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.uniform(1, 3)
            self.apply_ink_bleeding(canvas, x, y, size)
        
        # Restore the canvas state
        canvas.restoreState() 