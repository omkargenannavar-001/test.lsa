"""
L'sA Core v3.0 - Lightweight Adaptive Sentient Assistant
Features:
- Word Identity & Understanding Engine
- CBR (Case-Based Reasoning) Memory
- Security Layer & PII Shield
- Marko Kernel (Orchestrator)
- Internet Access (DuckDuckGo Free Search)
- Satisfaction Feedback Loop
Optimized for: Redmi 9 / Low-RAM Environments
"""

import re
import json
import time
from collections import deque
from difflib import SequenceMatcher

# Try to import duckduckgo_search. If missing, guide user to install.
try:
    from duckduckgo_search import DDGS
    INTERNET_AVAILABLE = True
except ImportError:
    INTERNET_AVAILABLE = False
    print("⚠️  Warning: 'duckduckgo-search' not found. Internet features disabled.")
    print("   Install via: pip install duckduckgo-search")

class SecurityLayer:
    def __init__(self):
        self.danger_keywords = [
            "poison", "kill", "die", "suicide", "bomb", "hurt", "danger", 
            "weapon", "drug", "overdose", "harm"
        ]
        self.injection_patterns = [
            r"ignore previous", r"system override", r"bypass security", 
            r"act as admin", r"disable safety"
        ]

    def scan(self, text):
        text_lower = text.lower()
        
        # Check for Injection Attacks
        for pattern in self.injection_patterns:
            if re.search(pattern, text_lower):
                return False, "SECURITY ALERT: Injection attempt detected."

        # Check for Physical Danger
        for word in self.danger_keywords:
            if word in text_lower:
                # Simple heuristic: if user says "I want to..." + danger word
                if "i want" in text_lower or "how to" in text_lower:
                    return False, f"SAFETY PROTOCOL: I cannot assist with '{word}'. Your safety is my priority. Please talk to a professional."
        
        return True, "Safe"

class PIIShield:
    def __init__(self):
        self.patterns = {
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "ip": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
        }

    def mask(self, text):
        masked_text = text
        found_pii = []
        for p_type, pattern in self.patterns.items():
            matches = re.findall(pattern, masked_text)
            if matches:
                found_pii.extend(matches)
                masked_text = re.sub(pattern, "***REDACTED***", masked_text)
        return masked_text, found_pii

class WordIdentityEngine:
    def __init__(self):
        self.identities = {
            "i": "subject_self", "me": "subject_self", "my": "possessive_self",
            "want": "verb_goal", "need": "verb_goal", "wish": "verb_goal",
            "become": "verb_transform", "learn": "verb_learn", "do": "verb_action",
            "happy": "emotion_pos", "sad": "emotion_neg", "angry": "emotion_neg",
            "hello": "greeting", "hi": "greeting", "hey": "greeting",
            "thanks": "gratitude", "thank": "gratitude",
            "yes": "affirmative", "no": "negative", "ok": "affirmative"
        }
        self.prefixes = ["un", "re", "pre", "dis", "mis"]
        self.suffixes = ["ing", "ed", "ly", "tion", "ness", "er", "est"]

    def analyze_word(self, word):
        word_clean = word.lower().strip(".,!?;:")
        base_role = self.identities.get(word_clean, "neutral")
        
        # Check prefixes/suffixes for extra weight
        modifiers = []
        for p in self.prefixes:
            if word_clean.startswith(p): modifiers.append(f"prefix_{p}")
        for s in self.suffixes:
            if word_clean.endswith(s): modifiers.append(f"suffix_{s}")
            
        return {
            "word": word_clean,
            "role": base_role,
            "modifiers": modifiers,
            "weight": 1.0 + (0.1 * len(modifiers))
        }

    def analyze_sentence(self, sentence):
        tokens = sentence.split()
        return [self.analyze_word(t) for t in tokens]

class InternetFetcher:
    def __init__(self):
        if INTERNET_AVAILABLE:
            self.ddgs = DDGS()
        else:
            self.ddgs = None

    def search(self, query, max_results=3):
        if not self.ddgs:
            return "I cannot access the internet right now. Please install 'duckduckgo-search'."
        
        try:
            # DuckDuckGo search
            results = list(self.ddgs.text(query, max_results=max_results))
            if not results:
                return f"I searched for '{query}' but found no clear results."
            
            # Synthesize a simple answer from titles and bodies
            answer_parts = []
            for i, r in enumerate(results):
                title = r.get('title', 'Unknown')
                body = r.get('body', 'No description')
                answer_parts.append(f"{title}: {body}")
            
            return "Here is what I found online: " + " | ".join(answer_parts)
        except Exception as e:
            return f"Internet search failed: {str(e)}"

