# src/guardrails.py
import re

def detect_human_handoff(query: str) -> bool:
    """Detects if a user query requires human intervention based on frustration, legal threats, or explicit requests."""
    escalation_keywords = [
        r"talk to a human", r"speak to a manager", r"customer service agent",
        r"lawyer", r"sue", r"fraud", r"unacceptable", r"dispute charge",
        r"angry", r"terrible service", r"human representative"
    ]
    
    query_lower = query.lower()
    for pattern in escalation_keywords:
        if re.search(pattern, query_lower):
            return True
    return False

if __name__ == "__main__":
    print("Testing Human Hand-off Detector:")
    print("'I want to speak to a human agent please' -> Escalation:", detect_human_handoff("I want to speak to a human agent please"))
    print("'What is your return window?' -> Escalation:", detect_human_handoff("What is your return window?"))