# Project Concierge - Failure & Robustness Log (`FAILURES.md`)

## Adversarial Findings & Edge Cases

1. **Out-of-Bounds Queries (e.g., Flight Bookings)**
   - **Observation:** When asked about booking flights, the retriever returns lowest-distance policy chunks (like shipping policy) because no strict confidence score cutoff exists yet.
   - **Mitigation / Next Step (Day 3):** Implement a similarity distance threshold or a lightweight classifier to reject queries when top vector distance exceeds a safe tolerance.

2. **Malformed Order IDs**
   - **Observation:** Regex successfully captures `ORD-\d{4}` patterns. Non-existent IDs like `ORD-9999` return a clean dictionary lookup message instead of throwing server errors.

3. **Prompt Injection Resilience**
   - **Observation:** Because the system prompt uses strict delimiters and grounded context formatting, naive injection attempts are treated as standard literal text queries.