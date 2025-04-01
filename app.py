import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from ai_matchmaker import AIMatchmaker
from match_engine import MatchRecommendationEngine
from document_generator import ProfileDocumentGenerator
from payment_system import PaymentSystem
import json
from datetime import datetime
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Directory to store user data
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Directory to store generated documents
DOCUMENTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/documents')
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

# Create sample audio directory
SAMPLE_MATCHES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/audio/sample_matches')
os.makedirs(SAMPLE_MATCHES_DIR, exist_ok=True)

# Initialize components
ai_matchmaker = AIMatchmaker()
match_engine = MatchRecommendationEngine(DATA_DIR)
document_generator = ProfileDocumentGenerator('templates', DOCUMENTS_DIR)
payment_system = PaymentSystem(app, DATA_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('firstName')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Create user data object
        user_data = {
            'first_name': first_name,
            'email': email,
            'phone': phone,
            'signup_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'pending_call',
            'user_id': str(uuid.uuid4())  # Generate unique ID for the user
        }
        
        # Generate a unique filename based on email
        filename = f"{email.replace('@', '_at_').replace('.', '_dot_')}.json"
        file_path = os.path.join(DATA_DIR, filename)
        
        # Save user data to file
        with open(file_path, 'w') as f:
            json.dump(user_data, f, indent=4)
        
        # Store user_id in session for conversation
        session['user_id'] = user_data['user_id']
        session['user_data'] = user_data
        
        # For API/AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': 'Thank you! We\'ll be in touch shortly to schedule your AI matchmaking call.',
                'redirect': url_for('thank_you', name=first_name)
            })
        
        # For regular form submissions, redirect to thank you page
        return redirect(url_for('thank_you', name=first_name))
    
    # If not POST, redirect to home
    return redirect(url_for('index'))

@app.route('/thank-you')
def thank_you():
    name = request.args.get('name', 'there')
    return render_template('thank_you.html', name=name)

@app.route('/conversation')
def conversation():
    # Check if user is in session
    if 'user_id' not in session or 'user_data' not in session:
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    user_data = session['user_data']
    
    return render_template('conversation.html', user=user_data)

@app.route('/api/start-conversation', methods=['POST'])
def start_conversation():
    if 'user_id' not in session or 'user_data' not in session:
        return jsonify({'error': 'No active user session'}), 400
    
    user_id = session['user_id']
    user_data = session['user_data']
    
    # Start conversation with AI matchmaker
    result = ai_matchmaker.start_conversation(user_id, user_data)
    
    return jsonify({
        'message': result['message'],
        'audio_url': '/' + result['audio_path'].replace('\\', '/'),
    })

@app.route('/api/send-message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return jsonify({'error': 'No active user session'}), 400
    
    user_id = session['user_id']
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Process user message and get AI response
    result = ai_matchmaker.process_user_response(user_id, user_message)
    
    return jsonify({
        'message': result['message'],
        'audio_url': '/' + result['audio_path'].replace('\\', '/'),
    })

@app.route('/api/generate-profile', methods=['POST'])
def generate_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'No active user session'}), 400
    
    # Generate user profile based on conversation
    profile = ai_matchmaker.generate_user_profile()
    
    # Find potential matches
    matches = match_engine.find_matches_for_user(profile)
    
    # Update user data with profile and matches
    if 'user_data' in session:
        user_data = session['user_data']
        user_data['profile'] = profile
        user_data['matches'] = matches
        user_data['status'] = 'profile_generated'
        
        # Generate profile document
        document_path = document_generator.generate_html_preview(user_data)
        if document_path:
            user_data['profile_document'] = document_path
        
        # Save updated user data
        email = user_data['email']
        filename = f"{email.replace('@', '_at_').replace('.', '_dot_')}.json"
        file_path = os.path.join(DATA_DIR, filename)
        
        with open(file_path, 'w') as f:
            json.dump(user_data, f, indent=4)
        
        session['user_data'] = user_data
    
    return jsonify({
        'success': True,
        'profile': profile,
        'matches': matches,
        'redirect': url_for('profile_preview')
    })

@app.route('/profile-preview')
def profile_preview():
    # Check if user is in session
    if 'user_id' not in session or 'user_data' not in session:
        return redirect(url_for('index'))
    
    user_data = session['user_data']
    
    # Check if profile has been generated
    if 'profile' not in user_data:
        return redirect(url_for('conversation'))
    
    return render_template('profile_preview.html', user=user_data)

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    # Check if user is in session
    if 'user_id' not in session or 'user_data' not in session:
        return redirect(url_for('index'))
    
    user_data = session['user_data']
    
    if request.method == 'POST':
        # Process subscription (in MVP, just update status)
        user_data['status'] = 'subscribed'
        user_data['subscription_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save updated user data
        email = user_data['email']
        filename = f"{email.replace('@', '_at_').replace('.', '_dot_')}.json"
        file_path = os.path.join(DATA_DIR, filename)
        
        with open(file_path, 'w') as f:
            json.dump(user_data, f, indent=4)
        
        session['user_data'] = user_data
        
        return redirect(url_for('subscription_success'))
    
    return render_template('subscribe.html', user=user_data)

@app.route('/subscription-success')
def subscription_success():
    # Check if user is in session
    if 'user_id' not in session or 'user_data' not in session:
        return redirect(url_for('index'))
    
    user_data = session['user_data']
    
    # Check if user has subscribed
    if user_data.get('status') != 'subscribed':
        return redirect(url_for('subscribe'))
    
    return render_template('subscription_success.html', user=user_data)

@app.route('/admin')
def admin():
    # Simple admin view to see registered users
    users = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json') and not filename.startswith('match_'):
            with open(os.path.join(DATA_DIR, filename), 'r') as f:
                user_data = json.load(f)
                users.append(user_data)
    
    return render_template('admin.html', users=users)

@app.route('/test-flow')
def test_flow():
    """Special route for testing the entire flow with sample data"""
    # Create a test user
    test_user = {
        'first_name': 'Test',
        'email': 'test@example.com',
        'phone': '555-123-4567',
        'signup_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'pending_call',
        'user_id': 'test_' + str(uuid.uuid4())
    }
    
    # Store in session
    session['user_id'] = test_user['user_id']
    session['user_data'] = test_user
    
    # Save to file
    filename = f"test_user.json"
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, 'w') as f:
        json.dump(test_user, f, indent=4)
    
    return redirect(url_for('conversation'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
