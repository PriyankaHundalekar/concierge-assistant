# src/generator.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.retriever import ConciergeRetriever
from src.tools import lookup_order, extract_order_id
from src.guardrails import detect_human_handoff

class ConciergeGenerator:
    def __init__(self):
        self.retriever = ConciergeRetriever()
        
    def generate_answer(self, query: str):
        # 0. Human Hand-Off Escalation Check
        if detect_human_handoff(query):
            return (
                "**Escalating to Customer Support:**\n"
                "I understand this requires personalized attention. I have flagged your request and connected you with a human support specialist who will review your case shortly.\n\n"
                "*(Action: Routed to Human Support Queue)*"
            ), ["escalation:human_handoff"]

        # 1. Tool Routing Check: Look for Order ID queries
        order_id = extract_order_id(query)
        if order_id:
            order_info = lookup_order(order_id)
            if order_info.get("status") == "Not Found":
                return f"Sorry, I couldn't find order details for **{order_id}**. Please double-check your order number.", ["tool:lookup_order"]
            
            response = (
                f"**Order Status for {order_id}:**\n"
                f"- **Item:** {order_info['item']}\n"
                f"- **Status:** {order_info['status']}\n"
                f"- **Estimated Delivery:** {order_info['delivery_estimate']}\n"
                f"- **Tracking Number:** {order_info['tracking_number']}\n\n"
                f"*(Source: Order Database Tool)*"
            )
            return response, ["tool:lookup_order"]

        # 2. RAG Route: Search indexed policy documents
        retrieved_docs = self.retriever.search(query, top_k=3)
        if not retrieved_docs:
            return "I'm sorry, I couldn't find any relevant policy information to answer your question.", []
            
        context_texts = []
        sources = set()
        for doc in retrieved_docs:
            context_texts.append(f"[{doc['source']}]: {doc['content']}")
            sources.add(doc['source'])
            
        primary_content = retrieved_docs[0]['content'] if retrieved_docs else ""
        response = (
            f"Based on our policy documents ({', '.join(sources)}):\n\n"
            f"{primary_content}\n\n"
            f"*(Sources referenced: {', '.join(sources)})*"
        )
        
        return response, list(sources)

if __name__ == "__main__":
    generator = ConciergeGenerator()
    
    print("--- Test Escalation Route ---")
    ans, srcs = generator.generate_answer("This is unacceptable service, I want to talk to a manager immediately!")
    print(ans)