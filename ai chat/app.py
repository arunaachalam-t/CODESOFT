"""
Web interface for RuleBot — run this file to chat in your browser.
"""

import uuid
from flask import Flask, jsonify, render_template, request, session

from chatbot import ConversationState, detect_intent, generate_response

app = Flask(__name__)
app.secret_key = "rulebot-dev-key-change-in-production"

# One conversation state per browser session
_states: dict[str, ConversationState] = {}


def get_state() -> ConversationState:
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())
    sid = session["sid"]
    if sid not in _states:
        _states[sid] = ConversationState()
    return _states[sid]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400

    state = get_state()
    response = generate_response(message, state)
    intent, _ = detect_intent(message)

    return jsonify({
        "response": response,
        "turn_count": state.turn_count,
        "ended": intent == "farewell",
    })


@app.route("/api/reset", methods=["POST"])
def reset():
    sid = session.get("sid")
    if sid and sid in _states:
        del _states[sid]
    session.clear()
    return jsonify({"ok": True})


if __name__ == "__main__":
    print("RuleBot web UI starting at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
