"""
NXTSYNC CERTIFICATE GENERATOR - FIXED VERSION
==============================================
NOW SAVES TO static/certificates/ TO MATCH app.py!
"""

from PIL import Image, ImageDraw, ImageFont
import qrcode
from datetime import datetime, timedelta
import os
import sys

# ========== CONFIGURATION ==========
# Try multiple possible template names
POSSIBLE_TEMPLATES = [
    'static/templates/blank_certificate_template.jpg',
    'static/templates/template.jpg',
    'template.jpg', 
    'template.png'
]

# FIXED: Changed to match app.py's expected folder
OUTPUT_FOLDER = 'static/certificates'

# Text positions (percentages of image height)
POSITIONS = {
    'name_y': 0.515,
    'name_underline': 0.57,
    'text1_y': 0.633,
    'domain_y': 0.673,
    'text2_y': 0.712,
    'qr_y': 0.78
}

# Colors matching your certificate
COLORS = {
    'name': (184, 134, 86),       # Gold/tan for name
    'text': (0, 0, 0),            # Black for text
    'underline': (128, 128, 128)  # Gray for underline
}

# Font sizes
FONT_SIZES = {
    'name': 60,
    'domain': 26,
    'text': 19
}

# ========== DATABASE ==========
STUDENTS = [
    {
        'id': 'CERT001',
        'name': 'PULLABHOTLA VENKATARAMA SASTRY',
        'domain': 'Full Stack Web Development',
        'start_date': '2025-05-19'
    },
    {
        'id': 'CERT002',
        'name': 'kovuru Praneeth',
        'domain': 'Full Stack Web Development',
        'start_date': '2025-05-19'
    },
    {
        'id': 'CERT003',
        'name': 'DODDA YUVARATNA',
        'domain': 'Full Stack Web Development',
        'start_date': '2025-05-19'
    },
    {
        'id': 'CERT004',
        'name': 'GOTTEMUKKALA KEERTHI',
        'domain': 'Full Stack Web Development',
        'start_date': '2025-05-19'
    },
    {
        'id': 'CERT005',
        'name': 'TATIPAKALA VINEELA',
        'domain': 'Full Stack Web Development',
        'start_date': '2025-05-19'
    },
    {
        'id': 'CERT006',
        'name': 'CHEGIREDDY KARTHEEK REDDY',
        'domain': 'Full Stack Web Development',
        'start_date': '2025-05-19'
    },
    {
        'id': 'CERT007',
        'name': 'SINGAMPALLI UMA JAYA SREE',
        'domain': 'Full Stack Web Development',
        'start_date': '2025-05-19'
    },
    {
        'id': 'CERT008',
        'name': 'MANDALAPU MARUTHI SAI KRISHNA',
        'domain': 'Full Stack Web Development',
        'start_date': '2025-05-19'
    },
]

# ========== FUNCTIONS ==========

def find_template():
    """Find the template file"""
    print("🔍 Looking for template file...")
    
    current_dir = os.getcwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Try predefined paths first
    for template_path in POSSIBLE_TEMPLATES:
        if os.path.exists(template_path):
            print(f"✅ Found template: {template_path}")
            return template_path
    
    # Search in common locations
    search_locations = [
        'static/templates',
        'templates',
        '.'
    ]
    
    for location in search_locations:
        if os.path.exists(location):
            for file in os.listdir(location):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    if 'template' in file.lower() or 'certificate' in file.lower():
                        full_path = os.path.join(location, file)
                        print(f"✅ Found possible template: {full_path}")
                        return full_path
    
    return None

def load_fonts():
    """Load fonts for the certificate"""
    try:
        # Try Windows fonts first
        name_font = ImageFont.truetype("C:\\Windows\\Fonts\\georgiai.ttf", FONT_SIZES['name'])
        domain_font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", FONT_SIZES['domain'])
        text_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", FONT_SIZES['text'])
        print("✅ Loaded Windows fonts")
        return name_font, domain_font, text_font
    except:
        try:
            # Try Linux fonts
            name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 
                                           FONT_SIZES['name'])
            domain_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 
                                             FONT_SIZES['domain'])
            text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 
                                           FONT_SIZES['text'])
            print("✅ Loaded Linux fonts")
            return name_font, domain_font, text_font
        except:
            print("⚠️  Using default fonts")
            default = ImageFont.load_default()
            return default, default, default

def create_qr_code(cert_id, base_url="http://192.168.0.66:5000"):
    """Generate QR code for verification"""
    verification_url = f"{base_url}/verify/{cert_id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(verification_url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def calculate_end_date(start_date_str):
    """Calculate end date (127 days after start)"""
    try:
        start = datetime.strptime(start_date_str, '%Y-%m-%d')
        end = start + timedelta(days=127)
        return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')
    except:
        return start_date_str, "2026-03-31"

