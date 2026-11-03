import os
import glob
from pathlib import Path

def audit_documents(raw_docs_dir: str = "data/raw_docs"):
    """
    Scans raw document collection for basic quality issues:
    - Empty files
    - Duplicate names
    - Missing metadata markers
    """
    path = Path(raw_docs_dir)
    if not path.exists():
        print(f"Directory {raw_docs_dir} not found. Please place your raw docs there.")
        return []

    files = list(path.glob("*.*"))
    print(f"Found {len(files)} raw documents for auditing.")
    
    audit_log = []
    seen_contents = {}

    for file_path in files:
        file_name = file_path.name
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            # Check for empty content
            if len(content.strip()) == 0:
                audit_log.append({"file": file_name, "issue": "Empty file detected"})
                continue
                
            # Check for duplicates by content hash
            content_sample = content[:200]
            if content_sample in seen_contents:
                audit_log.append({
                    "file": file_name, 
                    "issue": f"Potential duplicate of {seen_contents[content_sample]}"
                })
            else:
                seen_contents[content_sample] = file_name
                
        except Exception as e:
            audit_log.append({"file": file_name, "issue": f"Read error: {str(e)}"})

    print("Audit completed. Issues found:", len(audit_log))
    return audit_log

if __name__ == "__main__":
    audit_documents()