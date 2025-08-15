import toml
import os

from dotenv import load_dotenv

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")

# Load environment variables from .env file
# Use override=True to force override existing environment variables
load_dotenv(env_path, override=True)

try:
    CONFIG = toml.load(os.path.expanduser("config.toml"))
except Exception as e:
    print(f"load config.toml failed: {e}")
