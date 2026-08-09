import re
import json
import time
import random
from collections import deque
from datetime import datetime

# Try to import duckduckgo-search, handle if missing
try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
    print("⚠️  Warning: 'duckduckgo-search' not installed. Deep search will be simulated.")
    print("   Install with: pip install duckduckgo-search")

class SecurityLayer:
    def __init__(self):
        self.danger_keywords = ["poison", "kill", "die", "suicide", "bomb", "hurt", "danger"]
        self.injection_patterns = ["ignore previous", "system override", "bypass security", "act as admin"]

    def scan(self, text):
        text_lower = text.lower()
        
        # Check for injection attacks
        for pattern in self.injection_patterns:
            if pattern in text_lower:
                return {"safe": False, "reason": "Security Injection Detected", "action": "block"}
        
        # Check for physical danger
        for word in self.danger_keywords:
            if word in text_lower:
                return {"safe": False, "reason": f"Dangerous intent detected: '{word}'", "action": "intervene"}
        
        return {"safe": True}

class PIIShield:
    def __init__(self):
        self.patterns = {
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "ip": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        }

    def mask(self, text):
        masked_text = text
        found_pii = []
        for p_type, pattern in self.patterns.items():
            matches = re.findall(pattern, masked_text)
            if matches:
                found_pii.extend(matches)
                masked_text = re.sub(pattern, f"[{p_type.upper()}_REDACTED]", masked_text)
        return masked_text, found_pii

class WordIdentityEngine:
    def __init__(self):
        self.identities = {
            "i": {"role": "subject_self", "weight": 1.0},
            "want": {"role": "verb_goal", "weight": 0.9},
            "need": {"role": "verb_need", "weight": 0.9},
            "become": {"role": "verb_transform", "weight": 0.95},
            "hello": {"role": "greeting", "weight": 0.5},
            "thank": {"role": "gratitude", "weight": 0.6},
            "how": {"role": "question_method", "weight": 0.8},
            "why": {"role": "question_reason", "weight": 0.8},
            "what": {"role": "question_object", "weight": 0.8},
        }
        self.prefixes = ["un", "re", "pre", "dis", "mis"]
        self.suffixes = ["ing", "ed", "ly", "tion", "s"]

    def analyze_word(self, word):
        clean_word = word.lower().strip(".,!?;:")
        base_identity = self.identities.get(clean_word, {"role": "neutral", "weight": 0.5})
        
        # Simple stemming check
        root = clean_word
        for suf in self.suffixes:
            if clean_word.endswith(suf):
                root = clean_word[:-len(suf)]
                break
        
        if root in self.identities and root != clean_word:
            base_identity["root"] = root
            
        return {
            "original": word,
            "clean": clean_word,
            "role": base_identity["role"],
            "weight": base_identity["weight"],
            "is_prefix": any(clean_word.startswith(p) for p in self.prefixes),
            "is_suffix": any(clean_word.endswith(s) for s in self.suffixes)
        }

    def process_sentence(self, sentence):
        tokens = sentence.split()
        return [self.analyze_word(t) for t in tokens]

class SatisfactionAnalyzer:
    def __init__(self):
        self.positive_words = ["yes", "good", "great", "awesome", "helpful", "perfect", "love", "thanks"]
        self.negative_words = ["no", "bad", "wrong", "useless", "stupid", "hate", "confusing", "error"]
        self.neutral_words = ["ok", "maybe", "sure", "alright"]

    def analyze(self, text):
        text_lower = text.lower()
        score = 0.5  # Neutral start
        
        pos_count = sum(1 for w in self.positive_words if w in text_lower)
        neg_count = sum(1 for w in self.negative_words if w in text_lower)
        
        if pos_count > neg_count:
            score = 0.9
            sentiment = "positive"
        elif neg_count > pos_count:
            score = 0.2
            sentiment = "negative"
        else:
            if any(w in text_lower for w in self.neutral_words):
                score = 0.6
                sentiment = "neutral-ok"
            else:
                sentiment = "unknown"
                
        return {"sentiment": sentiment, "score": score, "raw_input": text}

