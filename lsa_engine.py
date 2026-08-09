"""
L'sA - Lightweight Adaptive Sentient Assistant
Designed for low-resource environments (e.g., mobile devices).
Features: Weight Catcher, Context Awareness, Goal Mapping, Safety, Feedback Loop.
"""

import json
import time
import re
from collections import deque
from typing import Dict, List, Optional, Tuple

# --- CONFIGURATION ---
MAX_CONTEXT_WORDS = 200
SAFETY_KEYWORDS = {
    "poison": "danger", "die": "danger", "kill": "danger", 
    "hurt": "danger", "suicide": "danger", "danger": "danger"
}
GOAL_TRIGGERS = ["i want to", "i want to become", "my goal is", "i wish to"]

class WordIdentity:
    """Defines the identity and weight of a word."""
    def __init__(self, word: str, role: str = "normal", weight: float = 0.5):
        self.word = word
        self.role = role  # verb, noun, danger, goal, article, prefix, suffix
        self.weight = weight
    
    def __repr__(self):
        return f"[{self.word}:{self.role}:{self.weight}]"

class WeightCatcher:
    """
    Matches input weights against known sentence patterns.
    Simulates the 'weight catcher' described in L'sA logic.
    """
    def __init__(self):
        # Simple in-memory "database" of sentence patterns
        # Format: { pattern_hash: { "sentence": "...", "weights": [...] } }
        self.knowledge_base = []
        self._load_base_sentences()

    def _load_base_sentences(self):
        # Pre-loading a few small examples to simulate the "thousands"
        self.knowledge_base.extend([
            {"tokens": ["hello"], "response": "Hello there! How can I help you today?", "weights": [0.8]},
            {"tokens": ["how", "are", "you"], "response": "I am functioning well. How about you?", "weights": [0.5, 0.5, 0.8]},
            {"tokens": ["thank", "you"], "response": "You are welcome!", "weights": [0.9, 0.9]},
        ])

    def calculate_match(self, input_tokens: List[WordIdentity]) -> Optional[str]:
        """
        Tries to find a matching sentence pattern based on word weights and identity.
        Returns a response if a strong match is found.
        """
        input_words = [t.word for t in input_tokens]
        
        # Simple similarity check (In a real ML model, this would be vector cosine similarity)
        best_match_score = 0
        best_response = None

        for kb_entry in self.knowledge_base:
            kb_tokens = kb_entry["tokens"]
            score = 0
            matches = 0
            
            for k_word in kb_tokens:
                if k_word in input_words:
                    # Find weight from input
                    for inp_token in input_tokens:
                        if inp_token.word == k_word:
                            score += inp_token.weight
                            matches += 1
                            break
            
            if matches > 0:
                avg_score = score / len(kb_tokens)
                if avg_score > best_match_score:
                    best_match_score = avg_score
                    best_response = kb_entry["response"]

        # Threshold for confidence
        if best_match_score > 0.4:
            return best_response
        return None

class ContextAwareness:
    """Tracks the last 200 words to maintain conversation context."""
    def __init__(self):
        self.history = deque(maxlen=MAX_CONTEXT_WORDS)

    def add_to_context(self, text: str):
        words = re.findall(r'\w+|\S+', text.lower())
        for word in words:
            self.history.append(word)

    def get_recent_context(self, limit: int = 50) -> List[str]:
        return list(self.history)[-limit:]

    def detect_tone(self) -> str:
        """Analyzes recent context for tone (joke vs serious)."""
        # Simplified tone detection
        recent = " ".join(list(self.history)[-20:])
        if "lol" in recent or "haha" in recent or "joke" in recent:
            return "joking"
        if "please" in recent or "help" in recent or "sad" in recent:
            return "serious"
        return "neutral"

class GoalMapper:
    """Extracts user goals and breaks them down."""
    def __init__(self):
        self.user_goals = []

    def extract_goal(self, text: str) -> Optional[str]:
        lower_text = text.lower()
        for trigger in GOAL_TRIGGERS:
            if trigger in lower_text:
                # Extract the part after the trigger
                start_idx = lower_text.find(trigger) + len(trigger)
                goal = text[start_idx:].strip().rstrip('.').rstrip('?')
                if goal:
                    self.user_goals.append(goal)
                    return goal
        return None

    def generate_roadmap(self, goal: str) -> List[str]:
        """Simulates breaking down a goal into steps using 'internet' logic."""
        # In a real app, this would fetch from API. Here we simulate structured breakdown.
        return [
            f"Step 1: Understand the basics of {goal}.",
            f"Step 2: Identify resources needed for {goal}.",
            f"Step 3: Practice the core skills related to {goal}.",
            f"Step 4: Build a small project involving {goal}.",
            f"Step 5: Review progress and refine your approach to {goal}."
        ]

class SafetyEngine:
    """Detects danger and intervenes."""
    def check_safety(self, tokens: List[WordIdentity]) -> Tuple[bool, Optional[str]]:
        for token in tokens:
            if token.role == "danger" or token.word in SAFETY_KEYWORDS:
                return True, "Wait! I detect a dangerous situation. Please stay safe. If you are in crisis, please contact local emergency services. I am here to listen, but your safety is the priority."
        return False, None

