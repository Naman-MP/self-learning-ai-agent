from dotenv import load_dotenv
from langchain_ollama import ChatOllama
load_dotenv()

llm = ChatOllama(
    model="qwen2.5-coder-14b:latest",
    base_url="http://localhost:11434",
    temperature=0,
    num_ctx=4096,
    validate_model_on_init=True
)