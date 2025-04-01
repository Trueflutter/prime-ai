# AI Voice Service Research Findings

## OpenAI Text-to-Speech API

### Pricing
- Standard TTS Model: $0.015 per 1,000 characters
- TTS HD Model (higher quality): $0.030 per 1,000 characters

### Advantages
- Cost-effective for our use case
- High-quality voices
- Easy integration with other OpenAI services
- Reliable API with good documentation

### Considerations
- Character-based pricing means we need to estimate conversation lengths
- For a 5-minute conversation (approximately 5,000 characters):
  - Standard: $0.075
  - HD: $0.15

## Eleven Labs

### Pricing
- Free tier: 10,000 credits/month
- Starter plan available
- Pro plan: $99/month for 500,000 credits
- Conversational AI calls: 10 cents per minute (Creator/Pro plans)
- Conversational AI calls: 8 cents per minute (Business annual plan)

### Advantages
- Highly realistic voices
- Specialized in conversational AI
- Offers real-time API with low latency
- Good for telephony applications

### Considerations
- Generally more expensive than OpenAI
- Credit-based system requires careful management
- Better suited for production environments than MVPs

## Recommendation

For our MVP with a $300 budget constraint, **OpenAI's Text-to-Speech API** appears to be the most cost-effective solution:

1. We can use the HD model for the highest quality
2. Estimated cost for 100 simulated conversations (5 minutes each):
   - 100 conversations × 5,000 characters × $0.030/1,000 characters = $15
   
3. This leaves substantial budget for other development aspects and potential integration with telephony services

For the initial MVP, we can implement:
- Text-to-speech for the AI agent's side of the conversation
- Simulated conversation flow with pre-recorded responses
- Profile generation based on conversation data
- Match recommendation from a sample database

As the product proves successful, upgrading to Eleven Labs for production would be a natural progression, especially for the telephony integration.
