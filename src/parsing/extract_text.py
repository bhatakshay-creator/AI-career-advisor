from pathlib import Path
import pdfplumber
from docx import Document
import re

def extract_text_from_pdf(file_path: Path) -> str:
    """Extract raw text from a PDF resume."""
    text_parts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)

def extract_text_from_docx(file_path: Path) -> str:
    """Extract raw text from a DOCX resume."""
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

def extract_resume_text(file_path: str | Path) -> str:
    """Route to the correct extractor based on file extension."""
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif suffix == ".docx":
        raw_text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    return clean_extracted_text(raw_text)

def clean_extracted_text(text: str) -> str:
      """Remove common PDF extraction artifacts."""
      text = re.sub(r"\(cid:\d+\)", "", text)  # remove cid glyph artifacts
      text = re.sub(r"[ \t]+", " ", text)        # collapse extra spaces
      text = re.sub(r"\n{3,}", "\n\n", text)     # collapse excess blank lines
      return text.strip()   

if __name__ == "__main__":
    # Quick manual test — put a sample resume in data/raw/ and point to it here
    sample_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "sample_resume.pdf"
    if sample_path.exists():
        text = extract_resume_text(sample_path)
        print(text[:1000])  # print first 1000 chars as a sanity check
    else:
        print(f"No sample resume found at {sample_path} — add one to test.")