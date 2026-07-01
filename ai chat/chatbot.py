"""
Simple rule-based chatbot using if-else logic and pattern matching.

Demonstrates basic NLP concepts: intent detection, entity extraction,
and conversation flow without machine learning.
"""

import re
import random
from datetime import datetime


# ---------------------------------------------------------------------------
# Response templates grouped by intent
# ---------------------------------------------------------------------------

RESPONSES = {
    "greeting": [
        "Hello! How can I help you today?",
        "Hi there! What would you like to know?",
        "Hey! I'm here to chat. What's on your mind?",
    ],
    "farewell": [
        "Goodbye! Have a great day!",
        "See you later! Take care.",
        "Bye! Feel free to come back anytime.",
    ],
    "thanks": [
        "You're welcome!",
        "Happy to help!",
        "Anytime! Let me know if you need anything else.",
    ],
    "help": [
        "I can answer questions about:\n"
        "  • Greetings and farewells\n"
        "  • The current time and date\n"
        "  • Simple math calculations\n"
        "  • Weather (demo responses)\n"
        "  • Jokes and fun facts\n"
        "Just type your question and I'll do my best!",
    ],
    "unknown": [
        "I'm not sure I understand. Try asking for 'help' to see what I can do.",
        "Hmm, I didn't catch that. Type 'help' to see my capabilities.",
        "I don't have a response for that yet. Ask me for 'help'!",
    ],
}

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the developer go broke? Because he used up all his cache.",
    "How many programmers does it take to change a light bulb? None — it's a hardware problem.",
]

FUN_FACTS = [
    "Honey never spoils. Archaeologists have found 3,000-year-old honey still edible.",
    "Octopuses have three hearts and blue blood.",
    "A day on Venus is longer than a year on Venus.",
]


# ---------------------------------------------------------------------------
# Pattern definitions: (compiled regex, intent name)
# Order matters — first match wins.
# ---------------------------------------------------------------------------

PATTERNS = [
    # Greetings
    (re.compile(r"\b(hi|hello|hey|howdy|greetings|good\s+(morning|afternoon|evening))\b", re.I), "greeting"),

    # Farewells
    (re.compile(r"\b(bye|goodbye|see\s+you|farewell|exit|quit|leave)\b", re.I), "farewell"),

    # Thanks
    (re.compile(r"\b(thanks?|thank\s+you|thx|appreciate)\b", re.I), "thanks"),

    # Help
    (re.compile(r"\b(help|what\s+can\s+you\s+do|capabilities|commands)\b", re.I), "help"),

    # Time / date
    (re.compile(r"\b(what\s+time|current\s+time|time\s+is\s+it)\b", re.I), "time"),
    (re.compile(r"\b(what\s+date|today'?s?\s+date|what\s+day)\b", re.I), "date"),

    # Weather (demo — no real API)
    (re.compile(r"\b(weather|temperature|forecast|rain|sunny)\b", re.I), "weather"),

    # Math
    (re.compile(r"\b(calculate|compute|what\s+is)\s+[\d\+\-\*/\(\)\.\s]+", re.I), "math"),
    (re.compile(r"^[\d\+\-\*/\(\)\.\s]+$"), "math"),

    # Jokes & facts
    (re.compile(r"\b(tell\s+me\s+a\s+joke|joke|make\s+me\s+laugh)\b", re.I), "joke"),
    (re.compile(r"\b(fun\s+fact|interesting\s+fact|tell\s+me\s+something)\b", re.I), "fact"),

    # Name / identity
    (re.compile(r"\b(what\s+is\s+your\s+name|who\s+are\s+you|your\s+name)\b", re.I), "identity"),
    (re.compile(r"\b(my\s+name\s+is|i\s+am|i'm)\s+(\w+)", re.I), "user_name"),

    # How are you
    (re.compile(r"\b(how\s+are\s+you|how\s+do\s+you\s+do|how'?s?\s+it\s+going)\b", re.I), "how_are_you"),
]


# ---------------------------------------------------------------------------
# Conversation state (simple memory for multi-turn flow)
# ---------------------------------------------------------------------------

class ConversationState:
    def __init__(self):
        self.user_name: str | None = None
        self.turn_count: int = 0


