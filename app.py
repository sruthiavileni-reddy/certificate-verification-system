from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import qrcode
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
CORS(app)

# Create necessary directories
os.makedirs('static/certificates', exist_ok=True)
os.makedirs('static/templates', exist_ok=True)

def init_db():
    """Initialize database with sample certificates"""
    conn = sqlite3.connect('certificates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS certificates
                 (id TEXT PRIMARY KEY, 
                  name TEXT, 
                  domain TEXT, 
                  issue_date TEXT,
                  certificate_url TEXT)''')
    
    # Sample certificates
    certificates = [
        ('CERT001', 'PULLABHOTLA VENKATARAMA SASTRY', 'Full Stack Web Development', '2025-08-19', ''),
        ('CERT002', 'kovuru Praneeth ', 'Full Stack Web Development', '2025-08-19', ''),
        ('CERT003', 'DODDA YUVARATNA ', 'Full Stack Web Development', '2025-08-19', ''),
        ('CERT004', 'GOTTEMUKKALA KEERTHI ', 'Full Stack Web Development', '2025-08-19', ''),
        ('CERT005', 'TATIPAKALA VINEELA', 'Full Stack Web Development', '2025-08-19', ''),
        ('CERT006', 'CHEGIREDDY KARTHEEK REDDY ', 'Full Stack Web Development', '2025-08-19', ''),
        ('CERT007', 'SINGAMPALLI UMA JAYA SREE ', 'Full Stack Web Development', '2025-08-19', ''),
        ('CERT008', 'MANDALAPU MARUTHI SAI KRISHNA ', 'Full Stack Web Development', '2025-08-19', ''),
       
    ]
    
    c.executemany('INSERT OR IGNORE INTO certificates VALUES (?,?,?,?,?)', certificates)
    conn.commit()
    conn.close()
    print("✅ Database initialized")

def create_qr_code_image(cert_id):
    """Generate QR code for certificate verification"""
    if os.environ.get('RENDER'):
        base_url = "https://certificate-verification-system-3.onrender.com"
    else:
        # Fixed IP address for your laptop
        base_url = "http://192.168.0.66:5000"
    
    verification_url = f"{base_url}/verify/{cert_id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(verification_url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def generate_certificate_image(name, domain, start_date, end_date, cert_id):
    """
    Generate certificate using Picture 1 as template
    Adds dynamic content like Picture 2:
    - Name in italic gold/tan
    - "has successfully completed the internship [DOMAIN] conducted by"
    - "Nxtsync from [START] to [END]."
    - QR code
    """
    try:
        print(f"\n{'='*80}")
        print(f"🎨 GENERATING CERTIFICATE")
        print(f"   Name: {name}")
        print(f"   Domain: {domain}")
        print(f"   Period: {start_date} to {end_date}")
        print(f"   ID: {cert_id}")
        print(f"{'='*80}\n")
        
        # Check if template exists
        template_path = 'static/templates/blank_certificate_template.jpg'
        
        if not os.path.exists(template_path):
            print("❌ TEMPLATE NOT FOUND!")
            print("⚠️  Please run the setup script first:")
            print("    python setup_certificate.py")
            return None
        
        # Open the blank template (Picture 1)
        certificate = Image.open(template_path).convert('RGB')
        draw = ImageDraw.Draw(certificate)
        width, height = certificate.size
        
        print(f"📐 Template size: {width}x{height}")
        
        # Load fonts
        try:
            # Linux fonts
            name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 60)
            domain_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
            text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)
            print("✅ Loaded Linux fonts")
        except:
            try:
                # Windows fonts
                name_font = ImageFont.truetype("C:\\Windows\\Fonts\\georgiai.ttf", 60)
                domain_font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 26)
                text_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 19)
                print("✅ Loaded Windows fonts")
            except:
                print("⚠️ Using default fonts")
                name_font = ImageFont.load_default()
                domain_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
        
        # Colors from your certificate design
        gold_tan = (184, 134, 86)  # Gold/tan for name (from Picture 2)
        black = (0, 0, 0)
        gray = (128, 128, 128)
        
        center_x = width // 2
        
        # ========== DRAW NAME (Italic, Gold/Tan) ==========
        name_y = int(height * 0.515)  # Position matching Picture 2
        draw.text((center_x, name_y), name, fill=gold_tan, font=name_font, anchor="mm")
        print(f"✅ Drew name: {name}")
        
        # Draw underline under name
        underline_y = name_y + 50
        underline_length = 300
        draw.line([center_x - underline_length, underline_y, 
                   center_x + underline_length, underline_y], 
                  fill=gray, width=2)
        
        # ========== CALCULATE DATES ==========
        try:
            start_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_obj = start_obj + timedelta(days=127)
            start_str = start_obj.strftime('%Y-%m-%d')
            end_str = end_obj.strftime('%Y-%m-%d')
        except:
            start_str = start_date
            end_str = end_date
        
        print(f"📅 Dates: {start_str} to {end_str}")
        
        # ========== DRAW TEXT LINE 1 ==========
        # "has successfully completed the internship"
        text1_y = int(height * 0.633)
        text1 = "has successfully completed the internship "
        draw.text((center_x, text1_y), text1, fill=black, font=text_font, anchor="mm")
        
        # ========== DRAW DOMAIN (Bold, Black) ==========
        domain_y = int(height * 0.673)
        draw.text((center_x, domain_y), domain, fill=black, font=domain_font, anchor="mm")
        print(f"✅ Drew domain: {domain}")
        
        # ========== DRAW TEXT LINE 2 ==========
        # "conducted by Nxtsync from [START] to [END]."
        dates_y = int(height * 0.712)
        dates_text = f"conducted by Nxtsync from {start_str} to {end_str}."
        draw.text((center_x, dates_y), dates_text, fill=black, font=text_font, anchor="mm")
        print(f"✅ Drew dates line")
        
        # ========== ADD QR CODE ==========
        qr_img = create_qr_code_image(cert_id)
        qr_size = 140
        qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        
        qr_x = center_x - (qr_size // 2)
        qr_y = int(height * 0.78)
        certificate.paste(qr_img, (qr_x, qr_y))
        print(f"✅ Added QR code")
        
        # ========== SAVE ==========
        output_path = f'static/certificates/{cert_id}.jpg'
        certificate.save(output_path, 'JPEG', quality=95)
        
        print(f"✅ SAVED: {output_path}")
        print(f"{'='*80}\n")
        
        return output_path
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_certificate_url(cert_id):
    """Get or generate certificate URL"""
    cert_path = f'static/certificates/{cert_id}.jpg'
    
    # Generate if doesn't exist
    if not os.path.exists(cert_path):
        conn = sqlite3.connect('certificates.db')
        c = conn.cursor()
        c.execute('SELECT name, domain, issue_date FROM certificates WHERE id=?', (cert_id,))
        result = c.fetchone()
        conn.close()
        
        if result:
            name, domain, issue_date = result
            try:
                start = datetime.strptime(issue_date, '%Y-%m-%d')
                end = start + timedelta(days=127)
                end_date = end.strftime('%Y-%m-%d')
            except:
                end_date = "2026-03-31"
            
            cert_path = generate_certificate_image(name, domain, issue_date, end_date, cert_id)
            if not cert_path:
                return None
        else:
            return None
    
    # Return URL with fixed IP
    if os.environ.get('RENDER'):
        base_url = "https://certificate-verification-system-3.onrender.com"
    else:
        base_url = "http://192.168.0.66:5000"
    
    return f"{base_url}/static/certificates/{cert_id}.jpg"

# ========== ROUTES ==========

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify/<cert_id>')
def verify_certificate(cert_id):
    return render_template('verify.html', cert_id=cert_id)

@app.route('/certificate/<cert_id>')
def full_certificate(cert_id):
    return render_template('certificate.html', cert_id=cert_id)

@app.route('/api/certificate/<cert_id>')
def get_certificate(cert_id):
    """Get certificate details by ID"""
    conn = sqlite3.connect('certificates.db')
    c = conn.cursor()
    c.execute('SELECT * FROM certificates WHERE id=?', (cert_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        certificate_url = get_certificate_url(cert_id)
        if not certificate_url:
            return jsonify({'success': False, 'message': 'Failed to generate certificate'})
        
        return jsonify({
            'success': True,
            'id': result[0],
            'name': result[1],
            'domain': result[2],
            'issue_date': result[3],
            'certificate_url': certificate_url
        })
    else:
        return jsonify({'success': False, 'message': 'Certificate not found'})

@app.route('/api/search')
def search_certificate():
    """Search certificate by name"""
    name = request.args.get('name', '').strip().upper()
    
    if not name:
        return jsonify({'success': False, 'message': 'Name required'})
    
    conn = sqlite3.connect('certificates.db')
    c = conn.cursor()
    c.execute('SELECT id, name FROM certificates WHERE UPPER(name) LIKE ?', (f'%{name}%',))
    result = c.fetchone()
    conn.close()
    
    if result:
        return jsonify({'success': True, 'id': result[0], 'name': result[1]})
    else:
        return jsonify({'success': False, 'message': f'No certificate found for "{name}"'})

@app.route('/api/regenerate-all')
def regenerate_all_certificates():
    """Regenerate all certificates"""
    print("\n" + "="*80)
    print("🔄 REGENERATING ALL CERTIFICATES")
    print("="*80 + "\n")
    
    # Check template
    if not os.path.exists('static/templates/blank_certificate_template.jpg'):
        return jsonify({
            'success': False,
            'message': 'Template not found! Run setup first.'
        })
    
    # Delete old certificates
    if os.path.exists('static/certificates'):
        for file in os.listdir('static/certificates'):
            if file.endswith('.jpg'):
                os.remove(f'static/certificates/{file}')
    
    # Generate all
    conn = sqlite3.connect('certificates.db')
    c = conn.cursor()
    c.execute('SELECT id, name, domain, issue_date FROM certificates')
    results = c.fetchall()
    conn.close()
    
    generated = []
    failed = []
    
    for cert in results:
        cert_id, name, domain, issue_date = cert
        
        try:
            start = datetime.strptime(issue_date, '%Y-%m-%d')
            end = start + timedelta(days=127)
            end_date = end.strftime('%Y-%m-%d')
        except:
            end_date = "2026-03-31"
        
        cert_path = generate_certificate_image(name, domain, issue_date, end_date, cert_id)
        
        if cert_path:
            generated.append(cert_id)
        else:
            failed.append(cert_id)
    
    print(f"\n✅ Generated: {len(generated)} | ❌ Failed: {len(failed)}\n")
    
    return jsonify({
        'success': True,
        'message': f'Generated {len(generated)}, Failed {len(failed)}',
        'generated': generated,
        'failed': failed
    })

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🏢 NXTSYNC CERTIFICATE VERIFICATION SYSTEM")
    print("="*80)
    
    # Check template
    if not os.path.exists('static/templates/blank_certificate_template.jpg'):
        print("\n⚠️  WARNING: Template not found!")
        print("📝 Please run setup first:")
        print("    python setup_certificate.py")
        print("="*80 + "\n")
    else:
        print("\n✅ Template found - ready to generate!")
        print("="*80 + "\n")
    
    init_db()
    
    PORT = int(os.environ.get('PORT', 5000))
    is_production = os.environ.get('RENDER', False)
    
    if not is_production:
        print(f"🌐 URL: http://192.168.0.66:{PORT}")
        print(f"🔄 Regenerate: http://192.168.0.66:{PORT}/api/regenerate-all")
        print(f"📱 Try searching: DODDA YUVARATNA")
        print("\n" + "="*80 + "\n")
        
        import webbrowser
        from threading import Timer
        Timer(2, lambda: webbrowser.open(f'http://192.168.0.66:{PORT}')).start()
    
    app.run(debug=not is_production, host='0.0.0.0', port=PORT, use_reloader=False)