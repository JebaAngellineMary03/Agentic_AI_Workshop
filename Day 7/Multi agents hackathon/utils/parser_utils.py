import re

def parse_metadata_bullets(metadata_text):
    meta_dict = {}
    lines = metadata_text.split("\n")
    current_key = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = re.match(r"\*+\s*\*\*(.+?)\s*[:：]\s*\*\*\s*(.*)", line)
        if match:
            current_key = match.group(1).strip().lower()
            meta_dict[current_key] = match.group(2).strip()
        elif ":" in line:
            key, value = line.split(":", 1)
            meta_dict[key.strip().lower()] = value.strip()
        elif current_key:
            meta_dict[current_key] += " " + line.strip()
    return meta_dict

def parse_authorship_response(response):
    verdict = "Unknown"
    if "human-authored" in response.lower():
        verdict = "🧠 Human-authored"
    elif "ai-generated" in response.lower():
        verdict = "🤖 AI-generated"
    elif "mixed" in response.lower():
        verdict = "🧬 Mixed"

    checklist = []
    lines = response.split("\n")
    for line in lines:
        if any(word in line.lower() for word in ["structure", "vocabulary", "tone", "consistency", "references", "orcid"]):
            match = re.search(r"^(.*?):\s*(.*)", line)
            if match:
                checklist.append((match.group(1), match.group(2)))
    return verdict, checklist
