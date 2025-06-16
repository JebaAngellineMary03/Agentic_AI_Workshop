import fitz
import re

def extract_metadata_and_text(file_path):
    doc = fitz.open(file_path)
    full_text = "\n".join([page.get_text() for page in doc])
    first_page = doc[0].get_text()
    doc.close()

    lines = [line.strip() for line in first_page.split("\n") if line.strip()]
    title = "Title not found"
    title_index = -1
    for i, line in enumerate(lines):
        if len(line) > 20 and (line.istitle() or "Attention Is All You Need" in line):
            title = line
            title_index = i
            break

    authors_raw = []
    for line in lines[title_index + 1:]:
        if re.search(r'(?i)abstract', line):
            break
        if '@' not in line and not re.search(r'\b(Google|University|Research|Brain|\.com|\.edu|\.org)\b', line):
            authors_raw.append(line)

    authors_cleaned = []
    for author in authors_raw:
        parts = re.split(r',| and ', author)
        for part in parts:
            cleaned = re.sub(r'[∗†‡]+', '', part).strip()
            if cleaned:
                authors_cleaned.append(cleaned)

    abstract = ""
    abstract_match = re.search(r'(?is)\babstract\b(.*?)(?=\n\d+\s+[A-Z]|\bkeywords\b|\n\n|\nIntroduction)', full_text)
    if abstract_match:
        abstract = abstract_match.group(1).strip()
    else:
        for i, line in enumerate(lines):
            if re.match(r'(?i)^abstract$', line):
                abstract = "\n".join(lines[i + 1:i + 5])
                break

    return {
        "title": title.strip(),
        "authors": ", ".join(authors_cleaned),
        "abstract": abstract.strip(),
        "full_text": full_text
    }

def split_sections(text):
    """
    Splits a research paper into sections based on heading patterns,
    avoiding tables/figures and repeated/incomplete titles.
    """
    section_pattern = re.compile(r'\n\s*(\d{1,2}\.?\s+[A-Z][^\n]{5,100})\n')  
    matches = list(section_pattern.finditer(text))

    sections = {}
    seen_titles = set()

    for i, match in enumerate(matches):
        section_title = match.group(1).strip()

        if section_title in seen_titles or len(section_title.split()) < 2:
            continue
        seen_titles.add(section_title)

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section_content = text[start:end].strip()

        sections[section_title] = section_content

    return sections

def clean_section_titles(sections_dict):
    """
    Cleans section titles by removing only leading numeric index (e.g., '1 ', '12 ')
    while preserving the rest of the title, including numbers like 'Figure 1'.
    """
    cleaned_sections = {}
    seen_titles = set()

    for raw_title, content in sections_dict.items():
        # Remove leading standalone number(s) followed by space(s)
        cleaned_title = re.sub(r'^\d{1,2}\s+', '', raw_title).strip()

        # Avoid duplicates
        if cleaned_title.lower() in seen_titles:
            continue
        seen_titles.add(cleaned_title.lower())

        cleaned_sections[cleaned_title] = content

    return cleaned_sections