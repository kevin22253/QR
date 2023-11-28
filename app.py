from flask import Flask, render_template, request
import qrcode
import hashlib

app = Flask(_name_)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    data = request.args.get('data')

    # Generate a verification tag
    verification_tag = generate_verification_tag(data)

    # Combine data and verification tag
    data_with_verification = f"{data}\n[VERIFY: {verification_tag}]"

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_with_verification)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("static/qr_code.png")

    return 'QR code generated successfully!'

def generate_verification_tag(data):
    sha256_hash = hashlib.sha256(data.encode()).hexdigest()
    return sha256_hash[:8]

if _name_ == '_main_':
    app.run(debug=True)
