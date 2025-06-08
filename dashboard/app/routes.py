from flask import Blueprint, render_template, jsonify
from app.monitor import scan_cookies  # Import your monitoring function

bp = Blueprint('main', __name__)

@bp.route('/')
def dashboard():
    # Get monitoring data (you'll replace this with real data)
    sample_data = {
        'total_cookies': 42,
        'secure_cookies': 38,
        'http_only': 35,
        'samesite_none': 5
    }
    return render_template('dashboard.html', data=sample_data)

@bp.route('/scan', methods=['POST'])
def scan():
    # This would trigger a new scan
    results = scan_cookies()  # Your monitoring function
    return jsonify(results)
