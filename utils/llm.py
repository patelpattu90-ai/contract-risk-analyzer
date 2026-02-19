import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(
    model="google/flan-t5-large",
    token=os.getenv("HF_API_KEY")
)

def summarize_contract(text: str) -> str:
    prompt = f"""
You are a legal assistant.

Summarize the following contract in simple language.
Focus on:
- obligations
- payment terms
- termination clauses
- potential risks

Contract text:
{text[:4000]}
"""
    response = client.text_generation(
        prompt,
        max_new_tokens=300,
        temperature=0.3
    )
    return response

