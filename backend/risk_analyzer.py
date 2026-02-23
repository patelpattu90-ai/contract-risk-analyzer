RISK_PROMPT = """
You are a contract risk assessment expert.
For the following contract section, list:

1) Financial Risks
2) Legal Risks
3) Termination Risks
4) Ambiguous Clauses

Output bullets for each category, e.g.:

Financial Risks:
- risk1
- risk2

Legal Risks:
- risk1
- risk2

Termination Risks:
- ...

Ambiguous Clauses:
- ...

Contract section:
\"\"\"{text}\"\"\"
"""