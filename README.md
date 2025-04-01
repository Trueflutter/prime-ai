# Trueflutter Prime AI - README

## Overview

Trueflutter Prime AI is an innovative matchmaking service that leverages artificial intelligence to automate and enhance the matchmaking process. This MVP demonstrates how AI can transform the traditional manual matchmaking approach into a scalable, efficient system that delivers personalized matches to clients.

## Features

- **Landing Page & User Registration**: Modern, responsive web interface for user onboarding
- **AI Conversation System**: Voice-based interaction powered by OpenAI's GPT-4o and Text-to-Speech API
- **Profile Generation System**: AI-driven analysis of conversation data to create comprehensive dating profiles
- **Match Recommendation Engine**: Algorithm for finding compatible matches based on multiple factors
- **Profile Document Generation**: Beautifully formatted profile summaries with potential matches
- **Payment Integration**: Stripe-powered subscription system for monetization

## Installation & Setup

1. Clone the repository or extract the provided files
2. Navigate to the project directory
3. Run the setup script:
   ```
   ./setup.sh
   ```
4. Update the `.env` file with your API keys:
   - OpenAI API key for AI conversation and text-to-speech
   - Stripe API key for payment processing

## Running the Application

1. Start the Flask application:
   ```
   python3 app.py
   ```
2. Open a web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Testing

1. Run the automated test script:
   ```
   ./test.sh
   ```
2. For manual testing, use the test flow route:
   ```
   http://localhost:5000/test-flow
   ```

## Demonstration

1. Run the demonstration script for a guided walkthrough:
   ```
   ./demo_script.sh
   ```
2. Follow the prompts to showcase each feature of the application

## Project Structure

- `app.py`: Main Flask application
- `ai_matchmaker.py`: AI conversation and profile generation
- `match_engine.py`: Match recommendation algorithm
- `document_generator.py`: Profile document generation
- `payment_system.py`: Stripe integration for subscriptions
- `templates/`: HTML templates for web pages
- `static/`: CSS, JavaScript, and media files
- `data/`: User and match data storage
- `setup.sh`: Environment setup script
- `test.sh`: Automated testing script
- `demo_script.sh`: Guided demonstration script
- `investor_demo.md`: Comprehensive documentation for investors

## Technology Stack

- **Backend**: Python with Flask framework
- **Frontend**: HTML5, CSS3, JavaScript
- **AI Services**: OpenAI GPT-4o and TTS API
- **Database**: JSON-based file storage (scalable to SQL database)
- **Payment Processing**: Stripe API
- **Document Generation**: HTML templates with PDF conversion

## Next Steps

1. User testing with real clients
2. AI enhancement and fine-tuning
3. Mobile app development
4. Marketing strategy development
5. Operations setup

## Budget Considerations

- **MVP Development**: Completed within $300 budget
- **Production Launch**: Estimated $5,000-$10,000 investment
- **Scale-Up Phase**: Additional $20,000-$30,000 investment

## Contact

For any questions or support, please contact the development team.

---

© 2025 Trueflutter Prime. All rights reserved.
