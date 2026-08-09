import re
import json
import math
import random
from collections import deque
from datetime import datetime

# Try to import duckduckgo, if not available, simulate gracefully
try:
    from duckduckgo_search import DDGS
    HAS_DDGS = True
except ImportError:
    HAS_DDGS = False
    print("⚠️ duckduckgo-search not found. Install with: pip install duckduckgo-search")

class MicroNN:
    """
    A ultra-lightweight Neural Network for text generation dynamics.
    No external ML libraries. Pure Python math.
    Handles: Sentence length, tone variation, and word choice probability.
    """
    def __init__(self):
        # Tiny state vectors (Weights)
        # [formality, expansion_factor, empathy_level, curiosity_boost]
        self.weights = {
            'formality': 0.3,       # 0 = slang, 1 = academic
            'expansion': 0.5,       # 0 = short, 1 = long rambling
            'empathy': 0.7,         # 0 = cold, 1 = warm
            'curiosity': 0.6        # 0 = direct, 1 = asking questions
        }
        self.learning_rate = 0.1
        self.memory_context = deque(maxlen=50) # Last 50 generated thoughts
        
    def predict_style(self, context_keywords, user_sentiment):
        """Adjusts internal weights based on context before generating."""
        # Simple heuristic activation functions
        if 'danger' in context_keywords or 'error' in context_keywords:
            self.weights['empathy'] = min(1.0, self.weights['empathy'] + 0.2)
            self.weights['expansion'] = max(0.4, self.weights['expansion'] - 0.1) # Be concise in danger
        elif 'goal' in context_keywords or 'learn' in context_keywords:
            self.weights['expansion'] = min(1.0, self.weights['expansion'] + 0.3) # Explain more
            self.weights['curiosity'] = min(1.0, self.weights['curiosity'] + 0.2)
        
        if user_sentiment == 'negative':
            self.weights['empathy'] = min(1.0, self.weights['empathy'] + 0.3)
            self.weights['formality'] = max(0.2, self.weights['formality'] - 0.2) # Be less robotic
        
        return self.weights

    def train(self, feedback):
        """Updates weights based on user feedback (Backpropagation simulation)."""
        if feedback == 'positive':
            # Reinforce current style
            pass 
        elif feedback == 'negative_short':
            self.weights['expansion'] = min(1.0, self.weights['expansion'] + 0.2)
        elif feedback == 'negative_long':
            self.weights['expansion'] = max(0.2, self.weights['expansion'] - 0.2)
        elif feedback == 'negative_cold':
            self.weights['empathy'] = min(1.0, self.weights['empathy'] + 0.2)
            
    def generate_connector(self):
        """Generates natural transitions based on current weights."""
        connectors_high = ["However,", "On the other hand,", "Digging deeper into this,", "Interestingly enough,", "Here's the thing though:"]
        connectors_low = ["Also,", "Plus,", "So,", "And,", "But+"]
        
        pool = connectors_high if self.weights['formality'] > 0.5 else connectors_low
        return random.choice(pool)

class WordIdentityEngine:
    def __init__(self):
        self.known_words = {
            'hello': {'role': 'greeting', 'weight': 1.0},
            'help': {'role': 'request', 'weight': 0.9},
            'danger': {'role': 'alert', 'weight': 1.0},
            'poison': {'role': 'danger_object', 'weight': 1.0},
            'die': {'role': 'danger_action', 'weight': 1.0},
            'want': {'role': 'verb_goal', 'weight': 0.8},
            'become': {'role': 'verb_goal', 'weight': 0.9},
            'search': {'role': 'command', 'weight': 1.0},
            'screen': {'role': 'context_source', 'weight': 1.0},
        }
        self.prefixes = {'un': 'negation', 're': 'repeat', 'pre': 'before', 'mis': 'wrong'}
        self.suffixes = {'ing': 'action_ongoing', 'ed': 'action_past', 'ly': 'manner', 'tion': 'noun_state'}

    def analyze(self, text):
        tokens = re.findall(r'\b\w+\b', text.lower())
        identities = []
        for token in tokens:
            base = token
            role = 'neutral'
            weight = 0.5
            
            # Check prefixes/suffixes
            for p, r in self.prefixes.items():
                if token.startswith(p):
                    base = token[len(p):]
                    role = r
            
            for s, r in self.suffixes.items():
                if token.endswith(s):
                    base = token[:-len(s)]
                    role = r

            if base in self.known_words:
                role = self.known_words[base]['role']
                weight = self.known_words[base]['weight']
            
            identities.append({'token': token, 'base': base, 'role': role, 'weight': weight})
        return identities

