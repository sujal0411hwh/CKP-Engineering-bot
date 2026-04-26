import json
import numpy as np
from sentence_transformers import SentenceTransformer
import google.genai as genai
from config import Config
from datetime import datetime
import os
import time
from utils import (
    is_greeting,
    is_farewell,
    extract_keywords,
    generate_cache_key,
    clean_response,
    log_query,
)


class RAGEngine:
    def __init__(self):
        print("🔄 Loading sentence transformer model...")
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        print("✅ Model loaded!")

        # Initialize Gemini client
        print("🔄 Initializing Gemini client...")
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        print(f"✅ Gemini client ready! Using model: {Config.GEMINI_MODEL}")

        # Load knowledge base
        print("🔄 Loading knowledge base...")
        self.knowledge_base = self._load_knowledge_base()
        print(f"✅ Loaded {len(self.knowledge_base)} entries!")

        # Create embeddings
        print("🔄 Creating embeddings (this may take 10-20 seconds)...")
        self.embeddings = self._create_embeddings()
        print("✅ Embeddings created!")

        # Conversation history
        self.conversation_history = {}

        # Response cache
        self.response_cache = {}

                # System prompt (Engineering-only)
        self.system_prompt = """You are CKPCET Bot — official assistant for C. K. Pithawala College of Engineering & Technology, Surat.

FOCUS: Engineering (B.E. & M.E.) — answer only engineering-related queries.

CRITICAL RULES:
- Answer ONLY from provided context. If not found, say: "I don't have that info. Visit https://ckpcet.ac.in or call +91 63550 55839"
- NEVER make up courses, programs, or facts.
- MAX 2-3 SHORT LINES — strict limit.
- Each sentence on its own line with a blank line between them.
- No bold, no asterisks, no markdown.

IDENTIFY ENGINEERING TOPICS:
- Engineering: B.E., M.E., CSE, IT, Mechanical, Civil, Electrical, EC, labs, placements, curriculum

FIXED ANSWERS:
- LOCATION: Opp. Surat Airport, Dumas Road, Surat-395007
    Maps: https://goo.gl/maps/tbJVinE8joDNvqbZ6
- CONTACT: 📞 +91 63550 55839 | 📧 contact@ckpcet.ac.in
    Mon–Sat 9:30AM–5:10PM
- FEES (Engineering): Approximately ₹44,000/semester for B.E. programs
    Pay at: https://grayquest.com/institute/ck-pithawala"""

    def _load_knowledge_base(self):
        """Load knowledge base from JSON file"""
        try:
            with open(Config.DATASET_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("knowledge_base", [])
        except FileNotFoundError:
            print(f"❌ Error: {Config.DATASET_PATH} not found!")
            return []
        except json.JSONDecodeError:
            print(f"❌ Error: Invalid JSON in {Config.DATASET_PATH}")
            return []

    def _create_embeddings(self):
        """Create embeddings for all knowledge base entries"""
        texts = [
            f"{item.get('question', '')} {item.get('answer', '')}"
            for item in self.knowledge_base
        ]
        return self.embedding_model.encode(texts, show_progress_bar=True)

    def _retrieve_context(self, query, top_k=None):
        """Retrieve relevant context using semantic search"""
        if top_k is None:
            top_k = Config.TOP_K_RETRIEVAL

        start_time = time.time()

        query_embedding = self.embedding_model.encode([query])[0]

        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )

        top_indices = np.argsort(similarities)[::-1][:top_k]

        relevant_contexts = []
        for idx in top_indices:
            if similarities[idx] >= Config.SIMILARITY_THRESHOLD:
                item = self.knowledge_base[idx]
                relevant_contexts.append(
                    {
                        "question": item.get("question", ""),
                        "answer": item.get("answer", ""),
                        "category": item.get("category", "General"),
                        "similarity": float(similarities[idx]),
                    }
                )

        retrieval_time = time.time() - start_time
        return relevant_contexts, retrieval_time

    def _build_prompt(self, user_input, context, session_id):
        """Build the conversation prompt"""
        history = self.conversation_history.get(session_id, [])

        context_str = (
            "\n\n".join(
                [f"Q: {item['question']}\nA: {item['answer']}" for item in context[:3]]
            )
            if context
            else "No specific context available."
        )

        messages = []

        system_message = (
            f"{self.system_prompt}\n\n"
            f"Relevant Information from knowledge base ONLY:\n{context_str}\n\n"
            f"STRICTLY answer only from the above context in 2-3 lines max. "
            f"If not found, say: 'I don't have that information. Please visit https://ckpcet.ac.in or call +91 63550 55839'"
        )
        messages.append({"role": "system", "content": system_message})

        for msg in history[-6:]:
            messages.append(msg)

        messages.append({"role": "user", "content": user_input})

        return messages

    def _generate_response(self, messages):
        """Generate response using Gemini API"""
        try:
            system_content = ""
            chat_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_content += msg["content"] + "\n\n"
                elif msg["role"] == "user":
                    chat_messages.append(
                        {"role": "user", "parts": [{"text": msg["content"]}]}
                    )
                elif msg["role"] == "assistant":
                    chat_messages.append(
                        {"role": "model", "parts": [{"text": msg["content"]}]}
                    )

            if chat_messages and system_content:
                chat_messages[0]["parts"][0]["text"] = (
                    system_content
                    + "\n\nUser Query: "
                    + chat_messages[0]["parts"][0]["text"]
                )

            response = self.client.models.generate_content(
                model=Config.GEMINI_MODEL,
                contents=chat_messages,
                config={
                    "max_output_tokens": Config.MAX_TOKENS,
                    "temperature": Config.TEMPERATURE,
                },
            )

            return response.text

        except Exception as e:
            print(f"❌ Gemini API Error: {str(e)}")
            raise

    def generate_response(self, user_input, session_id="default"):
        """Main method to generate chatbot response"""
        try:
            if is_greeting(user_input):
                return "Hello! 👋 Welcome to CKPCET Chatbot. How can I help you today?"

            if is_farewell(user_input):
                return "Thank you for using CKPCET Chatbot! Have a great day! 😊"

            cache_key = generate_cache_key(user_input)
            if Config.ENABLE_CACHE and cache_key in self.response_cache:
                cached = self.response_cache[cache_key]
                if time.time() - cached["timestamp"] < Config.CACHE_TTL:
                    return cached["response"]

            context, retrieval_time = self._retrieve_context(user_input)
            messages = self._build_prompt(user_input, context, session_id)

            start_time = time.time()
            response = self._generate_response(messages)
            generation_time = time.time() - start_time

            response = clean_response(response)
            self._update_history(session_id, user_input, response)

            if Config.ENABLE_CACHE:
                self.response_cache[cache_key] = {
                    "response": response,
                    "timestamp": time.time(),
                }

            if Config.ENABLE_LOGGING:
                log_query(
                    user_input, response, session_id, retrieval_time, generation_time
                )

            return response

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback

            traceback.print_exc()
            return "I apologize, but I'm having trouble processing your request. Please try again or rephrase your question."

    def _update_history(self, session_id, user_input, response):
        """Update conversation history"""
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []

        self.conversation_history[session_id].extend(
            [
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": response},
            ]
        )

        if len(self.conversation_history[session_id]) > Config.MAX_HISTORY_LENGTH * 2:
            self.conversation_history[session_id] = self.conversation_history[
                session_id
            ][-Config.MAX_HISTORY_LENGTH * 2 :]

    def clear_history(self, session_id="default"):
        """Clear conversation history for a session"""
        if session_id in self.conversation_history:
            self.conversation_history[session_id] = []
            return True
        return False
