import subprocess
import time
from langchain_ollama import OllamaLLM
def start_ollama():
    try:
        # Start Ollama service using subprocess
        subprocess.Popen(["ollama", "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        print("Ollama service started successfully.")
    except Exception as e:
        print(f"Failed to start Ollama service: {e}")

# Wait for Ollama service to start (you can adjust the sleep time)
def wait_for_ollama():
    time.sleep(1)

def get_ollama_response(user_input, reply_type="long"):
    try:
        model = OllamaLLM(model="llama3.2")

        if reply_type == "long":
            result = model.invoke(input=f"{user_input} Please provide a detailed response.")
        else:
            result = model.invoke(input=f"{user_input} Please provide a very brief answer.")

        return result
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't get a response from Ollama."

