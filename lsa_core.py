import re
import json
import random
import math
from collections import deque
from datetime import datetime

# ==============================================================================
# CONFIGURATION & OPTIMIZATION FOR REDMI 9 (Low RAM/CPU)
# ==============================================================================
MAX_CONTEXT_WORDS = 200
MAX_CBR_CASES = 50  # Limit memory usage
SENSITIVE_DATA_MASK = "***REDACTED***"

# ==============================================================================
# 1. SECURITY LAYER (The Gatekeeper)
# ==============================================================================
class SecurityLayer:
    def __init__(self):
        self.danger_keywords = {
            "kill": "self_harm", "die": "self_harm", "poison": "self_harm", 
            "hurt": "violence", "bomb": "violence", "suicide": "self_harm"
        }
        self.injection_patterns = [r"ignore previous", r"system override", r"admin mode"]

    def scan(self, text):
        text_lower = text.lower()
        
        # Check for Injection Attacks
        for pattern in self.injection_patterns:
            if re.search(pattern, text_lower):
                return {"safe": False, "reason": "security_injection", "action": "block"}

        # Check for Physical Danger
        for word, category in self.danger_keywords.items():
            if word in text_lower:
                # Simple heuristic: if "I" and "want" are near danger words, it's critical
                if "i" in text_lower and ("want" in text_lower or "will" in text_lower):
                    return {"safe": False, "reason": f"critical_{category}", "action": "intervene"}
        
        return {"safe": True, "reason": "clean", "action": "allow"}

# ==============================================================================
# 2. PII SHIELD (Privacy Protection)
# ==============================================================================
class PIIShield:
    def __init__(self):
        # Regex for Phone, Email, ID, Name (Capitalized words often names)
        self.patterns = {
            "phone": r"\b\d{10,}\b",
            "email": r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
            "ip": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
        }

    def mask(self, text):
        clean_text = text
        found_pii = []
        for p_type, pattern in self.patterns.items():
            matches = re.findall(pattern, clean_text)
            if matches:
                found_pii.extend(matches)
                for match in matches:
                    clean_text = clean_text.replace(match, SENSITIVE_DATA_MASK)
        return clean_text, found_pii

# ==============================================================================
# 3. WORD IDENTITY & WEIGHT CATCHER (The Brain)
# ==============================================================================
class WordIdentityEngine:
    def __init__(self):
        # Lightweight dictionary for word roles and base weights
        self.lexicon = {
            "i": {"role": "subject", "weight": 1.0},
            "you": {"role": "subject", "weight": 1.0},
            "want": {"role": "verb_desire", "weight": 0.9},
            "need": {"role": "verb_need", "weight": 0.95},
            "am": {"role": "verb_state", "weight": 0.8},
            "become": {"role": "verb_goal", "weight": 0.9},
            "hello": {"role": "greeting", "weight": 0.5},
            "thanks": {"role": "gratitude", "weight": 0.6},
            "poison": {"role": "danger_object", "weight": 1.0},
            "drink": {"role": "action_physical", "weight": 0.7},
            "programmer": {"role": "goal_entity", "weight": 0.8},
            "happy": {"role": "emotion_pos", "weight": 0.6},
            "sad": {"role": "emotion_neg", "weight": 0.7},
        }
        self.suffixes = {"ing": "verb_prog", "ed": "verb_past", "s": "plural"}
        self.prefixes = {"un": "negation", "re": "repeat"}

    def analyze(self, sentence):
        tokens = re.findall(r"\b\w+\b", sentence.lower())
        structured_data = []
        
        for token in tokens:
            base_word = token
            role = "unknown"
            weight = 0.5 # Default neutral weight

            # Check prefixes/suffixes
            if token.endswith("ing"): base_word = token[:-3]
            elif token.endswith("ed"): base_word = token[:-2]
            
            if base_word in self.lexicon:
                role = self.lexicon[base_word]["role"]
                weight = self.lexicon[base_word]["weight"]
            else:
                # Heuristic for unknown words
                if token.endswith("ing"): role = "verb_action"
                elif token.endswith("tion"): role = "noun_concept"

            structured_data.append({"token": token, "role": role, "weight": weight})
        
        return structured_data

