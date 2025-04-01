#!/bin/bash

# Create a .env file with necessary API keys
echo "Creating .env file with placeholder API keys..."
cat > /home/ubuntu/trueflutter_prime_ai/.env << EOL
# OpenAI API Key - Replace with your actual key for production
OPENAI_API_KEY=sk_test_your_openai_key_here

# Stripe API Key - Replace with your actual key for production
STRIPE_API_KEY=sk_test_your_stripe_key_here
EOL

# Create placeholder voice clips for sample matches
echo "Creating placeholder voice clips for sample matches..."
mkdir -p /home/ubuntu/trueflutter_prime_ai/static/audio/sample_matches

# Create placeholder files for each sample match
for name in alex jordan taylor morgan jamie riley casey avery blake harper; do
    touch "/home/ubuntu/trueflutter_prime_ai/static/audio/sample_matches/${name}.mp3"
    echo "This is a placeholder for ${name}'s voice clip" > "/home/ubuntu/trueflutter_prime_ai/static/audio/sample_matches/${name}.mp3"
done

# Create a default audio message for AI responses when API key is not set
echo "Creating default audio message for AI responses..."
mkdir -p /home/ubuntu/trueflutter_prime_ai/static/audio
echo "This is a placeholder for AI voice response" > "/home/ubuntu/trueflutter_prime_ai/static/audio/default_message.mp3"

# Create directories for storing user data and documents
echo "Creating directories for user data and documents..."
mkdir -p /home/ubuntu/trueflutter_prime_ai/data
mkdir -p /home/ubuntu/trueflutter_prime_ai/static/documents

# Install wkhtmltopdf for PDF generation (required by pdfkit)
echo "Installing wkhtmltopdf for PDF generation..."
sudo apt-get update
sudo apt-get install -y wkhtmltopdf

echo "Setup complete! You can now run the application with:"
echo "cd /home/ubuntu/trueflutter_prime_ai && python3 app.py"
