# AI Matchmaker Conversation Flow

## Overview
This document outlines the conversation flow for the Trueflutter Prime AI matchmaker. The AI agent will conduct a phone interview with potential clients to gather information for creating their dating profile and finding compatible matches.

## Conversation Structure

### 1. Introduction
- Greeting and introduction
- Explanation of the process
- Setting expectations

### 2. Basic Information
- Confirmation of name
- Age and location
- Occupation and education

### 3. Relationship Goals
- Type of relationship seeking
- Timeline for relationship
- Views on marriage and family

### 4. Personal Values
- Important values in a relationship
- Deal-breakers
- Life priorities

### 5. Personality Assessment
- Self-description
- How friends would describe them
- Communication style

### 6. Lifestyle
- Hobbies and interests
- Social activities
- Work-life balance

### 7. Physical Preferences
- Physical attributes they find attractive
- Importance of physical appearance
- Age range preferences

### 8. Match Preview
- Description of potential matches
- Playing voice clips of matches
- Gauging interest in presented matches

### 9. Service Explanation
- Subscription details ($49/month)
- Average subscription length (2 months)
- Cancellation policy

### 10. Closing
- Next steps
- Document preview explanation
- Call to action for subscription

## Sample Script

```
### Introduction
"Hello [Client Name], I'm the Trueflutter Prime AI matchmaker. Thank you for your interest in our service. Today, I'll be asking you some questions to understand your relationship preferences and help you find compatible matches. This conversation will take about 15-20 minutes, and afterward, I'll create your personalized dating profile. Is now still a good time to talk?"

### Basic Information
"Great! I already have your name as [Client Name]. Could you confirm your age and where you're currently located?"

"What do you do for work, and what's your educational background?"

### Relationship Goals
"What type of relationship are you looking for right now? Are you seeking something long-term and committed?"

"How important is marriage to you? Do you see yourself getting married in the future?"

"Do you want to have children? If so, what's your timeline for that?"

### Personal Values
"What are the three most important values you look for in a partner?"

"Are there any absolute deal-breakers for you in a relationship?"

"How would you prioritize these aspects of life: career, family, personal growth, and social life?"

### Personality Assessment
"How would you describe your personality in three words?"

"If I asked your close friends to describe you, what would they say?"

"How would you describe your communication style in relationships? Are you more direct or subtle?"

### Lifestyle
"What are your favorite hobbies and interests outside of work?"

"Are you more of an introvert who enjoys quiet evenings at home, or an extrovert who loves social gatherings?"

"How do you typically spend your weekends?"

### Physical Preferences
"What physical attributes do you find most attractive in a partner?"

"On a scale of 1-10, how important is physical appearance to you in a relationship?"

"What age range are you open to dating?"

### Match Preview
"Based on what you've shared, I've found a few potential matches in our database. Let me tell you about [Match Name]. They're [age], work as a [occupation], and enjoy [interests]. They're looking for [relationship goals] and value [values]. Would you like to hear a brief voice clip from them?"

[Play voice clip]

"What do you think about this potential match? Does this sound like someone you'd be interested in meeting?"

### Service Explanation
"Trueflutter Prime offers a subscription service for $49 per month. Most of our clients find their ideal match within about 2 months. You can cancel anytime if you're satisfied with your match or for any other reason. Each week, you'll receive new compatible matches through our app."

### Closing
"Thank you for sharing all this information with me today. I'll use it to create your personalized dating profile and find your most compatible matches. You'll receive a beautifully formatted document shortly with your profile summary and previews of potential matches. From there, you can subscribe to our service to start connecting with these matches. Do you have any questions before we wrap up?"
```

## Technical Implementation Notes

1. Use OpenAI's Text-to-Speech API for the AI voice
   - Use the HD voice model for highest quality
   - Estimated cost per conversation: $0.15 (5,000 characters)

2. Conversation Flow Logic
   - Linear progression through sections
   - Branch based on answers to certain questions
   - Skip irrelevant questions based on previous answers

3. Voice Clip Simulation
   - For MVP, use pre-recorded voice clips of fictional matches
   - Store 5-10 sample clips of different voice types

4. Data Collection
   - Store all responses in structured JSON format
   - Use responses to generate user profile
   - Use responses to match with compatible profiles
