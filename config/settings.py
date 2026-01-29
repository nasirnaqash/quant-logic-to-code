from dotenv import dotenv_values

# Load .env file
config = dotenv_values(".env")

# API Key
ANTHROPIC_API_KEY = config.get("ANTHROPIC_API_KEY")
GEMINI_API_KEY = config.get("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in .env file")

# Model Settings
MODEL_NAME = "gemini-2.5-flash-lite"
TEMPERATURE = 0
MAX_TOKENS = 4000

# Cache Settings
REDIS_HOST = config.get("REDIS_HOST")
REDIS_PORT = int(config.get("REDIS_PORT"))

# Prompt Version
PROMPT_VERSION = "v1.0"

# Paths
PROMPTS_DIR = "prompts"
GENERATED_DIR = "generated"
