from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from config import Config
from utils import setup_logging, log_query
from rag_engine import RAGEngine
import uuid

print("=" * 50)
print("🚀 Starting CKPCET Chatbot...")
print("=" * 50)

# Point Flask to React's build output
app = Flask(
    __name__,
    static_folder="../frontend/dist",  # React build output
    static_url_path=""                 # Serve from root /
)

CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

os.makedirs("logs", exist_ok=True)

print("🔄 Initializing RAG Engine...")
rag_engine = RAGEngine()
print("✅ RAG Engine Ready!")
print("=" * 50)


# ── API Routes (unchanged) ────────────────────────────────────────────────────

@app.route("/api", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    session_id = data.get("session_id", str(uuid.uuid4()))

    if not user_input:
        return jsonify({"response": "Please enter a message.", "session_id": session_id})

    response = rag_engine.generate_response(user_input, session_id)
    return jsonify({"response": response, "session_id": session_id})


@app.route("/clear_history", methods=["POST"])
def clear_history():
    data = request.get_json()
    session_id = data.get("session_id", "default")
    success = rag_engine.clear_history(session_id)
    return jsonify({
        "message": "Conversation history cleared" if success else "No history found",
        "session_id": session_id,
        "success": success,
    })


@app.route("/get_faqs", methods=["GET"])
def get_faqs():
    faqs = [
        {"question": "What are the engineering admission requirements?", "preview": "Pass 12th Science with 45% marks, pass GUJCET exam...", "stream": "Engineering"},
        {"question": "What engineering branches are available?",         "preview": "Computer, IT, Mechanical, Civil, Electrical, Electronics...", "stream": "Engineering"},
        {"question": "What is the engineering tuition fee?",            "preview": "Approximately ₹44,000 per semester...", "stream": "Engineering"},
        {"question": "Does the college have hostel facilities?",        "preview": "Yes, separate hostels for boys and girls with mess...", "stream": "General"},
        {"question": "How do I contact admissions?",                    "preview": "Phone: +91 78628-24298 or +91 63550 55839...", "stream": "General"},
    ]
    return jsonify({"faqs": faqs})


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "model": "Gemini 2.0 Flash Lite",
        "knowledge_base_entries": len(rag_engine.knowledge_base),
        "active_sessions": len(rag_engine.conversation_history),
        "cache_size": len(rag_engine.response_cache),
    })


# ── Serve React Frontend ──────────────────────────────────────────────────────
# This replaces all the old render_template() routes.
# React Router handles /faq, /aboutus, /contactus etc. on the client side.

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    # If requesting a real file that exists in dist/ (JS, CSS, images), serve it
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # Otherwise serve index.html — React Router takes over
    return send_from_directory(app.static_folder, "index.html")


# ── Security Headers ──────────────────────────────────────────────────────────

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "font-src 'self' https://cdn.jsdelivr.net; "
        "connect-src 'self' https://www.google.com https://*.googleapis.com; "
        "img-src 'self' data:; "
        "media-src 'self' blob:; "
    )
    return response


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Starting Flask server on http://localhost:{port}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)