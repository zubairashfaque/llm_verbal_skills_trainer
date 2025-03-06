import requests
import json
import logging
from config.settings import MODEL_NAME, OLLAMA_SERVER_URL
from functools import lru_cache
from cachetools import LRUCache, cached
import multiprocessing
# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

response_cache = LRUCache(maxsize=128)  # ✅ Increased cache size

@cached(cache=response_cache)  # ✅ First-level caching
@lru_cache(maxsize=128)        # ✅ Second-level caching
def generate_response(prompt: str, max_tokens: int = 512) -> str:
    """
    Calls the local Ollama server to generate text using the LLaMA-13B model.
    """
    url = f"{OLLAMA_SERVER_URL}generate"
    logging.info(f"Sending request to Ollama at {url}")

    optimization = {
        "quantization": "NF4"  # ✅ Uses Normalized Float 4 (4-bit quantization)
    }

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "num_ctx": 2048,
        "num_gpu": 0,
        "temperature": 0.7,
        "max_tokens": max_tokens,
        "options": optimization
    }

    logging.debug(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()

        generated_text = []
        for line in response.iter_lines(decode_unicode=True):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                logging.debug(f"Received line: {data}")

                # ✅ Ensure we capture response properly
                if "response" in data and data["response"]:
                    generated_text.append(data["response"])

            except json.JSONDecodeError as e:
                logging.error(f"JSON decoding error: {e}")
                continue

        # ✅ Fix: Ensure we return a meaningful response
        final_text = "".join(generated_text).strip()
        if not final_text:
            return "Error: No meaningful response received from Ollama."

        logging.info("Response generated successfully.")
        return final_text

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return "Error: Unable to connect to Ollama. Check if the server is running."


# --------------------------
# MULTIPROCESSING WRAPPER
# --------------------------
def generate_response_parallel(prompt: str, max_tokens: int = 512):
    """
    Uses multiprocessing to generate responses in parallel.
    """
    with multiprocessing.Pool(processes=4) as pool:  # ✅ 4 parallel workers
        result = pool.apply_async(generate_response, (prompt, max_tokens))
        return result.get()