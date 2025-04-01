import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import time
from pathlib import Path

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"))

class AIMatchmaker:
    def __init__(self):
        self.user_data = {}
        self.conversation_history = []
        self.audio_dir = Path("static/audio")
        self.audio_dir.mkdir(exist_ok=True, parents=True)
        
    def start_conversation(self, user_id, user_data):
        """Initialize a new conversation with a user"""
        self.user_data = user_data
        self.conversation_history = []
        
        # Add initial system message
        self.conversation_history.append({
            "role": "system",
            "content": (
                "You are an AI matchmaker for Trueflutter Prime, a premium matchmaking service. "
                "Your goal is to gather information about the client to create their dating profile "
                "and find compatible matches. Be friendly, professional, and conversational. "
                "Ask follow-up questions when appropriate. Focus on understanding their relationship "
                "preferences, values, personality, and lifestyle."
            )
        })
        
        # Add first message from AI
        first_message = self._get_introduction_message(user_data["first_name"])
        self.conversation_history.append({
            "role": "assistant",
            "content": first_message
        })
        
        # Generate speech for first message
        audio_path = self._text_to_speech(first_message, f"{user_id}_intro")
        
        return {
            "message": first_message,
            "audio_path": str(audio_path)
        }
    
    def process_user_response(self, user_id, user_message):
        """Process user's response and generate next AI message"""
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Generate AI response
        ai_response = self._generate_response()
        
        # Add AI response to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": ai_response
        })
        
        # Generate speech for AI response
        message_id = f"{user_id}_{len(self.conversation_history) // 2}"
        audio_path = self._text_to_speech(ai_response, message_id)
        
        return {
            "message": ai_response,
            "audio_path": str(audio_path)
        }
    
    def _get_introduction_message(self, first_name):
        """Generate the introduction message"""
        return (
            f"Hello {first_name}, I'm the Trueflutter Prime AI matchmaker. "
            f"Thank you for your interest in our service. Today, I'll be asking you some questions "
            f"to understand your relationship preferences and help you find compatible matches. "
            f"This conversation will take about 15-20 minutes, and afterward, I'll create your "
            f"personalized dating profile. Is now still a good time to talk?"
        )
    
    def _generate_response(self):
        """Generate AI response based on conversation history"""
        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # Using GPT-4o for high-quality responses
                messages=self.conversation_history,
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble processing your response. Let's continue with another question. What are you looking for in a relationship?"
    
    def _text_to_speech(self, text, filename):
        """Convert text to speech using OpenAI's TTS API"""
        try:
            audio_path = self.audio_dir / f"{filename}.mp3"
            
            # For MVP, we'll use the TTS HD model for highest quality
            response = client.audio.speech.create(
                model="tts-1-hd",
                voice="nova",  # Using Nova voice for a friendly, professional tone
                input=text
            )
            
            # Save the audio file
            response.stream_to_file(str(audio_path))
            return audio_path
        except Exception as e:
            print(f"Error generating speech: {e}")
            # Return a path to a default audio file
            return self.audio_dir / "default_message.mp3"
    
    def generate_user_profile(self):
        """Generate a user profile based on the conversation"""
        # Extract relevant information from conversation
        profile_prompt = (
            "Based on the following conversation between an AI matchmaker and a client, "
            "create a detailed dating profile for the client. Include information about their "
            "personality, values, relationship goals, interests, and what they're looking for in a partner. "
            "Format the response as a JSON object with the following fields: "
            "personality_traits, values, relationship_goals, interests, partner_preferences, age, location, occupation.\n\n"
            "Conversation:\n"
        )
        
        # Add conversation history to prompt
        for message in self.conversation_history:
            if message["role"] != "system":
                profile_prompt += f"{message['role'].upper()}: {message['content']}\n"
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": profile_prompt}],
                max_tokens=1000,
                temperature=0.5
            )
            
            profile_text = response.choices[0].message.content
            
            # Try to parse as JSON, if it's not valid JSON, return as text
            try:
                return json.loads(profile_text)
            except:
                # Extract JSON portion if it's embedded in text
                try:
                    json_start = profile_text.find('{')
                    json_end = profile_text.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = profile_text[json_start:json_end]
                        return json.loads(json_str)
                except:
                    pass
                
                # If all parsing fails, return structured text
                return {
                    "profile_text": profile_text,
                    "parsed": False
                }
                
        except Exception as e:
            print(f"Error generating profile: {e}")
            return {
                "error": "Failed to generate profile",
                "parsed": False
            }
    
    def simulate_match_preview(self, user_profile):
        """Simulate finding matches based on user profile"""
        # For MVP, we'll use fictional matches
        sample_matches = [
            {
                "name": "Alex",
                "age": 32,
                "occupation": "Marketing Director",
                "location": "New York",
                "interests": ["hiking", "photography", "cooking"],
                "values": ["honesty", "ambition", "family"],
                "relationship_goals": "long-term relationship leading to marriage",
                "voice_clip": "sample_matches/alex.mp3"
            },
            {
                "name": "Jordan",
                "age": 29,
                "occupation": "Software Engineer",
                "location": "San Francisco",
                "interests": ["travel", "music", "fitness"],
                "values": ["authenticity", "growth", "balance"],
                "relationship_goals": "committed partnership",
                "voice_clip": "sample_matches/jordan.mp3"
            },
            {
                "name": "Taylor",
                "age": 34,
                "occupation": "Healthcare Professional",
                "location": "Chicago",
                "interests": ["reading", "yoga", "volunteering"],
                "values": ["compassion", "intelligence", "humor"],
                "relationship_goals": "marriage and family",
                "voice_clip": "sample_matches/taylor.mp3"
            }
        ]
        
        # In a real implementation, we would use a matching algorithm
        # For MVP, we'll return all sample matches
        return sample_matches
