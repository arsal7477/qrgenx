import time 
import os
from flask import Flask, request, send_file, jsonify
import qrcode
from io import BytesIO
from prometheus_client import make_wsgi_app, Counter, Gauge
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import Counter, Gauge


app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)
REQUEST_TIME = Gauge(
    'http_request_duration_seconds',
    'HTTP request duration in seconds'
)

@app.route('/health')
def health_check():
    REQUEST_COUNT.labels('GET', '/health', '200').inc()
    return jsonify({"status": "healthy"}), 200

@app.route('/generate', methods=['POST'])
def generate_qr():
    start_time = time.time()
    data = request.json.get('data')
    
    if not data:
        REQUEST_COUNT.labels('POST', '/generate', '400').inc()
        return jsonify({"error": "Missing data parameter"}), 400
    
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        REQUEST_COUNT.labels('POST', '/generate', '200').inc()
        REQUEST_TIME.set(time.time() - start_time)
        return send_file(img_io, mimetype='image/png')
    
    except Exception as e:
        REQUEST_COUNT.labels('POST', '/generate', '500').inc()
        return jsonify({"error": str(e)}), 500

# Add Prometheus WSGI middleware
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