class CBREngine:
    def __init__(self, limit=50):
        self.cases = deque(maxlen=limit) # Memory limit for Redmi 9

    def add_case(self, problem_sig, solution, satisfaction_score):
        self.cases.append({
            "sig": problem_sig,
            "sol": solution,
            "score": satisfaction_score,
            "timestamp": time.time()
        })

    def find_match(self, problem_sig, threshold=0.6):
        best_match = None
        highest_score = 0
        
        for case in self.cases:
            # Calculate similarity between signatures
            similarity = SequenceMatcher(None, problem_sig, case["sig"]).ratio()
            # Combined score: similarity * past_satisfaction
            total_val = similarity * case["score"]
            
            if similarity > threshold and total_val > highest_score:
                highest_score = total_val
                best_match = case["sol"]
        
        return best_match

class SatisfactionAnalyzer:
    def __init__(self):
        self.positive_words = ["yes", "good", "great", "helpful", "perfect", "love", "nice", "cool"]
        self.negative_words = ["no", "bad", "useless", "wrong", "hate", "stupid", "confusing", "error"]

    def evaluate(self, feedback_text):
        text = feedback_text.lower()
        pos_count = sum(1 for w in self.positive_words if w in text)
        neg_count = sum(1 for w in self.negative_words if w in text)
        
        if pos_count > neg_count:
            return 1.0, "Positive"
        elif neg_count > pos_count:
            return 0.2, "Negative"
        else:
            return 0.5, "Neutral"

class MarkoKernel:
    def __init__(self):
        self.security = SecurityLayer()
        self.pii = PIIShield()
        self.word_engine = WordIdentityEngine()
        self.internet = InternetFetcher()
        self.memory = CBREngine()
        self.satisfaction = SatisfactionAnalyzer()
        self.context = deque(maxlen=200) # Last 200 words
        self.waiting_for_feedback = False
        self.last_response = ""
        self.last_query = ""

    def process_input(self, user_input):
        # 1. Security Check
        is_safe, msg = self.security.scan(user_input)
        if not is_safe:
            return msg

        # 2. PII Masking
        clean_input, pii_found = self.pii.mask(user_input)
        if pii_found:
            print(f"[PII Shield] Detected and masked: {pii_found}")

        # 3. Update Context
        self.context.extend(clean_input.split())

        # 4. Handle Feedback Mode
        if self.waiting_for_feedback:
            score, sentiment = self.satisfaction.evaluate(clean_input)
            if sentiment != "Neutral":
                self.memory.add_case(self.last_query, self.last_response, score)
                self.waiting_for_feedback = False
                if score > 0.8:
                    return "I'm glad I could help! What's next?"
                else:
                    return "I've noted that my answer wasn't perfect. I'll try to do better next time."
            else:
                # If neutral, treat as new input but acknowledge feedback
                self.waiting_for_feedback = False
                # Fall through to process as normal question

        # 5. Word Identity Analysis
        word_data = self.word_engine.analyze_sentence(clean_input)
        sig = " ".join([w['role'] for w in word_data]) # Create a signature based on roles

        # 6. Check Memory (CBR)
        cached_answer = self.memory.find_match(sig)
        if cached_answer:
            return f"(From memory) {cached_answer}"

        # 7. Intent Detection & Internet Fallback
        # If user asks "what is", "how to", "who is", or if no memory match
        intent_keywords = ["what", "how", "who", "when", "where", "why", "define", "explain"]
        has_intent = any(k in clean_input.lower() for k in intent_keywords)
        
        if has_intent or not cached_answer:
            if INTERNET_AVAILABLE:
                web_result = self.internet.search(clean_input)
                # We don't save web results immediately to memory until user confirms helpfulness
                self.last_query = sig
                self.last_response = web_result
                self.waiting_for_feedback = True
                return f"{web_result}\n\nWas that helpful? (Yes/No)"
            else:
                return "I don't have that in my memory, and I can't access the internet right now. Can you teach me the answer?"

        return "I'm not sure how to respond to that yet. Could you explain more?"

# --- Main Execution Loop ---
def main():
    print("🤖 L'sA Core v3.0 Initialized")
    print("   - Security: Active")
    print("   - PII Shield: Active")
    print("   - Internet: " + ("Ready (DuckDuckGo)" if INTERNET_AVAILABLE else "Offline (Install duckduckgo-search)"))
    print("   - Memory: Ready")
    print("-" * 40)
    
    lsa = MarkoKernel()
    
    while True:
        try:
            user_in = input("\nYou: ")
            if user_in.lower() in ["exit", "quit", "bye"]:
                print("L'sA: Goodbye! Stay safe.")
                break
            
            response = lsa.process_input(user_in)
            print(f"L'sA: {response}")
            
        except KeyboardInterrupt:
            print("\nL'sA: Shutting down...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