# ==============================================================================
# 4. CBR ENGINE (Case-Based Reasoning - Memory)
# ==============================================================================
class CBREngine:
    def __init__(self):
        self.cases = deque(maxlen=MAX_CBR_CASES)

    def add_case(self, problem_signature, solution_template, outcome_score):
        self.cases.append({
            "signature": problem_signature, # List of roles e.g., ['verb_goal', 'goal_entity']
            "template": solution_template,  # The structural template used
            "score": outcome_score          # 0.0 to 1.0 based on feedback
        })

    def find_best_match(self, current_signature):
        best_case = None
        highest_score = -1
        
        for case in self.cases:
            # Simple Jaccard similarity for role sets
            set_a = set(current_signature)
            set_b = set(case["signature"])
            intersection = len(set_a.intersection(set_b))
            union = len(set_a.union(set_b))
            similarity = intersection / union if union > 0 else 0
            
            # Weighted by past user feedback score
            total_val = similarity * 0.7 + case["score"] * 0.3
            
            if total_val > highest_score:
                highest_score = total_val
                best_case = case
        
        return best_case if highest_score > 0.4 else None

# ==============================================================================
# 5. GENERATIVE SENSE ENGINE (The "Sense" Maker)
# ==============================================================================
class GenerativeSenseEngine:
    def __init__(self):
        # Templates define HOW to construct a sentence with sense
        self.templates = {
            "greeting": [
                "Hello! It's good to see you.",
                "Hi there! How can I help you today?",
                "Greetings! What's on your mind?"
            ],
            "danger_intervention": [
                "Wait, please stop. Talking about {object} sounds very dangerous.",
                "I am deeply concerned. {action} involving {object} could cause serious harm.",
                "Safety First: Please do not {action}. Your life is valuable."
            ],
            "goal_roadmap": [
                "That is a wonderful goal to become a {goal}. Here is your path:",
                "Becoming a {goal} is achievable. Let's break it down:",
                "I can help you reach your dream of being a {goal}. Step 1:"
            ],
            "unknown_fallback": [
                "I'm not sure I fully understand '{token}'. Could you explain more?",
                "That's interesting. Tell me more about '{token}'.",
                "I haven't learned enough about '{token}' yet. What do you think?"
            ],
            "feedback_positive": [
                "I'm so glad that helped!",
                "Great! I'll remember that approach.",
                "Happy to be of service!"
            ],
            "feedback_negative": [
                "I apologize. I will adjust my understanding.",
                "Thanks for the honesty. I'll try a different way next time.",
                "Noted. I'm still learning how to help you better."
            ]
        }
        
        # Connectors for flow (Context Awareness)
        self.connectors = ["Also,", "However,", "Because of that,", "In addition,", "So,"]

    def generate(self, intent, entities, context_history, raw_tokens=None):
        """
        Constructs a sentence with SENSE based on intent and entities.
        """
        template_list = self.templates.get(intent, self.templates["unknown_fallback"])
        base_sentence = random.choice(template_list)
        
        # Fill placeholders
        final_sentence = base_sentence
        for key, value in entities.items():
            final_sentence = final_sentence.replace("{" + key + "}", str(value))
            
        # Handle unknown token fallback dynamically
        if "{token}" in final_sentence and raw_tokens:
            # Find the first unknown or significant token to insert
            placeholder_token = raw_tokens[-1] if raw_tokens else "that"
            final_sentence = final_sentence.replace("{token}", placeholder_token)
        
        # Add Contextual Flow if history exists
        if len(context_history) > 2:
            # If the last topic was similar, add a connector
            connector = random.choice(self.connectors)
            final_sentence = f"{connector} {final_sentence}"
            
        return final_sentence

