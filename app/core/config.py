import os
from redis import Redis
import logging

openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    raise ValueError("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")

# Conectar a Redis
try:
    redis_client = Redis(host='redis', port=6379, db=0)
    redis_client.ping()
    logging.info("Connected to Redis successfully.")
except Exception as e:
    logging.error(f"Could not connect to Redis: {e}")
    raise ConnectionError("Could not connect to Redis. Ensure Redis is running.") from e
