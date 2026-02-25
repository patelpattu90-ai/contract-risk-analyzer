from transformers import pipeline

# Load a pure text-generation model (local, stable)
generator = pipeline(
    "text-generation",
    model="google/flan-t5-base"
)

# =======================
# Day 3: Summarization
# =======================

def summarize_chunks(chunks):
    summaries = []

    for chunk in chunks:
        if not chunk or len(chunk.strip()) < 50:
            continue

        prompt = (
            "Summarize the following contract text clearly and concisely. "
            "Focus on obligations, payments, termination, and risks:\n\n"
            f"{chunk}"
        )

        result = summarizer(
            prompt,
            max_new_tokens=150,
            do_sample=False
        )

        summaries.append(result[0]["generated_text"].strip())

    return "\n".join(summaries)


def summarize_contract(text: str) -> str:
    if not text or len(text.strip()) < 50:
        return "Text too short to summarize."

    prompt = (
        "Summarize the following contract clearly and concisely. "
        "Focus on obligations, payments, termination, and risks:\n\n"
        f"{text[:2000]}"
    )

    result = summarizer(
        prompt,
        max_new_tokens=200,
        do_sample=False
    )

    return result[0]["generated_text"].strip()


# =======================
# Day 4: Risk Analysis
# =======================

RISK_PROMPT = """
The following is a contract clause.

List risks as short bullet points.

Financial Risks:
- late payment penalties

Legal Risks:
- liability exposure

Termination Risks:
- unilateral termination

Ambiguous Clauses:
- unclear notice period

Contract:
{chunk}

Answer:
"""


def analyze_single_chunk(chunk: str) -> dict:
    """
    Analyze ONE contract chunk and extract risks.
    """
    if not chunk or len(chunk.strip()) < 30:
        return {
            "financial_risks": [],
            "legal_risks": [],
            "termination_risks": [],
            "ambiguous_clauses": []
        }

    prompt = RISK_PROMPT.format(chunk=chunk)

    result = generator(
        prompt,
        max_new_tokens=150,
        do_sample=False,
        pad_token_id=generator.tokenizer.eos_token_id
    )

    raw_text = result[0]["generated_text"]

    return parse_risk_response(raw_text)


def parse_risk_response(text: str) -> dict:
    risks = {
        "financial_risks": [],
        "legal_risks": [],
        "termination_risks": [],
        "ambiguous_clauses": []
    }

    current_section = None

    for line in text.splitlines():
        line = line.strip().lower()

        if line.startswith("financial risks"):
            current_section = "financial_risks"
        elif line.startswith("legal risks"):
            current_section = "legal_risks"
        elif line.startswith("termination risks"):
            current_section = "termination_risks"
        elif line.startswith("ambiguous clauses"):
            current_section = "ambiguous_clauses"
        elif line.startswith("-") and current_section:
            risks[current_section].append(line[1:].strip())

    # ✅ FALLBACK LOGIC (outside loop, inside function)
    if not any(risks.values()):
        text_lower = text.lower()

        if "terminate" in text_lower:
            risks["termination_risks"].append("unilateral termination clause")

        if "penalt" in text_lower or "late payment" in text_lower:
            risks["financial_risks"].append("payment penalties")

    return risks


def analyze_risks_for_chunks(chunks: list[str]) -> dict:
    """
    Analyze risks across all chunks and aggregate results.
    """
    aggregated = {
        "financial_risks": set(),
        "legal_risks": set(),
        "termination_risks": set(),
        "ambiguous_clauses": set()
    }

    for chunk in chunks:
        chunk_risks = analyze_single_chunk(chunk)

        aggregated["financial_risks"].update(chunk_risks["financial_risks"])
        aggregated["legal_risks"].update(chunk_risks["legal_risks"])
        aggregated["termination_risks"].update(chunk_risks["termination_risks"])
        aggregated["ambiguous_clauses"].update(chunk_risks["ambiguous_clauses"])

    return {
        "financial_risks": list(aggregated["financial_risks"]),
        "legal_risks": list(aggregated["legal_risks"]),
        "termination_risks": list(aggregated["termination_risks"]),
        "ambiguous_clauses": list(aggregated["ambiguous_clauses"])
    }

def score_risk_severity(risk_text: str) -> dict:
    text = risk_text.lower()

    if any(keyword in text for keyword in [
        "terminate anytime",
        "without notice",
        "penalty",
        "penalties",
        "unlimited liability",
        "indemnify"
    ]):
        return {
            "severity": "High",
            "reason": "High impact or one-sided contractual risk"
        }

    if any(keyword in text for keyword in [
        "may terminate",
        "subject to",
        "renewal",
        "reasonable notice"
    ]):
        return {
            "severity": "Medium",
            "reason": "Conditional or negotiable contractual risk"
        }

    return {
        "severity": "Low",
        "reason": "Minor or ambiguous contractual risk"
    }
def enrich_risks_with_severity(risks: dict) -> dict:
    enriched = {}

    for category, items in risks.items():
        enriched[category] = []

        for risk in items:
            score = score_risk_severity(risk)
            enriched[category].append({
                "risk": risk,
                "severity": score["severity"],
                "reason": score["reason"]
            })

    return enriched