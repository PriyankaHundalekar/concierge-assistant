# src/tools.py
import re

def lookup_order(order_id: str) -> dict:
    """Mock database lookup for customer order status."""
    mock_db = {
        "ORD-1001": {
            "status": "Shipped",
            "item": "Wireless Ergonomic Mouse",
            "delivery_estimate": "2 business days",
            "carrier": "FedEx",
            "tracking_number": "FX-992014"
        },
        "ORD-1002": {
            "status": "Processing",
            "item": "Mechanical Keyboard",
            "delivery_estimate": "4-5 business days",
            "carrier": "UPS",
            "tracking_number": "Pending"
        },
        "ORD-1003": {
            "status": "Delivered",
            "item": "USB-C Hub",
            "delivery_estimate": "Delivered yesterday",
            "carrier": "DHL",
            "tracking_number": "DHL-883011"
        }
    }
    
    clean_id = order_id.upper().strip()
    return mock_db.get(clean_id, {
        "status": "Not Found",
        "message": f"Order ID '{order_id}' was not found in our system."
    })

def extract_order_id(query: str) -> str | None:
    """Detect ORD-XXXX patterns in user queries using regex."""
    match = re.search(r"ORD-\d{4}", query, re.IGNORECASE)
    return match.group(0).upper() if match else None

if __name__ == "__main__":
    print("Testing Tool directly:")
    print("ORD-1001 Lookup:", lookup_order("ORD-1001"))
    print("Regex Detection:", extract_order_id("Where is my status for ord-1002 please?"))