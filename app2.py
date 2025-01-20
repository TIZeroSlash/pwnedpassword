from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import hashlib
import os
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class PasswordCheckHistory(db.Model):
    __tablename__ = 'password_check_history'
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(40), nullable=False)  # Store SHA-1 hash
    breach_count = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Helper function to check password using the Pwned Passwords API
def check_password(password):
    """Check if a password has been pwned and return breach count."""
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    # Check if password hash is already in the database
    existing_entry = PasswordCheckHistory.query.filter_by(password_hash=sha1_hash).first()
    if existing_entry:
        return existing_entry.breach_count

    # If not in the database, check against the Pwned Passwords API
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Error fetching data from Pwned Passwords API")

    # Parse response from API
    hashes = (line.split(':') for line in response.text.splitlines())
    breach_count = 0
    for h, count in hashes:
        if h == suffix:
            breach_count = int(count)
            break

    # Save the result to the database
    new_entry = PasswordCheckHistory(password_hash=sha1_hash, breach_count=breach_count)
    db.session.add(new_entry)
    db.session.commit()

    return breach_count

# Routes
@app.route('/check_password', methods=['POST'])
def api_check_password():
    """API route to check if a password has been pwned."""
    data = request.json
    password = data.get('password')

    if not password:
        return jsonify({"message": "Password is required"}), 400

    breach_count = check_password(password)
    if breach_count > 0:
        return jsonify({"message": f"Oh no — pwned! This password has been seen {breach_count:,} times before."})
    else:
        return jsonify({"message": "Good news — no pwnage found! This password has not been seen in any breaches."})

@app.route('/history', methods=['GET'])
def get_history():
    """API route to get the history of password checks."""
    history = PasswordCheckHistory.query.order_by(PasswordCheckHistory.timestamp.desc()).all()
    response = [{"password_hash": h.password_hash, "breach_count": h.breach_count, "timestamp": h.timestamp} for h in history]
    return jsonify(response)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main route to render the web interface."""
    message = None
    history = get_history()

    if request.method == 'POST':
        password = request.form.get('password')
        if not password:
            message = "Please enter a password."
        else:
            try:
                breach_count = check_password(password)
                if breach_count > 0:
                    message = f"Oh no — pwned! This password has been seen {breach_count:,} times before."
                else:
                    message = "Good news — no pwnage found! This password has not been seen in any breaches."

            except Exception as e:
                message = f"An error occurred: {str(e)}"
    return render_template('index.html', message=message, history=history)

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize database tables
    app.run(host='0.0.0.0', port=5000, debug=True)