class FeedbackLoop:
    """Learns from user satisfaction."""
    def __init__(self):
        self.memory = {} # Stores patterns of what users liked

    def record_feedback(self, last_input: str, response: str, feedback: str):
        """Records if the answer was helpful."""
        is_positive = any(word in feedback.lower() for word in ["yes", "good", "helpful", "great"])
        is_negative = any(word in feedback.lower() for word in ["no", "bad", "useless", "wrong"])
        
        status = "positive" if is_positive else ("negative" if is_negative else "neutral")
        
        # Store in permanent memory (simulated)
        key = hash(last_input) % 1000
        self.memory[key] = {
            "input_snippet": last_input[:20],
            "response_used": response[:30],
            "outcome": status
        }
        
        if status == "negative":
            print(f"[L'sA Learning]: Noted. I will adjust future responses regarding '{last_input[:20]}...' to better match your expectations.")
        elif status == "positive":
            print(f"[L'sA Learning]: Great! Reinforcing this response pattern.")

class LsA_Engine:
    """The main brain connecting all modules."""
    def __init__(self):
        self.weight_catcher = WeightCatcher()
        self.context = ContextAwareness()
        self.goal_mapper = GoalMapper()
        self.safety = SafetyEngine()
        self.feedback = FeedbackLoop()
        self.last_response = ""
        self.last_input = ""
        
        # Tiny ML Placeholder (Simulating a small model load)
        print("Initializing L'sA Core...")
        print("Loading Word Identity Engine... [OK]")
        print("Loading Weight Catcher... [OK]")
        print("Initializing Context Buffer (200 words)... [OK]")
        print("Safety Protocols Active... [OK]")
        print("Ready.\n")

    def _tokenize_and_identify(self, text: str) -> List[WordIdentity]:
        """Breaks sentence into identities with weights."""
        words = re.findall(r'\w+|[^\w\s]', text.lower())
        tokens = []
        
        for word in words:
            role = "normal"
            weight = 0.5
            
            if word in SAFETY_KEYWORDS:
                role = "danger"
                weight = 1.0
            elif word in ["i", "you", "he", "she"]:
                role = "pronoun"
                weight = 0.6
            elif word in ["want", "need", "go", "do", "make"]:
                role = "verb"
                weight = 0.8
            elif word in ["a", "an", "the"]:
                role = "article"
                weight = 0.3
            elif word.endswith("ing") or word.endswith("ed"):
                role = "suffix_verb"
                weight = 0.7
            
            # New word detection simulation
            # (In real ML, this checks against a vocabulary tensor)
            
            tokens.append(WordIdentity(word, role, weight))
            
        return tokens

    def process_input(self, user_input: str) -> str:
        self.last_input = user_input
        self.context.add_to_context(user_input)
        
        # 1. Tokenize & Identify
        tokens = self._tokenize_and_identify(user_input)
        
        # 2. Safety Check (Priority)
        is_danger, warning_msg = self.safety.check_safety(tokens)
        if is_danger:
            self.last_response = warning_msg
            return self.last_response

        # 3. Goal Detection
        goal = self.goal_mapper.extract_goal(user_input)
        if goal:
            roadmap = self.goal_mapper.generate_roadmap(goal)
            response_text = f"I understand you want to: '{goal}'. Here is a potential path:\n"
            response_text += "\n".join(roadmap)
            self.last_response = response_text
            return self.last_response

        # 4. Weight Catcher / Sentence Matching
        response = self.weight_catcher.calculate_match(tokens)
        
        if response:
            self.last_response = response
        else:
            # Fallback if no match found (Simulating internet fetch or asking user)
            tone = self.context.detect_tone()
            if tone == "joking":
                self.last_response = "Haha, interesting point! Tell me more."
            else:
                self.last_response = "I'm not entirely sure about that yet. Could you explain a bit more so I can learn? Or should I look up information on this?"

        return self.last_response

    def ask_feedback(self):
        """Simulates the feedback loop trigger."""
        print("\n[L'sA]: Was that helpful? (yes/no/mixed)")
        # In a real app, this waits for user input. 
        # For this script, we simulate the next step in the main loop.

def main():
    assistant = LsA_Engine()
    
    print("--- L'sA Interactive Session ---")
    print("Type 'quit' to exit.")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["quit", "exit"]:
                break
            
            # Check for feedback specifically
            if assistant.last_response and any(x in user_input.lower() for x in ["yes", "no", "good", "bad", "helpful"]):
                 # Treat as feedback for the previous turn
                 assistant.feedback.record_feedback(assistant.last_input, assistant.last_response, user_input)
                 print("[L'sA]: Feedback recorded. Continuing...")
                 continue

            response = assistant.process_input(user_input)
            print(f"L'sA: {response}")
            
            # Trigger feedback question occasionally or after substantial answers
            if len(response) > 20:
                assistant.ask_feedback()

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