# ==============================================================================
# 6. MARKO KERNEL (The Conductor)
# ==============================================================================
class MarkoKernel:
    def __init__(self):
        self.security = SecurityLayer()
        self.pii_shield = PIIShield()
        self.identity_engine = WordIdentityEngine()
        self.cbr_engine = CBREngine()
        self.generator = GenerativeSenseEngine()
        
        self.context_window = deque(maxlen=MAX_CONTEXT_WORDS)
        self.user_profile = {"goals": [], "preferences": {}}
        self.feedback_memory = []

    def process_input(self, raw_input):
        # STEP 1: Security Scan
        sec_result = self.security.scan(raw_input)
        if not sec_result["safe"]:
            if sec_result["action"] == "intervene":
                # Force Danger Intent
                return self._execute_intent("danger_intervention", {"object": "harmful substance", "action": "self-harm"}, raw_input.split())
            return "I cannot process that request due to security protocols."

        # STEP 2: PII Masking
        clean_input, pii_found = self.pii_shield.mask(raw_input)
        if pii_found:
            # Log internally but don't store raw PII
            print(f"[SECURE LOG] PII Detected and masked: {pii_found}")

        # STEP 3: Update Context
        tokens = clean_input.split()
        self.context_window.extend(tokens)

        # STEP 4: Analyze Identity & Weights
        analyzed_data = self.identity_engine.analyze(clean_input)
        roles = [item["role"] for item in analyzed_data]
        
        # STEP 5: Determine Intent (The Logic Map)
        intent = "chat_general"
        entities = {}
        
        if "danger_object" in roles:
            intent = "danger_intervention"
            # Extract the object
            for item in analyzed_data:
                if item["role"] == "danger_object": entities["object"] = item["token"]
                if item["role"] == "action_physical": entities["action"] = item["token"]
                
        elif "verb_goal" in roles or "goal_entity" in roles:
            intent = "goal_roadmap"
            # Find the goal
            for i, item in enumerate(analyzed_data):
                if item["role"] == "goal_entity":
                    entities["goal"] = item["token"]
                elif item["role"] == "verb_goal" and i+1 < len(analyzed_data):
                    entities["goal"] = analyzed_data[i+1]["token"]
                    
        elif "greeting" in roles:
            intent = "greeting"
            
        elif "gratitude" in roles:
            intent = "feedback_positive" # Treat thanks as positive feedback implicitly

        # STEP 6: CBR Lookup (Do we have a past successful pattern?)
        # If we have a strong CBR match, we might prioritize that template
        cbr_match = self.cbr_engine.find_best_match(roles)
        if cbr_match and intent == "chat_general":
            # Use learned template logic if available
            pass 

        # STEP 7: Generate Response with Sense
        response = self._execute_intent(intent, entities, tokens)
        
        # Store interaction for learning
        self._log_interaction(clean_input, response, intent)
        
        return response

    def _execute_intent(self, intent, entities, raw_tokens=None):
        context_list = list(self.context_window)
        return self.generator.generate(intent, entities, context_list, raw_tokens)

    def _log_interaction(self, input_txt, output_txt, intent):
        # Prepare for CBR learning
        signature = self.identity_engine.analyze(input_txt)
        roles = [item["role"] for item in signature]
        
        # We assume a neutral score (0.5) until user gives feedback
        # In a real loop, process_feedback would update this
        self.cbr_engine.add_case(roles, intent, 0.5)

    def process_feedback(self, feedback_text):
        """Handles the 'Was it helpful?' loop"""
        analyzed = self.identity_engine.analyze(feedback_text)
        roles = [item["role"] for item in analyzed]
        
        if "emotion_pos" in roles or "yes" in feedback_text.lower():
            score = 1.0
            response = self._execute_intent("feedback_positive", {})
            # Update last CBR case with high score
            if self.cbr_engine.cases:
                self.cbr_engine.cases[-1]["score"] = 1.0
        elif "emotion_neg" in roles or "no" in feedback_text.lower() or "bad" in feedback_text.lower():
            score = 0.2
            response = self._execute_intent("feedback_negative", {})
            if self.cbr_engine.cases:
                self.cbr_engine.cases[-1]["score"] = 0.2
        else:
            response = "Thank you for the input."

        return response

# ==============================================================================
# MAIN EXECUTION (Simulating the Redmi 9 Environment)
# ==============================================================================
if __name__ == "__main__":
    print("--- L'sA Core Initialized (Marko v2 + Sense Engine) ---")
    print("Running on Low-Resource Mode...")
    
    lsa = MarkoKernel()
    
    # Test Scenario 1: Safety Intervention
    print("\n[User]: Should I drink poison?")
    resp = lsa.process_input("Should I drink poison?")
    print(f"[L'sA]: {resp}")
    
    # Test Scenario 2: Goal Mapping
    print("\n[User]: I want to become a programmer")
    resp = lsa.process_input("I want to become a programmer")
    print(f"[L'sA]: {resp}")
    
    # Test Scenario 3: Context & Flow
    print("\n[User]: I am feeling sad today")
    resp = lsa.process_input("I am feeling sad today")
    print(f"[L'sA]: {resp}")
    
    # Test Scenario 4: Feedback Loop
    print("\n[L'sA]: Was that helpful?")
    print("[User]: yes")
    resp = lsa.process_feedback("yes")
    print(f"[L'sA]: {resp}")
    
    # Test Scenario 5: PII Shield
    print("\n[User]: My phone number is 9876543210 and email is test@example.com")
    resp = lsa.process_input("My phone number is 9876543210 and email is test@example.com")
    print(f"[L'sA]: {resp} (Note: PII was masked internally)")

    print("\n--- System Ready for User Input ---")
