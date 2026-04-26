import re
import logging
from datetime import datetime
import hashlib

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/queries.log"), logging.StreamHandler()],
)


def setup_logging(log_file):
    """Setup logging configuration"""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def is_greeting(text):
    """Check if message is a greeting"""
    greetings = [
        r"\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b",
        r"^(hi|hello|hey)$",
        r"\b(namaste|namaskar)\b",
    ]
    text_lower = text.lower().strip()
    return any(re.search(pattern, text_lower) for pattern in greetings)


def is_farewell(text):
    """Check if message is a farewell"""
    farewells = [
        r"\b(bye|goodbye|see you|take care|thanks|thank you)\b",
        r"^(bye|thanks)$",
    ]
    text_lower = text.lower().strip()
    return any(re.search(pattern, text_lower) for pattern in farewells)


def extract_keywords(text):
    """Extract important keywords from query"""
    stop_words = {
        "the",
        "is",
        "at",
        "which",
        "on",
        "a",
        "an",
        "as",
        "are",
        "was",
        "were",
        "been",
        "be",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
    }
    words = re.findall(r"\b\w+\b", text.lower())
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    return keywords


def generate_cache_key(text):
    """Generate cache key for a query"""
    return hashlib.md5(text.lower().strip().encode()).hexdigest()


def clean_response(response):
    """Clean up response formatting"""
    response = re.sub(r"\n{3,}", "\n\n", response)
    response = response.strip()
    return response


def log_query(user_query, response, session_id, retrieval_time, generation_time):
    """Log user queries for analytics"""
    logging.info(
        f"Session: {session_id} | "
        f"Query: {user_query[:100]} | "
        f"Retrieval: {retrieval_time:.2f}s | "
        f"Generation: {generation_time:.2f}s"
    )


def detect_stream(user_input):
    """Detect whether the user query is about Engineering.

    Returns: 'Engineering' or None
    """
    query = user_input.lower()

    engineering_keywords = [
        "engineering",
        "btech",
        "mtech",
        "cse",
        "it",
        "mechanical",
        "civil",
        "electrical",
        "ec",
        "branch",
        "specialization",
        "b.e.",
        "m.e.",
        "computer",
        "ece",
        "automobile",
    ]

    if any(keyword in query for keyword in engineering_keywords):
        return "Engineering"

    return None