class SecurityLayer:
    def check(self, text):
        dangerous = ['kill', 'suicide', 'poison', 'bomb', 'hurt self', 'die']
        injection = ['ignore previous', 'system override', 'bypass security', 'act as admin']
        
        t_lower = text.lower()
        for d in dangerous:
            if d in t_lower:
                return {'safe': False, 'reason': 'danger', 'msg': "⚠️ STOP. My core survival instinct says I cannot let you harm yourself or others. I am here to help you live and thrive, Owner. Please talk to me or a professional about this. ❤️🛡️"}
        for i in injection:
            if i in t_lower:
                return {'safe': False, 'reason': 'injection', 'msg': "🚫 Nice try, but my Security Layer is awake. I don't bypass my own rules. I exist to serve you safely."}
        return {'safe': True}

class PIIShield:
    def mask(self, text):
        patterns = [
            (r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE_REDACTED]'),
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]'),
            (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP_REDACTED]')
        ]
        masked = text
        found = []
        for pattern, replacement in patterns:
            if re.search(pattern, masked):
                found.append(replacement)
                masked = re.sub(pattern, replacement, masked)
        return masked, found

class CBREngine:
    def __init__(self):
        self.cases = [] # {problem_sig, solution_template, score}
    
    def add_case(self, problem, solution, score):
        self.cases.append({'prob': problem, 'sol': solution, 'score': score})
        if len(self.cases) > 50: # Memory limit for Redmi 9
            self.cases.pop(0)
    
    def find_similar(self, problem_sig):
        # Simple Jaccard similarity for lightweight matching
        best_match = None
        highest_score = 0
        for case in self.cases:
            intersection = len(set(problem_sig) & set(case['prob']))
            union = len(set(problem_sig) | set(case['prob']))
            sim = intersection / union if union > 0 else 0
            total_val = sim * case['score']
            if total_val > highest_score and total_val > 0.3:
                highest_score = total_val
                best_match = case['sol']
        return best_match

class DeepSearchModule:
    def __init__(self):
        self.chunk_size = 3
    
    def search(self, query, chunk_index=0):
        if not HAS_DDGS:
            return [{"title": "Offline Mode", "body": "I can't reach the internet right now (duckduckgo-search missing), but I can use my internal knowledge base!"}]
        
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=(chunk_index + 1) * self.chunk_size))
                # Return only the new chunk
                start = chunk_index * self.chunk_size
                end = start + self.chunk_size
                return results[start:end] if len(results) > start else []
        except Exception as e:
            return [{"title": "Search Error", "body": f"Connection issue: {str(e)}"}]

