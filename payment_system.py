import os
import stripe
from flask import request, jsonify, redirect, url_for, session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PaymentSystem:
    def __init__(self, app, data_dir):
        self.app = app
        self.data_dir = data_dir
        
        # Initialize Stripe with API key
        # For MVP, we'll use test mode
        stripe.api_key = os.getenv("STRIPE_API_KEY", "sk_test_example")
        
        # Register routes
        self.register_routes()
    
    def register_routes(self):
        """Register payment-related routes with the Flask app"""
        
        @self.app.route('/api/create-checkout-session', methods=['POST'])
        def create_checkout_session():
            try:
                # Check if user is in session
                if 'user_id' not in session or 'user_data' not in session:
                    return jsonify({'error': 'No active user session'}), 400
                
                user_data = session['user_data']
                
                # Create a Stripe checkout session
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {
                                    'name': 'Trueflutter Prime Subscription',
                                    'description': 'Monthly matchmaking service',
                                },
                                'unit_amount': 4900,  # $49.00
                                'recurring': {
                                    'interval': 'month',
                                }
                            },
                            'quantity': 1,
                        },
                    ],
                    mode='subscription',
                    success_url=request.host_url + 'payment-success?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.host_url + 'subscribe',
                    client_reference_id=user_data['user_id'],
                    customer_email=user_data['email'],
                )
                
                return jsonify({'id': checkout_session.id})
            
            except Exception as e:
                return jsonify({'error': str(e)}), 400
        
        @self.app.route('/payment-success')
        def payment_success():
            # Get the checkout session ID
            session_id = request.args.get('session_id')
            
            if not session_id:
                return redirect(url_for('subscribe'))
            
            try:
                # Retrieve the checkout session
                checkout_session = stripe.checkout.Session.retrieve(session_id)
                
                # Update user data with subscription info
                if 'user_data' in session:
                    user_data = session['user_data']
                    user_data['status'] = 'subscribed'
                    user_data['subscription_date'] = checkout_session.created
                    user_data['subscription_id'] = checkout_session.subscription
                    
                    # Save updated user data
                    self._update_user_data(user_data)
                    
                    session['user_data'] = user_data
                
                return redirect(url_for('subscription_success'))
            
            except Exception as e:
                print(f"Error processing payment success: {e}")
                return redirect(url_for('subscribe'))
    
    def _update_user_data(self, user_data):
        """Update user data in the database"""
        try:
            email = user_data['email']
            filename = f"{email.replace('@', '_at_').replace('.', '_dot_')}.json"
            file_path = os.path.join(self.data_dir, filename)
            
            import json
            with open(file_path, 'w') as f:
                json.dump(user_data, f, indent=4)
                
            return True
        
        except Exception as e:
            print(f"Error updating user data: {e}")
            return False
    
    def process_subscription(self, user_data, payment_details):
        """Process a subscription payment (simplified for MVP)"""
        try:
            # For MVP, we'll simulate a successful payment
            # In production, this would integrate with Stripe API
            
            # Update user data
            user_data['status'] = 'subscribed'
            user_data['subscription_date'] = os.path.join(self.data_dir, 'subscriptions.json')
            
            # Save updated user data
            self._update_user_data(user_data)
            
            return {
                'success': True,
                'message': 'Subscription successful',
                'subscription_id': 'sub_' + os.urandom(8).hex()
            }
        
        except Exception as e:
            print(f"Error processing subscription: {e}")
            return {
                'success': False,
                'message': f'Error processing subscription: {str(e)}'
            }
