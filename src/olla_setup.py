import os
import time
import logging
import torch
import platform
import psutil
import difflib
import ollama
import subprocess
import csv
from concurrent.futures import ThreadPoolExecutor

# --------------------------
# CONFIGURATION
# --------------------------
MODELS = [
    "llama2:7b",
    "mistral:7b",
    "deepseek-r1:14b",
    "deepseek-r1:7b",
    "deepseek-r1:1.5b",
    "llama3.2",
]

QUANTIZATION_TYPES = ["F16", "Q8_0", "Q4_K_M", "Q4_K_S", "Q6_K", "NF4", "INT8", "BF16"]

OPTIMIZATION_SETTINGS = [
    {"num_threads": 4, "num_gqa": 1, "num_kv_heads": 1},
    {"num_threads": 8, "num_gqa": 2, "num_kv_heads": 2},
    {"num_threads": 16, "num_gqa": 4, "num_kv_heads": 4},
]

PERFORMANCE_METRICS = ["Inference Time", "Memory Usage", "Token Throughput", "Latency"]

BENCHMARK_PROMPT = "Explain quantum computing in simple terms."
USE_GPU = torch.cuda.is_available()

# --------------------------
# SET UP LOGGING
# --------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# --------------------------
# CHECK IF OLLAMA IS INSTALLED
# --------------------------
def is_ollama_installed():
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"Ollama is already installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    logger.warning("Ollama is not installed.")
    return False

# --------------------------
# INSTALL OLLAMA ON UBUNTU
# --------------------------
def install_ollama():
    if not is_ollama_installed():
        logger.info("Installing Ollama on Ubuntu...")
        os.system("curl -fsSL https://ollama.com/install.sh | sh")
        os.system("pip install --upgrade pip")
        os.system("pip install torch psutil ollama")
        logger.info("Ollama installation complete.")

# --------------------------
# GET SYSTEM INFO
# --------------------------
def get_system_info():
    logger.info("\n--- SYSTEM INFORMATION ---")
    logger.info(f"OS: {platform.system()} {platform.release()}")
    logger.info(f"CPU: {platform.processor()}")
    logger.info(f"Total RAM: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB")

    if USE_GPU:
        logger.info(f"CUDA Available: {torch.cuda.is_available()}")
        logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
    else:
        logger.warning("Running on CPU! Expect slower performance.")

# --------------------------
# CHECK IF MODEL IS ALREADY DOWNLOADED
# --------------------------
def is_model_downloaded(model_name):
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if model_name in result.stdout:
            logger.info(f"Model {model_name} is already downloaded.")
            return True
    except Exception as e:
        logger.error(f"Error checking model list: {str(e)}")
    return False

# --------------------------
# DOWNLOAD MODEL IF NOT ALREADY AVAILABLE
# --------------------------
def download_model(model_name):
    if not is_model_downloaded(model_name):
        logger.info(f"\nDownloading model: {model_name}")
        os.system(f"ollama pull {model_name}")
        logger.info("Model downloaded.")

# --------------------------
# RUN INFERENCE TEST WITH QUANTIZATION AND OPTIMIZATION
# --------------------------
def run_inference(model_name, quant_type, optimization, prompt):
    logger.info(
        f"Running inference with model: {model_name} | Quantization: {quant_type} | Optimization: {optimization}")
    start_time = time.time()

    response = ollama.chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        options={"num_ctx": 2048, "num_predict": 100, "temperature": 0.7, **optimization, "quantization": quant_type}
    )

    end_time = time.time()
    inference_time = end_time - start_time
    memory_usage = psutil.virtual_memory().used / (1024 ** 3)  # GB

    logger.info(f"Inference Time: {inference_time:.2f} seconds")
    logger.info(f"Memory Usage: {memory_usage:.2f} GB")
    logger.info(f"Generated Response:\n{response['message']['content']}")

    return response['message']['content'], inference_time, memory_usage

# --------------------------
# BENCHMARK ALL MODELS & QUANTIZATION METHODS
# --------------------------
def benchmark_all():
    install_ollama()
    get_system_info()

    ground_truth = "Quantum computing uses qubits instead of classical bits, allowing for complex calculations through superposition and entanglement."
    results = []

    with ThreadPoolExecutor() as executor:
        executor.map(download_model, MODELS)

    for model in MODELS:
        for quant_type in QUANTIZATION_TYPES:
            for optimization in OPTIMIZATION_SETTINGS:
                logger.info(f"\nTesting Model: {model} | Quantization: {quant_type} | Optimization: {optimization}")
                try:
                    response, inference_time, memory_usage = run_inference(model, quant_type, optimization,
                                                                           BENCHMARK_PROMPT)
                    accuracy = difflib.SequenceMatcher(None, ground_truth, response).ratio() * 100
                    logger.info(f"Accuracy Score: {accuracy:.2f}%")
                    results.append((model, quant_type, optimization, inference_time, memory_usage, accuracy))
                except Exception as e:
                    logger.error(f"Error running model {model} with {quant_type} and {optimization}: {str(e)}")
    save_results_to_csv(results)

# --------------------------
# SAVE RESULTS TO CSV FILE
# --------------------------
def save_results_to_csv(results, filename="benchmark_results.csv"):
    headers = ["Model", "Quantization", "Optimization", "Time (s)", "Memory Usage (GB)", "Accuracy (%)"]

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(results)

    logger.info(f"Results saved to {filename}")

# --------------------------
# MAIN EXECUTION
# --------------------------
if __name__ == "__main__":
    benchmark_all()
