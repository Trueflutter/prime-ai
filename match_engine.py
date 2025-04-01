import json
import os
import random
from pathlib import Path
import numpy as np
from datetime import datetime

class MatchRecommendationEngine:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.sample_matches_dir = Path("static/audio/sample_matches")
        self.sample_matches_dir.mkdir(exist_ok=True, parents=True)
        self.create_sample_matches()
        
    def create_sample_matches(self):
        """Create sample match profiles for the MVP"""
        sample_matches = [
            {
                "id": "match_001",
                "name": "Alex",
                "age": 32,
                "gender": "male",
                "occupation": "Marketing Director",
                "location": "New York",
                "interests": ["hiking", "photography", "cooking", "travel", "reading"],
                "values": ["honesty", "ambition", "family", "communication", "growth"],
                "personality_traits": ["outgoing", "creative", "analytical"],
                "relationship_goals": "long-term relationship leading to marriage",
                "voice_clip": "sample_matches/alex.mp3"
            },
            {
                "id": "match_002",
                "name": "Jordan",
                "age": 29,
                "gender": "female",
                "occupation": "Software Engineer",
                "location": "San Francisco",
                "interests": ["travel", "music", "fitness", "technology", "hiking"],
                "values": ["authenticity", "growth", "balance", "independence", "creativity"],
                "personality_traits": ["analytical", "curious", "adventurous"],
                "relationship_goals": "committed partnership",
                "voice_clip": "sample_matches/jordan.mp3"
            },
            {
                "id": "match_003",
                "name": "Taylor",
                "age": 34,
                "gender": "non-binary",
                "occupation": "Healthcare Professional",
                "location": "Chicago",
                "interests": ["reading", "yoga", "volunteering", "cooking", "art"],
                "values": ["compassion", "intelligence", "humor", "honesty", "balance"],
                "personality_traits": ["empathetic", "thoughtful", "organized"],
                "relationship_goals": "marriage and family",
                "voice_clip": "sample_matches/taylor.mp3"
            },
            {
                "id": "match_004",
                "name": "Morgan",
                "age": 31,
                "gender": "female",
                "occupation": "Financial Analyst",
                "location": "Boston",
                "interests": ["running", "investing", "travel", "cooking", "podcasts"],
                "values": ["ambition", "stability", "honesty", "family", "health"],
                "personality_traits": ["determined", "practical", "reliable"],
                "relationship_goals": "long-term partnership with potential for marriage",
                "voice_clip": "sample_matches/morgan.mp3"
            },
            {
                "id": "match_005",
                "name": "Jamie",
                "age": 28,
                "gender": "male",
                "occupation": "Graphic Designer",
                "location": "Los Angeles",
                "interests": ["art", "surfing", "photography", "music", "hiking"],
                "values": ["creativity", "freedom", "authenticity", "growth", "passion"],
                "personality_traits": ["creative", "laid-back", "optimistic"],
                "relationship_goals": "serious relationship with the right person",
                "voice_clip": "sample_matches/jamie.mp3"
            },
            {
                "id": "match_006",
                "name": "Riley",
                "age": 33,
                "gender": "female",
                "occupation": "Environmental Scientist",
                "location": "Portland",
                "interests": ["hiking", "sustainability", "gardening", "reading", "kayaking"],
                "values": ["environmental consciousness", "integrity", "adventure", "learning", "community"],
                "personality_traits": ["passionate", "thoughtful", "outdoorsy"],
                "relationship_goals": "committed relationship with shared values",
                "voice_clip": "sample_matches/riley.mp3"
            },
            {
                "id": "match_007",
                "name": "Casey",
                "age": 30,
                "gender": "male",
                "occupation": "Chef",
                "location": "Austin",
                "interests": ["cooking", "food exploration", "travel", "music", "fitness"],
                "values": ["creativity", "passion", "family", "cultural appreciation", "balance"],
                "personality_traits": ["passionate", "adventurous", "warm"],
                "relationship_goals": "marriage and family in the future",
                "voice_clip": "sample_matches/casey.mp3"
            },
            {
                "id": "match_008",
                "name": "Avery",
                "age": 27,
                "gender": "non-binary",
                "occupation": "UX Designer",
                "location": "Seattle",
                "interests": ["design", "hiking", "photography", "gaming", "coffee"],
                "values": ["creativity", "inclusivity", "growth", "authenticity", "balance"],
                "personality_traits": ["creative", "analytical", "empathetic"],
                "relationship_goals": "meaningful connection with long-term potential",
                "voice_clip": "sample_matches/avery.mp3"
            },
            {
                "id": "match_009",
                "name": "Blake",
                "age": 35,
                "gender": "male",
                "occupation": "Architect",
                "location": "Denver",
                "interests": ["architecture", "skiing", "hiking", "design", "travel"],
                "values": ["creativity", "ambition", "balance", "family", "integrity"],
                "personality_traits": ["detail-oriented", "thoughtful", "driven"],
                "relationship_goals": "marriage and building a life together",
                "voice_clip": "sample_matches/blake.mp3"
            },
            {
                "id": "match_010",
                "name": "Harper",
                "age": 29,
                "gender": "female",
                "occupation": "Elementary School Teacher",
                "location": "Minneapolis",
                "interests": ["education", "reading", "baking", "hiking", "volunteering"],
                "values": ["compassion", "family", "growth", "kindness", "stability"],
                "personality_traits": ["nurturing", "patient", "energetic"],
                "relationship_goals": "marriage and starting a family",
                "voice_clip": "sample_matches/harper.mp3"
            }
        ]
        
        # Save sample matches to files
        for match in sample_matches:
            match_file = self.data_dir / f"match_{match['id']}.json"
            with open(match_file, 'w') as f:
                json.dump(match, f, indent=4)
                
        # Create a placeholder for sample voice clips
        self.create_sample_voice_clips()
        
        return sample_matches
    
    def create_sample_voice_clips(self):
        """Create placeholder text files for sample voice clips"""
        sample_names = ["alex", "jordan", "taylor", "morgan", "jamie", "riley", "casey", "avery", "blake", "harper"]
        
        for name in sample_names:
            voice_clip_path = self.sample_matches_dir / f"{name}.mp3"
            # Create an empty file as a placeholder
            # In a real implementation, these would be actual audio files
            if not voice_clip_path.exists():
                with open(voice_clip_path, 'w') as f:
                    f.write(f"This is a placeholder for {name}'s voice clip")
    
    def get_all_matches(self):
        """Get all available matches from the database"""
        matches = []
        for file in self.data_dir.glob("match_*.json"):
            with open(file, 'r') as f:
                match_data = json.load(f)
                matches.append(match_data)
        return matches
    
    def find_matches_for_user(self, user_profile, num_matches=3):
        """Find compatible matches for a user based on their profile"""
        # For MVP, we'll use a simple matching algorithm
        # In a production system, this would be more sophisticated
        
        # Get all available matches
        all_matches = self.get_all_matches()
        
        # If user_profile is not properly parsed, return random matches
        if not isinstance(user_profile, dict) or user_profile.get('parsed') is False:
            return random.sample(all_matches, min(num_matches, len(all_matches)))
        
        # Extract user preferences
        try:
            user_interests = user_profile.get('interests', [])
            user_values = user_profile.get('values', [])
            user_relationship_goals = user_profile.get('relationship_goals', '')
            
            # Calculate compatibility scores
            scored_matches = []
            for match in all_matches:
                score = 0
                
                # Interest compatibility (30%)
                interest_overlap = set(user_interests).intersection(set(match['interests']))
                interest_score = len(interest_overlap) / max(len(user_interests), 1) * 30
                
                # Values compatibility (40%)
                value_overlap = set(user_values).intersection(set(match['values']))
                value_score = len(value_overlap) / max(len(user_values), 1) * 40
                
                # Relationship goals compatibility (30%)
                # Simple text matching - in production would use NLP
                if user_relationship_goals and any(goal in user_relationship_goals.lower() for goal in match['relationship_goals'].lower().split()):
                    relationship_score = 30
                else:
                    relationship_score = 0
                
                # Total score
                total_score = interest_score + value_score + relationship_score
                
                scored_matches.append((match, total_score))
            
            # Sort by score and get top matches
            scored_matches.sort(key=lambda x: x[1], reverse=True)
            top_matches = [match for match, score in scored_matches[:num_matches]]
            
            return top_matches
            
        except Exception as e:
            print(f"Error finding matches: {e}")
            # Fallback to random selection
            return random.sample(all_matches, min(num_matches, len(all_matches)))
    
    def generate_match_report(self, user_profile, matches):
        """Generate a report explaining why matches were selected"""
        report = {
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "matches": []
        }
        
        for match in matches:
            match_report = {
                "name": match['name'],
                "compatibility_reasons": []
            }
            
            # Add interest overlap
            if 'interests' in user_profile:
                interest_overlap = set(user_profile['interests']).intersection(set(match['interests']))
                if interest_overlap:
                    match_report["compatibility_reasons"].append(
                        f"You both enjoy {', '.join(interest_overlap)}"
                    )
            
            # Add value overlap
            if 'values' in user_profile:
                value_overlap = set(user_profile['values']).intersection(set(match['values']))
                if value_overlap:
                    match_report["compatibility_reasons"].append(
                        f"You share these values: {', '.join(value_overlap)}"
                    )
            
            # Add relationship goals compatibility
            if 'relationship_goals' in user_profile and 'relationship_goals' in match:
                match_report["compatibility_reasons"].append(
                    f"Your relationship goals align: You're looking for {user_profile['relationship_goals']} and {match['name']} wants {match['relationship_goals']}"
                )
            
            report["matches"].append(match_report)
        
        return report
