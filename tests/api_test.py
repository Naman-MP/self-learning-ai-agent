
from llm import llm
import time

start = time.monotonic()

try:
    print("Connecting to Gemini...", flush=True)
    response = llm.invoke("Say hello")
    print("Response:", response.content)
except Exception as e:
    print("Error:", type(e).__name__, str(e))
finally:
    print("Elapsed:", round(time.monotonic() - start, 2), "seconds")