def generate_certificate(student_data, template_path, output_folder):
    """Generate certificate for one student"""
    try:
        cert_id = student_data['id']
        name = student_data['name']
        domain = student_data['domain']
        start_date = student_data['start_date']
        
        print(f"\n{'='*70}")
        print(f"🎨 Generating: {name}")
        print(f"   Domain: {domain}")
        print(f"   Start: {start_date}")
        
        # Open template
        certificate = Image.open(template_path).convert('RGB')
        draw = ImageDraw.Draw(certificate)
        width, height = certificate.size
        
        print(f"   Template size: {width}x{height}")
        
        # Load fonts
        name_font, domain_font, text_font = load_fonts()
        
        # Calculate dates
        start_str, end_str = calculate_end_date(start_date)
        print(f"   Period: {start_str} to {end_str}")
        
        center_x = width // 2
        
        # ========== 1. DRAW NAME (Italic, Gold) ==========
        name_y = int(height * POSITIONS['name_y'])
        draw.text((center_x, name_y), name, 
                  fill=COLORS['name'], font=name_font, anchor="mm")
        
        # Draw underline
        underline_y = int(height * POSITIONS['name_underline'])
        underline_length = 300
        draw.line([center_x - underline_length, underline_y,
                   center_x + underline_length, underline_y],
                  fill=COLORS['underline'], width=2)
        
        # ========== 2. DRAW TEXT LINE 1 ==========
        text1_y = int(height * POSITIONS['text1_y'])
        text1 = "has successfully completed the internship "
        draw.text((center_x, text1_y), text1, 
                  fill=COLORS['text'], font=text_font, anchor="mm")
        
        # ========== 3. DRAW DOMAIN (Bold) ==========
        domain_y = int(height * POSITIONS['domain_y'])
        draw.text((center_x, domain_y), domain,
                  fill=COLORS['text'], font=domain_font, anchor="mm")
        
        # ========== 4. DRAW TEXT LINE 2 ==========
        text2_y = int(height * POSITIONS['text2_y'])
        text2 = f"conducted by Nxtsync from {start_str} to {end_str}."
        draw.text((center_x, text2_y), text2,
                  fill=COLORS['text'], font=text_font, anchor="mm")
        
        # ========== 5. ADD QR CODE ==========
        qr_img = create_qr_code(cert_id)
        qr_size = 140
        qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        
        qr_x = center_x - (qr_size // 2)
        qr_y = int(height * POSITIONS['qr_y'])
        certificate.paste(qr_img, (qr_x, qr_y))
        
        # ========== 6. SAVE ==========
        # FIXED: Save with just CERT ID (matching app.py expectations)
        output_path = os.path.join(output_folder, f'{cert_id}.jpg')
        certificate.save(output_path, 'JPEG', quality=95)
        
        print(f"✅ Saved: {output_path}")
        print(f"{'='*70}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("\n" + "="*70)
    print("🎓 NXTSYNC CERTIFICATE GENERATOR")
    print("="*70 + "\n")
    
    # Create required folders
    os.makedirs('static/templates', exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Find template
    template_path = find_template()
    
    if not template_path:
        print("\n❌ ERROR: No template file found!")
        print("\n📋 WHAT TO DO:")
        print("   1. Save your blank certificate template image")
        print("   2. Put it in: static/templates/")
        print("   3. Name it: blank_certificate_template.jpg")
        print("   4. Run this script again")
        print("\n" + "="*70 + "\n")
        input("Press ENTER to exit...")
        return
    
    # Load and check template
    try:
        template = Image.open(template_path)
        print(f"\n✅ Template loaded successfully!")
        print(f"   Size: {template.size[0]}x{template.size[1]} pixels")
        print(f"   Format: {template.format}")
        print(f"📂 Output folder: {OUTPUT_FOLDER}/")
        print(f"📊 Students to process: {len(STUDENTS)}")
        print("\n" + "="*70)
    except Exception as e:
        print(f"\n❌ ERROR loading template: {e}")
        print("The image file might be corrupted or invalid.")
        input("Press ENTER to exit...")
        return
    
    # Generate certificates
    success_count = 0
    fail_count = 0
    
    for student in STUDENTS:
        if generate_certificate(student, template_path, OUTPUT_FOLDER):
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print("\n" + "="*70)
    print("📊 GENERATION COMPLETE!")
    print(f"   ✅ Success: {success_count}")
    print(f"   ❌ Failed: {fail_count}")
    print(f"   📂 Certificates saved in: {OUTPUT_FOLDER}/")
    print("="*70 + "\n")
    
    # Show generated files
    if success_count > 0:
        print("🎉 Generated certificates:")
        cert_files = sorted(os.listdir(OUTPUT_FOLDER))
        for i, file in enumerate(cert_files, 1):
            print(f"   {i}. {file}")
        print()
    
    print("\n🚀 NOW YOU CAN RUN: python app.py")
    print("   The certificates are in the correct location!\n")
    
    input("Press ENTER to exit...")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress ENTER to exit...")