# ---------------------------------------------------------------------------
# Intent detection via pattern matching
# ---------------------------------------------------------------------------

def detect_intent(user_input: str) -> tuple[str, re.Match | None]:
    """Scan input against patterns and return (intent, match_object)."""
    text = user_input.strip()

    for pattern, intent in PATTERNS:
        match = pattern.search(text)
        if match:
            return intent, match

    return "unknown", None


# ---------------------------------------------------------------------------
# Intent handlers — each returns a response string
# ---------------------------------------------------------------------------

def handle_time() -> str:
    now = datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}."


def handle_date() -> str:
    now = datetime.now()
    return f"Today is {now.strftime('%A, %B %d, %Y')}."


def handle_weather() -> str:
    conditions = ["sunny", "partly cloudy", "overcast", "light rain"]
    temp = random.randint(15, 32)
    condition = random.choice(conditions)
    return (
        f"(Demo response) The weather looks {condition} with a temperature "
        f"around {temp}°C. Connect a weather API for real data!"
    )


def handle_math(user_input: str) -> str:
    """Extract and evaluate a simple arithmetic expression."""
    expression = re.sub(r"(?i)\b(calculate|compute|what\s+is)\s+", "", user_input).strip()

    if not re.fullmatch(r"[\d\+\-\*/\(\)\.\s]+", expression):
        return "I can only evaluate simple math like '2 + 2' or '10 * 5'."

    try:
        # Safe eval: only digits and operators allowed (validated above)
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except (SyntaxError, ZeroDivisionError, TypeError):
        return "Sorry, I couldn't calculate that. Try something like '2 + 2'."


def handle_user_name(match: re.Match, state: ConversationState) -> str:
    name = match.group(2).capitalize()
    state.user_name = name
    return f"Nice to meet you, {name}! How can I help you?"


def handle_how_are_you(state: ConversationState) -> str:
    if state.user_name:
        return f"I'm doing great, {state.user_name}! Thanks for asking. How are you?"
    return "I'm doing great, thanks for asking! How are you?"


# ---------------------------------------------------------------------------
# Main response generator — if-else dispatch on detected intent
# ---------------------------------------------------------------------------

def generate_response(user_input: str, state: ConversationState) -> str:
    """Route user input to the correct handler based on detected intent."""
    intent, match = detect_intent(user_input)
    state.turn_count += 1

    # --- if-else intent dispatch ---
    if intent == "greeting":
        reply = random.choice(RESPONSES["greeting"])
        if state.user_name:
            reply = reply.replace("!", f", {state.user_name}!")
        return reply

    elif intent == "farewell":
        return random.choice(RESPONSES["farewell"])

    elif intent == "thanks":
        return random.choice(RESPONSES["thanks"])

    elif intent == "help":
        return RESPONSES["help"][0]

    elif intent == "time":
        return handle_time()

    elif intent == "date":
        return handle_date()

    elif intent == "weather":
        return handle_weather()

    elif intent == "math":
        return handle_math(user_input)

    elif intent == "joke":
        return random.choice(JOKES)

    elif intent == "fact":
        return f"Here's a fun fact: {random.choice(FUN_FACTS)}"

    elif intent == "identity":
        return "I'm RuleBot, a simple rule-based chatbot built with pattern matching!"

    elif intent == "user_name" and match:
        return handle_user_name(match, state)

    elif intent == "how_are_you":
        return handle_how_are_you(state)

    else:
        return random.choice(RESPONSES["unknown"])


# ---------------------------------------------------------------------------
# Conversation loop
# ---------------------------------------------------------------------------

def run_chatbot():
    state = ConversationState()

    print("=" * 50)
    print("  RuleBot — A Simple Rule-Based Chatbot")
    print("=" * 50)
    print("Type your message below. Enter 'quit' or 'bye' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break

        if not user_input:
            continue

        response = generate_response(user_input, state)
        print(f"Bot: {response}")

        # Exit after farewell intent is handled
        intent, _ = detect_intent(user_input)
        if intent == "farewell":
            break

    print(f"\n(Session ended after {state.turn_count} turns.)")


if __name__ == "__main__":
    run_chatbot()
