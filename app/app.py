from flask import Flask, request, send_file, jsonify, render_template
import qrcode
from io import BytesIO
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Make sure you have this template

@app.route('/generate', methods=['POST'])
def generate_qr():
    try:
        # Get data from request
        request_data = request.get_json()
        if not request_data or 'data' not in request_data:
            return jsonify({"error": "Missing data parameter"}), 400
        
        data = request_data['data']
        if not isinstance(data, str) or not data.strip():
            return jsonify({"error": "Invalid data format"}), 400

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
        
    except Exception as e:
        app.logger.error(f"Error generating QR code: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
