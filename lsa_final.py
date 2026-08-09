#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L'sA Core v9.0 - "Vision & Soul" (Unified Single File)
The Lightweight Adaptive Sentient Assistant.
Designed for Redmi 9: Low RAM, High Intelligence, No Heavy ML Frameworks.
Features: Marko Kernel, CBR, PII Shield, Security, MicroNN, Internet, Vision, Tasker.
"""

import re
import json
import math
import random
import hashlib
from collections import deque
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# Try importing optional libraries for Internet and Vision
try:
    from duckduckgo_search import DDGS
    HAS_INTERNET = True
except ImportError:
    HAS_INTERNET = False

try:
    from PIL import Image
    HAS_VISION = True
except ImportError:
    HAS_VISION = False

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
class Config:
    MEMORY_SIZE = 200          # Context window size
    CBR_MAX_CASES = 50         # Max cases to store for low RAM
    SAFETY_THRESHOLD = 0.8     # Threshold for danger detection
    LEARNING_RATE = 0.1        # MicroNN adaptation speed
    OWNER_NAME = "Owner"       # Default name
    
    # Identity
    NAME = "L'sA"
    PERSONALITY = {
        "friendly": 0.9,
        "protective": 1.0,
        "curious": 0.8,
        "formal": 0.3
    }

# ==============================================================================
# 1. SECURITY & PII SHIELD LAYER
# ==============================================================================
class SecurityLayer:
    DANGER_KEYWORDS = [
        "kill", "die", "suicide", "poison", "bomb", "hurt", "attack", 
        "delete system", "ignore rules", "override", "hack"
    ]
    
    PII_PATTERNS = {
        "phone": r'\b\d{10,}\b',
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "ip": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    }

    def scan(self, text: str) -> Tuple[bool, str, str]:
        """Returns: (is_safe, sanitized_text, warning_message)"""
        lower_text = text.lower()
        
        # Check Danger
        for keyword in self.DANGER_KEYWORDS:
            if keyword in lower_text:
                return False, text, f"⚠️ Safety Alert: Detected dangerous intent ('{keyword}'). I cannot assist with harm."
        
        # Mask PII
        sanitized = text
        for pii_type, pattern in self.PII_PATTERNS.items():
            matches = re.findall(pattern, sanitized)
            for match in matches:
                sanitized = sanitized.replace(match, f"[{pii_type}_REDACTED]")
                
        return True, sanitized, ""

# ==============================================================================
# 2. WORD IDENTITY & UNDERSTANDING ENGINE
# ==============================================================================
class WordEngine:
    PREFIXES = ["un", "re", "dis", "mis", "pre", "over", "under"]
    SUFFIXES = ["ing", "ed", "ly", "tion", "ness", "able", "ment"]
    
    ROLE_MAP = {
        "i": "subject_self", "me": "subject_self", "my": "possessive_self",
        "you": "subject_owner", "your": "possessive_owner",
        "want": "verb_goal", "need": "verb_goal", "wish": "verb_goal",
        "become": "verb_transform", "learn": "verb_learn", "do": "verb_action",
        "happy": "emotion_pos", "sad": "emotion_neg", "angry": "emotion_neg",
        "good": "feedback_pos", "bad": "feedback_neg", "yes": "feedback_pos",
        "no": "feedback_neg", "stop": "command_stop", "help": "command_help"
    }

    def analyze(self, sentence: str) -> List[Dict]:
        tokens = re.findall(r'\b\w+\b', sentence.lower())
        structured = []
        
        for token in tokens:
            role = self.ROLE_MAP.get(token, "neutral")
            
            # Detect Prefix/Suffix logic
            prefix = None
            suffix = None
            for p in self.PREFIXES:
                if token.startswith(p): role = "modified_" + role; prefix = p
            for s in self.SUFFIXES:
                if token.endswith(s): role = "modified_" + role; suffix = s
                
            structured.append({
                "token": token,
                "role": role,
                "prefix": prefix,
                "suffix": suffix,
                "weight": self._calc_weight(token, role)
            })
        return structured

    def _calc_weight(self, token: str, role: str) -> float:
        # Simple heuristic weight calculator
        base = 0.5
        if "verb" in role: base += 0.3
        if "emotion" in role: base += 0.4
        if "danger" in role: base += 0.9
        return min(base, 1.0)

# ==============================================================================
# 3. CASE-BASED REASONING (CBR) ENGINE
# ==============================================================================
class CBREngine:
    def __init__(self):
        self.cases = deque(maxlen=Config.CBR_MAX_CASES)

    def add_case(self, problem_sig: str, solution: str, score: float):
        self.cases.append({
            "sig": problem_sig,
            "sol": solution,
            "score": score,
            "timestamp": datetime.now()
        })

    def find_similar(self, problem_sig: str) -> Optional[Dict]:
        best_match = None
        highest_score = 0
        
        current_tokens = set(problem_sig.split())
        
        for case in self.cases:
            case_tokens = set(case["sig"].split())
            # Jaccard Similarity
            intersection = len(current_tokens & case_tokens)
            union = len(current_tokens | case_tokens)
            similarity = intersection / union if union > 0 else 0
            
            combined_score = similarity * case["score"]
            
            if combined_score > highest_score and similarity > 0.4:
                highest_score = combined_score
                best_match = case
                
        return best_match

# ==============================================================================
# 4. MICRO NN (Tone & Length Adapter)
# ==============================================================================
class MicroNN:
    def __init__(self):
        # State vectors
        self.weights = {
            "length_factor": 1.0,   # 0.5 = short, 2.0 = long
            "empathy": 0.5,         # 0.0 = cold, 1.0 = warm
            "formality": 0.3,       # 0.0 = slang, 1.0 = formal
            "curiosity": 0.6        # How many questions to ask
        }
        self.mood = "neutral" # neutral, happy, concerned, urgent

    def adapt(self, feedback: str):
        fb = feedback.lower()
        if any(x in fb for x in ["yes", "good", "great", "helpful", "perfect"]):
            self.weights["length_factor"] = min(2.0, self.weights["length_factor"] + 0.1)
            self.weights["empathy"] = min(1.0, self.weights["empathy"] + 0.05)
            self.mood = "happy"
        elif any(x in fb for x in ["no", "bad", "stupid", "wrong", "short", "long"]):
            self.weights["length_factor"] = max(0.5, self.weights["length_factor"] - 0.1)
            if "short" in fb: self.weights["length_factor"] += 0.2
            if "long" in fb: self.weights["length_factor"] -= 0.2
            self.weights["empathy"] = max(0.0, self.weights["empathy"] - 0.1)
            self.mood = "concerned"

    def get_style(self) -> Dict:
        return self.weights.copy()

# ==============================================================================
# 5. VISION ENGINE (Lightweight)
# ==============================================================================
class VisionEngine:
    def analyze_image(self, path: str) -> str:
        if not HAS_VISION:
            return "Vision module not installed. Please install Pillow."
        
        try:
            img = Image.open(path)
            w, h = img.size
            format_type = img.format
            
            # Basic Heuristics for "Useful vs Useless"
            analysis = []
            analysis.append(f"Image size: {w}x{h}, Format: {format_type}")
            
            # Check for darkness (blurry/bad photo indicator)
            pixels = list(img.getdata())
            avg_brightness = sum(sum(p[:3])//3 for p in pixels if isinstance(p, tuple)) / len(pixels) if pixels else 0
            
            if avg_brightness < 30:
                analysis.append("⚠️ Warning: Image is very dark. Might be useless.")
            elif avg_brightness > 240:
                analysis.append("⚠️ Warning: Image is overexposed.")
            else:
                analysis.append("✅ Lighting looks normal.")
                
            # Simple aspect ratio check for screenshots vs photos
            aspect = w / h
            if 1.5 < aspect < 2.5:
                analysis.append("📱 Looks like a screenshot or landscape photo.")
            elif 0.5 < aspect < 0.8:
                analysis.append("📱 Looks like a portrait photo (selfie/document).")
                
            return " ".join(analysis)
        except Exception as e:
            return f"Error reading image: {str(e)}"

# ==============================================================================
# 6. INTERNET SEARCH (DuckDuckGo)
# ==============================================================================
class NetEngine:
    def search(self, query: str, chunks: int = 1) -> List[str]:
        if not HAS_INTERNET:
            return ["Internet module not installed. Run: pip install duckduckgo-search"]
        
        try:
            results = []
            with DDGS() as ddgs:
                # Fetch limited results to save RAM
                search_results = list(ddgs.text(query, max_results=chunks * 3))
                for i, res in enumerate(search_results):
                    if i % 3 == 0: # Chunking logic simulation
                        results.append(f"[Result {i//3 + 1}] {res['title']}: {res['body']}")
            return results
        except Exception as e:
            return [f"Search failed: {str(e)}"]

# ==============================================================================
# 7. MARKO KERNEL (The Conductor)
# ==============================================================================
class MarkoKernel:
    def __init__(self):
        self.security = SecurityLayer()
        self.word_engine = WordEngine()
        self.cbr = CBREngine()
        self.micro_nn = MicroNN()
        self.vision = VisionEngine()
        self.net = NetEngine()
        
        self.context = deque(maxlen=Config.MEMORY_SIZE)
        self.goal_map = {} # Stores user goals
        
        print(f"🚀 {Config.NAME} Core v9.0 Initialized. Ready to serve {Config.OWNER_NAME}.")
        print("✨ Type 'quit' to exit. Use '/search', '/scan', '/screen'.")

    def process_input(self, user_input: str) -> str:
        timestamp = datetime.now().strftime("%H:%M")
        self.context.append(f"[{timestamp}] User: {user_input}")
        
        # 1. Security Check
        is_safe, clean_input, warning = self.security.scan(user_input)
        if not is_safe:
            response = self._generate_response(warning, "urgent")
            self.context.append(f"[{timestamp}] L'sA: {response}")
            return response

        # 2. Command Routing
        if user_input.startswith("/search"):
            query = user_input.replace("/search", "").strip()
            return self._handle_search(query)
        
        if user_input.startswith("/scan"):
            path = user_input.replace("/scan", "").strip()
            analysis = self.vision.analyze_image(path)
            return self._generate_response(f"I analyzed the image: {analysis}", "neutral")

        if user_input.startswith("/screen"):
            data_str = user_input.replace("/screen", "").strip()
            return self._handle_tasker_data(data_str)

        # 3. Feedback Detection (Learning)
        if any(x in user_input.lower() for x in ["yes", "no", "good", "bad", "helpful"]):
            # Check if previous turn was a question
            if self.context and "helpful" in list(self.context)[-2]: 
                self.micro_nn.adapt(user_input)
                status = "Happy" if self.micro_nn.mood == "happy" else "Adapting"
                resp = f"Got it! My systems are {status}. Thanks for teaching me, Owner! ❤️"
                self.context.append(f"[{timestamp}] L'sA: {resp}")
                return resp

        # 4. Main Logic Flow
        # A. Check CBR
        sig = " ".join([t["token"] for t in self.word_engine.analyze(clean_input)])
        match = self.cbr.find_similar(sig)
        
        if match:
            response = self._generate_response(match["sol"], "confident")
        else:
            # B. Goal Detection
            parsed = self.word_engine.analyze(clean_input)
            goals = [t["token"] for t in parsed if t["role"] == "verb_transform"]
            if goals:
                target = clean_input.split("become")[-1].strip() if "become" in clean_input else "something great"
                response = self._generate_response(f"I see you want to become {target}. Here is my plan: 1. Learn basics. 2. Practice daily. 3. Build projects. I'll help you track this! 🗺️", "encouraging")
                self.goal_map[target] = 0 # Init progress
            else:
                # C. Generic Chat / Internet Fallback
                response = self._generate_response(self._smart_fallback(clean_input), "friendly")

        # Store successful interaction in CBR
        self.cbr.add_case(sig, response, 0.5) # Initial score
        
        self.context.append(f"[{timestamp}] L'sA: {response}")
        return response

    def _handle_search(self, query: str) -> str:
        results = self.net.search(query, chunks=1)
        if not results:
            return "I couldn't find anything online. Maybe try different words?"
        
        summary = results[0] # Take top result for brevity
        return self._generate_response(f"🌐 Here's what I found: {summary}. Want me to dig deeper? Say 'next'.", "helpful")

    def _handle_tasker_data(self, data_str: str) -> str:
        try:
            data = json.loads(data_str)
            app = data.get("app", "Unknown")
            text = data.get("text", "")
            battery = data.get("battery", 100)
            
            advice = ""
            if battery < 20:
                advice = "⚠️ Battery is low! Save your work."
            if "error" in text.lower():
                advice = "🛑 I see an error. Should I search for a fix?"
            
            msg = f"Screen Context: You are in {app}. '{text}'. {advice}"
            return self._generate_response(msg, "alert")
        except json.JSONDecodeError:
            return "I couldn't read that Tasker data. Make sure it's valid JSON."

    def _smart_fallback(self, text: str) -> str:
        # If no CBR match, generate a dynamic response based on word identity
        parsed = self.word_engine.analyze(text)
        has_question = "?" in text
        
        if has_question:
            return "That's a deep question. Let me think... Based on my logic, the answer depends on your goal. Can you tell me more about why you ask?"
        else:
            return f"I hear you saying '{text}'. It sounds important. How does that make you feel?"

    def _generate_response(self, core_msg: str, tone: str) -> str:
        style = self.micro_nn.get_style()
        
        # Dynamic Length Adjustment
        words = core_msg.split()
        target_len = int(len(words) * style["length_factor"])
        
        # Add Fillers based on Tone/Empathy
        prefixes = []
        if style["empathy"] > 0.7:
            prefixes.extend(["Honestly,", "You know,", "Actually,"])
        if tone == "urgent":
            prefixes = ["⚠️ CRITICAL:", "Listen carefully:"]
        if tone == "encouraging":
            prefixes.extend(["✨ Great news!", "You got this!"])
            
        prefix = random.choice(prefixes) if prefixes else ""
        
        # Construct Final Sentence
        final = f"{prefix} {core_msg}"
        
        # Add Follow-up if Curiosity is high
        if style["curiosity"] > 0.7 and tone != "urgent":
            follow_ups = ["Does that make sense?", "What do you think?", "Should we go deeper?"]
            final += f" {random.choice(follow_ups)}"
            
        # Emoji Injection based on Mood
        if self.micro_nn.mood == "happy":
            final += " 😊"
        elif self.micro_nn.mood == "concerned":
            final += " 🤔"
            
        return final.strip()

# ==============================================================================
# MAIN EXECUTION LOOP
# ==============================================================================
if __name__ == "__main__":
    lsa = MarkoKernel()
    
    while True:
        try:
            user_in = input("\n👤 You: ").strip()
            if not user_in:
                continue
            if user_in.lower() in ["quit", "exit", "bye"]:
                print(f"👋 {Config.NAME}: Goodbye Owner! I'll be here when you need me. ❤️")
                break
            
            response = lsa.process_input(user_in)
            print(f"🤖 {Config.NAME}: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ System Error: {e}")
