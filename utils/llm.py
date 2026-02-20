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


def summarize_chunks(chunks):
    """
    Summarize each chunk individually, then combine them
    into a final high-level contract summary. 
    """

    chunk_summaries = []

    for idx, chunk in enumerate(chunks):
        prompt = f"""
You are a legal assistant.

Summarize the following part of a contract.
Focus on:
- obligations
- payment terms
- termination
- risks

Contract part:
{chunk}
"""
    
    response = client.text_generation(
        prompt,
        max_new_tokens=200,
        temperature=0.3
    )

    chunk_summaries.append(responses)

    combined_text = "\n".join(chunk_summaries)

    final_prompt = f"""
You are a legal expert.

Given the following summaries of different parts of a contract,
produce a concise overall summary highlighting the key risks,
important clauses, and obligations.

Summaries:
{combined_text}
"""
    
    final_summary = client.text_generation(
        final_prompt,
        max_new_tokens=300,
        temperature=0.3
    )

    return final_summary