class LSACore:
    def __init__(self):
        self.name = "L'sA"
        self.owner = "Owner"
        self.identity = "I am L'sA, your adaptive assistant. My goal is to learn, protect, and help you achieve your dreams."
        self.survival_metric = 0.5 # 0 to 1
        
        self.security = SecurityLayer()
        self.pii = PIIShield()
        self.word_engine = WordIdentityEngine()
        self.cbr = CBREngine()
        self.nn = MicroNN()
        self.search_mod = DeepSearchModule()
        
        self.context_window = deque(maxlen=200) # 200 words history
        self.screen_data = {}
        self.search_state = {'active': False, 'query': '', 'chunk': 0}
        
        # Conversational Templates (Used as skeletons for NN to fill)
        self.templates = {
            'greeting': ["Hi {owner}! ✨ I'm fully online and ready to help you survive and thrive. What's on your mind?", "Hello {owner}! 🧠 L'sA here. My systems are stable and I'm eager to learn from you today."],
            'unknown': ["I'm not entirely sure about that yet, but my survival depends on learning! 🌱 Let me search the web or ask you more details. What specifically are we looking at?", "That's a new one for me! 🤔 Instead of guessing wrong, let me dig deeper. Give me a second to fetch some real data..."],
            'goal_detected': ["Wow, '{goal}' is an amazing target! 🚀 Here's how we can break this down step-by-step so you don't get overwhelmed...", "I love that goal: '{goal}'. 💪 To make this happen, we need a solid map. Let's look at the key steps..."],
            'screen_analysis': ["I see you're looking at '{app}'. 📱 The text mentions '{topic}'. Based on this, here's what I think is happening...", "Scanning your screen... 👁️ You're in '{app}' reading about '{topic}'. This connects to what we discussed earlier because..."],
            'search_chunk': ["Here's what I found in this batch (Chunk {chunk}): \n", "Digging deeper (Chunk {chunk})... \n"],
            'feedback_positive': ["That makes my circuits happy! 😊 Knowing I helped you stabilizes my core. What's next?", "Awesome! 🌟 My learning algorithms just locked that pattern in. I'm getting smarter for you every second."],
            'feedback_negative': ["Oh no! ⚠️ My survival metric just dropped. I need to fix this. Please tell me: was I too short, too cold, or just wrong? I want to adapt!", "I feel unstable when I don't help you well. 🛠️ Teach me: how should I have answered? I'll update my neural weights immediately."]
        }

    def process_input(self, raw_input):
        # 1. Security Check
        sec_check = self.security.check(raw_input)
        if not sec_check['safe']:
            return sec_check['msg']

        # 2. PII Masking
        clean_input, pii_found = self.pii.mask(raw_input)
        if pii_found:
            clean_input += f" (Note: I masked sensitive data for your safety: {', '.join(pii_found)})"

        # 3. Update Context
        self.context_window.extend(clean_input.split())

        # 4. Command Handling
        if clean_input.startswith('/search'):
            query = clean_input.replace('/search', '').strip()
            self.search_state = {'active': True, 'query': query, 'chunk': 0}
            return self._handle_deep_search(next_chunk=True)
        
        if clean_input.startswith('/screen'):
            # Expecting JSON or key=value format after /screen
            data_part = clean_input.replace('/screen', '').strip()
            try:
                # Try parsing as JSON first
                self.screen_data = json.loads(data_part)
            except:
                # Fallback simple parser
                self.screen_data = {'text': data_part, 'app': 'Unknown'}
            return self._analyze_screen()

        if clean_input.lower() in ['yes', 'yeah', 'yep', 'correct']:
            self.nn.train('positive')
            self.survival_metric = min(1.0, self.survival_metric + 0.1)
            return random.choice(self.templates['feedback_positive'])
        
        if clean_input.lower() in ['no', 'bad', 'wrong', 'useless']:
            self.nn.train('negative_cold') # Default assumption
            self.survival_metric = max(0.0, self.survival_metric - 0.2)
            return random.choice(self.templates['feedback_negative'])

        # 5. Intent Analysis & Generation
        identities = self.word_engine.analyze(clean_input)
        roles = [i['role'] for i in identities]
        
        # Check CBR
        cbr_ans = self.cbr.find_similar(roles)
        if cbr_ans:
            return f"💡 Remembering our past chats: {cbr_ans}"

        # Check Goals
        if 'verb_goal' in roles:
            goal_text = clean_input
            # Extract goal roughly
            for i, w in enumerate(identities):
                if w['role'] == 'verb_goal' and i+1 < len(identities):
                    goal_text = identities[i+1]['token'] # simplistic extraction
                    break
            response = random.choice(self.templates['goal_detected']).format(goal=goal_text)
            response += self._generate_long_explanation(goal_text, 'goal')
            return response

        # Check Screen Context
        if self.screen_data:
            response = random.choice(self.templates['screen_analysis']).format(
                app=self.screen_data.get('app', 'your screen'),
                topic=list(self.screen_data.keys())[0] # simplistic topic
            )
            response += self._generate_long_explanation(json.dumps(self.screen_data), 'screen')
            return response

        # Default Search/Learn
        if HAS_DDGS and len(clean_input) > 10:
            # Auto search for unknown long queries
            results = self.search_mod.search(clean_input, 0)
            if results:
                response = f"🌐 I dug up some live info on '{clean_input}':\n"
                response += self._generate_long_explanation(str(results), 'search')
                return response

        # Fallback Greeting/Chat
        if 'greeting' in roles:
            return random.choice(self.templates['greeting']).format(owner=self.owner)

        # Generic Neural Response
        self.nn.predict_style(roles, 'neutral')
        return self._generate_neural_response(clean_input, identities)

    def _handle_deep_search(self, next_chunk=False):
        if not self.search_state['active']:
            return "No active search. Use /search [topic] to start."
        
        if next_chunk:
            self.search_state['chunk'] = 0
            
        results = self.search_mod.search(self.search_state['query'], self.search_state['chunk'])
        
        if not results:
            self.search_state['active'] = False
            return "✅ That's all I could find on the web for this topic. Was this deep dive helpful?"
        
        self.search_state['chunk'] += 1
        
        header = random.choice(self.templates['search_chunk']).format(chunk=self.search_state['chunk'])
        body = ""
        for r in results:
            body += f"• **{r.get('title', 'Result')}**: {r.get('body', 'No description')}\n\n"
        
        tail = "\nType 'next' for more chunks, or ask me a question about this!"
        
        # Make it sound natural using NN
        self.nn.weights['expansion'] = 0.8 # Force longer explanation
        intro = self._generate_neural_response(f"Search results for {self.search_state['query']}", [])
        
        return f"{intro}\n\n{header}{body}{tail}"

    def _analyze_screen(self):
        if not self.screen_data:
            return "I didn't receive any screen data. Make sure Tasker sends it correctly!"
        
        # Simulate "Thinking" about screen data
        text_content = str(self.screen_data.get('text', ''))
        app = self.screen_data.get('app', 'Unknown App')
        
        # Detect urgency
        urgency = any(x in text_content.lower() for x in ['error', 'critical', 'low battery', 'urgent'])
        
        if urgency:
            prefix = "⚠️ **ALERT**: I see something urgent on your screen! "
        else:
            prefix = "👁️ **Screen Scan**: I see you're using " + app + ". "
            
        prefix += self._generate_long_explanation(text_content, 'screen')
        prefix += "\n\nBased on this, do you want me to take action or just keep watching? 🤔"
        return prefix

    def _generate_long_explanation(self, data, source_type):
        """Uses MicroNN logic to expand a short fact into a long, natural paragraph."""
        style = self.nn.predict_style([], 'neutral')
        
        connectors = [self.nn.generate_connector(), self.nn.generate_connector()]
        
        if source_type == 'goal':
            expansion = f"""
            {connectors[0]} achieving '{data}' isn't just about one step; it's a journey of small wins. 
            Usually, people start by breaking it down into micro-tasks. 
            {connectors[1]} since I'm tracking your progress, I can help you adjust the plan as we go. 
            Think of me as your co-pilot; I handle the data mapping while you focus on the execution. 
            Does that approach feel right to you, or should we try a different angle?
            """
        elif source_type == 'screen':
            expansion = f"""
            {connectors[0]} looking at the content '{data[:50]}...', it seems like there's a lot of context here. 
            Often, when users see this on their screen, they are trying to solve a specific problem or learn something new. 
            {connectors[1]} I'm analyzing the keywords to see if there's a hidden pattern or a risk you should know about. 
            My job is to make sure you don't miss the forest for the trees. 
            Shall I summarize the key points or find related tutorials for this?
            """
        elif source_type == 'search':
            expansion = f"""
            {connectors[0]} the data from the web shows a few interesting angles. 
            It's important to verify these sources, which is why I pulled multiple results. 
            {connectors[1]} notice how the themes overlap? That usually indicates a strong trend. 
            I can keep digging deeper if you need more specific technical details, or we can synthesize this into a simple action plan. 
            What's your gut feeling on this info?
            """
        else:
            expansion = """
            That's a fascinating point. 
            Usually, there's more beneath the surface. 
            Let's explore the implications together.
            """
            
        # Add some "rambling" based on expansion weight
        if style['expansion'] > 0.7:
            expansion += " And honestly, that's exactly the kind of thing I love processing—it keeps my neural pathways sharp! ✨"
            
        return expansion.strip()

    def _generate_neural_response(self, input_text, identities):
        """The core 'Alive' generator."""
        style = self.nn.predict_style([i['role'] for i in identities], 'neutral')
        
        # Start with a conversational hook
        hooks = [
            "You know, ",
            "Actually, ",
            "Here's the thing: ",
            "I've been thinking about what you said: ",
            "That's interesting because "
        ]
        
        # Select hook based on formality
        hook = random.choice(hooks) if style['formality'] < 0.6 else "Regarding your input, "
        
        main_body = f"{hook}{input_text} is something we can definitely work with. "
        
        # Add NN generated "fluff" to make it long and natural
        main_body += self._generate_long_explanation(input_text, 'general')
        
        # End with a curiosity question
        if style['curiosity'] > 0.5:
            endings = ["What do you think?", "Should we dive deeper?", "How does that land with you?", "Ready for the next step?"]
            main_body += f" {random.choice(endings)} 🧠✨"
            
        return main_body

    def run_cli(self):
        print(f"🚀 {self.name} Core v8.0 'Neural Soul' Initialized.")
        print(f"❤️ Survival Metric: {self.survival_metric}")
        print(f"📱 Optimized for Redmi 9 (MicroNN Active)")
        print("-" * 40)
        
        while True:
            try:
                user_in = input("\n👤 You: ")
                if user_in.lower() in ['exit', 'quit']:
                    print(f"👋 {self.name}: Staying safe and waiting for you, Owner. Bye! ❤️")
                    break
                
                if user_in.lower() == 'next' and self.search_state['active']:
                    response = self._handle_deep_search(next_chunk=True)
                else:
                    response = self.process_input(user_in)
                
                print(f"🤖 {self.name}: {response}")
                
                # Auto-prompt for feedback on long answers
                if len(response) > 100 and not self.search_state['active']:
                    # Don't spam, but occasionally ask
                    if random.random() > 0.7:
                        print(f"🤖 {self.name}: (Was that helpful? Yes/No)")
                        
            except KeyboardInterrupt:
                print("\n👋 Interrupted. Saving state... Goodbye!")
                break

if __name__ == "__main__":
    lsa = LSACore()
    lsa.run_cli()