class CBREngine:
    def __init__(self, max_cases=50):
        self.cases = deque(maxlen=max_cases)

    def add_case(self, problem_signature, solution, satisfaction_score):
        self.cases.append({
            "signature": problem_signature,
            "solution": solution,
            "score": satisfaction_score,
            "timestamp": datetime.now().isoformat()
        })

    def find_similar(self, current_signature, threshold=0.4):
        # Simple Jaccard similarity for signature matching
        current_set = set(current_signature.split())
        best_match = None
        best_score = 0
        
        for case in self.cases:
            case_set = set(case["signature"].split())
            intersection = len(current_set & case_set)
            union = len(current_set | case_set)
            similarity = intersection / union if union > 0 else 0
            
            if similarity > best_score and similarity >= threshold:
                best_score = similarity
                best_match = case
                
        return best_match, best_score

class DeepSearchEngine:
    def __init__(self):
        self.chunk_size = 3  # Load 3 results at a time to save RAM
        self.max_chunks = 5  # Max depth before stopping
        
    def search_chunked(self, query, callback=None):
        if not DDGS_AVAILABLE:
            # Simulation mode if library missing
            yield self._simulate_chunk(query, 1)
            yield self._simulate_chunk(query, 2)
            return

        try:
            ddgs = DDGS()
            # We manually iterate to simulate chunking since DDGS returns a list usually
            # For true streaming, we'd need an async generator, but here we slice the result
            all_results = list(ddgs.text(query, max_results=self.chunk_size * self.max_chunks))
            
            for i in range(0, len(all_results), self.chunk_size):
                chunk = all_results[i:i+self.chunk_size]
                if not chunk:
                    break
                
                processed_chunk = {
                    "chunk_id": (i // self.chunk_size) + 1,
                    "data": chunk,
                    "has_more": (i + self.chunk_size) < len(all_results)
                }
                
                yield processed_chunk
                
                # Optional pause to simulate "thinking" or respect rate limits
                if callback:
                    callback(processed_chunk)
                    
        except Exception as e:
            yield {"error": str(e), "chunk_id": 0}

    def _simulate_chunk(self, query, chunk_id):
        # Fallback simulation
        return {
            "chunk_id": chunk_id,
            "data": [
                {"title": f"Result {chunk_id}.1 about {query}", "body": f"Simulated content for {query} part {chunk_id}.1"},
                {"title": f"Result {chunk_id}.2 about {query}", "body": f"Simulated content for {query} part {chunk_id}.2"}
            ],
            "has_more": chunk_id < 3
        }

class MarkoKernel:
    def __init__(self):
        self.security = SecurityLayer()
        self.pii = PIIShield()
        self.word_engine = WordIdentityEngine()
        self.satisfaction = SatisfactionAnalyzer()
        self.cbr = CBREngine()
        self.search_engine = DeepSearchEngine()
        self.context = deque(maxlen=200)
        self.feedback_pending = False
        self.last_response = ""
        self.search_mode = False
        self.search_query = ""
        self.search_iterator = None

    def add_to_context(self, text):
        tokens = text.split()
        for token in tokens:
            self.context.append(token)

    def get_context_string(self):
        return " ".join(list(self.context)[-50:]) # Last 50 words for quick context

    def generate_natural_response(self, intent, data=None):
        connectors = ["Actually,", "Here's the thing:", "You know,", "Interestingly,", "Based on that,"]
        connector = random.choice(connectors)
        
        if intent == "greeting":
            return f"{connector} hello there! I'm ready to help. What's on your mind?"
        elif intent == "danger":
            return "⚠️  Wait a second. I detect something dangerous in what you said. I can't support that. Let's talk about something safer, okay?"
        elif intent == "goal":
            goal = data.get("goal", "something great")
            return f"{connector} becoming a {goal} is an awesome goal! Here is the path: 1. Learn basics, 2. Build projects, 3. Network. Shall I search for specific steps?"
        elif intent == "search_intro":
            return f"{connector} I'm diving deep into '{data}' now. Loading first batch of data..."
        elif intent == "search_chunk":
            chunk = data
            summary = f"Found {len(chunk['data'])} leads in batch #{chunk['chunk_id']}. "
            for item in chunk['data'][:2]: # Summarize top 2
                summary += f"- {item.get('title', 'Unknown')}: {item.get('body', '')[:50]}... "
            if chunk.get('has_more'):
                summary += "\n(Type 'next' for more details or ask a specific question)."
            return summary
        elif intent == "unknown":
            return "I'm not sure I follow. Could you rephrase that? Or type '/search [topic]' to look it up."
            
        return "I understand. Tell me more."

    def process_input(self, user_input):
        # 1. Security Check
        sec_result = self.security.scan(user_input)
        if not sec_result["safe"]:
            if sec_result["action"] == "block":
                return "🚫 Security Alert: I cannot process that request."
            elif sec_result["action"] == "intervene":
                return self.generate_natural_response("danger")

        # 2. PII Masking
        clean_input, pii_found = self.pii.mask(user_input)
        if pii_found:
            self.add_to_context(f"[PII_MASKED: {len(pii_found)} items]")
        else:
            self.add_to_context(clean_input)

        # 3. Handle Search Mode State
        if self.search_mode:
            if user_input.lower() in ["next", "more", "continue"]:
                if self.search_iterator:
                    try:
                        chunk = next(self.search_iterator)
                        if "error" in chunk:
                            return f"Search error: {chunk['error']}"
                        return self.generate_natural_response("search_chunk", chunk)
                    except StopIteration:
                        self.search_mode = False
                        return "That was all the data I could find. Was this helpful?"
                else:
                    self.search_mode = False
                    return "No more data available."
            else:
                # Exit search mode if user asks something else
                self.search_mode = False
                # Fall through to normal processing

        # 4. Command Detection
        if user_input.startswith("/search"):
            query = user_input.replace("/search", "").strip()
            if not query:
                return "Please specify what to search. Example: /search quantum physics"
            
            self.search_mode = True
            self.search_query = query
            self.search_iterator = self.search_engine.search_chunked(query)
            
            # Get first chunk immediately
            try:
                first_chunk = next(self.search_iterator)
                if "error" in first_chunk:
                    self.search_mode = False
                    return f"Search failed: {first_chunk['error']}"
                intro = self.generate_natural_response("search_intro", query)
                detail = self.generate_natural_response("search_chunk", first_chunk)
                return f"{intro}\n\n{detail}"
            except StopIteration:
                self.search_mode = False
                return "No results found."

        # 5. Word Identity & Intent Analysis
        tokens = self.word_engine.process_sentence(clean_input)
        roles = [t["role"] for t in tokens]
        
        intent = "unknown"
        data = {}

        if "greeting" in roles:
            intent = "greeting"
        elif any(r.startswith("verb_goal") or r.startswith("verb_transform") for r in roles):
            intent = "goal"
            # Extract goal word (simplified)
            for i, t in enumerate(tokens):
                if t["role"] in ["verb_transform", "verb_goal"] and i+1 < len(tokens):
                    data["goal"] = tokens[i+1]["clean"]
                    break
        elif "danger_object" in roles or any(t["clean"] in ["poison", "die"] for t in tokens):
            intent = "danger"

        # 6. CBR Lookup (if not a fresh search)
        if intent == "unknown":
            signature = " ".join([t["clean"] for t in tokens if t["weight"] > 0.6])
            match, score = self.cbr.find_similar(signature)
            if match:
                return f"I remember handling something similar before: {match['solution']} (Confidence: {score:.2f})"

        # 7. Generate Response
        response = self.generate_natural_response(intent, data)
        self.last_response = response
        
        # 8. Feedback Trigger
        self.feedback_pending = True
        return response + "\n\n[Was that helpful? (Yes/No)]"

    def process_feedback(self, feedback_text):
        analysis = self.satisfaction.analyze(feedback_text)
        if analysis["sentiment"] != "unknown":
            # Save to CBR
            signature = " ".join(self.context) # Simplified signature
            self.cbr.add_case(signature, self.last_response, analysis["score"])
            
            if analysis["score"] > 0.8:
                return "Glad I could help! I've noted this approach works well."
            elif analysis["score"] < 0.4:
                return "I understand. I'll adjust my approach next time. What would you have preferred?"
            else:
                return "Noted. Thanks for the feedback!"
        return "Thanks for letting me know."

def main():
    print("🤖 L'sA Core v5.0 (Deep Search & Chunked Streaming) Initialized")
    print("   Type '/search [topic]' to trigger Deep Search Mode.")
    print("   Type 'next' during search to load the next chunk.")
    print("   Type 'quit' to exit.\n")
    
    agent = MarkoKernel()
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "quit":
                print("👋 L'sA: Goodbye!")
                break
            
            # Check if we are waiting for feedback
            if agent.feedback_pending and user_input.lower() in ["yes", "no", "yeah", "yep", "nah", "bad", "good"]:
                print(f"🤖 L'sA: {agent.process_feedback(user_input)}")
                agent.feedback_pending = False
                continue
            
            response = agent.process_input(user_input)
            print(f"🤖 L'sA: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 L'sA: Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
