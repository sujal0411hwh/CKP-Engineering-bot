import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Configuration - Gemini Only
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Validate API key
    if not GEMINI_API_KEY:
        raise ValueError(
            "❌ GEMINI_API_KEY not found in .env file!\n"
            "Please create a .env file with: GEMINI_API_KEY=your_key_here\n"
            "Get your free API key from: https://aistudio.google.com/app/apikey"
        )

    # Model Configuration
    GEMINI_MODEL = "gemini-2.5-flash"
    MAX_TOKENS = 2048
    TEMPERATURE = 0.2

    # Rate Limiting
    REQUEST_DELAY = 2
    MAX_REQUESTS_PER_MINUTE = 15
    MAX_REQUESTS_PER_DAY = 1500

    # RAG Configuration
    EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
    TOP_K_RETRIEVAL = 5
    SIMILARITY_THRESHOLD = 0.3
    MAX_HISTORY_LENGTH = 5
    SESSION_TIMEOUT = 3600

    # Dataset Configuration
    DATASET_PATH = 'dataset.json'

    # Logging
    LOG_FILE = 'logs/queries.log'
    ENABLE_LOGGING = True

    # Cache Configuration
    ENABLE_CACHE = True
    CACHE_TTL = 300

    @staticmethod
    def apply_rate_limit():
        """Add delay between API requests"""
        time.sleep(Config.REQUEST_DELAY)