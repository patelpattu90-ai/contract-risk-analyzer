# utils/llm.py

from transformers import pipeline

# Load a pure text-generation model (local, stable)
generator = pipeline(
    "text-generation",
    model="distilgpt2"
)

def summarize_chunks(chunks):
    """
    Summarize each chunk individually and combine results.
    """
    summaries = []

    for chunk in chunks:
        if not chunk or len(chunk.strip()) < 30:
            continue

        prompt = (
            "Summarize the following contract text in simple terms:\n\n"
            f"{chunk}\n\nSummary:"
        )

        result = generator(
         prompt,
         max_new_tokens=120,
         do_sample=False,
         pad_token_id=generator.tokenizer.eos_token_id
)

        summaries.append(result[0]["generated_text"])

    return "\n\n".join(summaries)


def summarize_contract(text: str) -> str:
    """
    Summarize full contract text without chunking (fallback).
    """
    if not text or len(text.strip()) < 50:
        return "Text too short to summarize."

    prompt = (
        "Summarize the following contract in simple terms:\n\n"
        f"{text[:2000]}\n\nSummary:"
    )

    result = generator(
        prompt,
        max_new_tokens=200,
        do_sample=False
    )

    return result[0]["generated_text"]
