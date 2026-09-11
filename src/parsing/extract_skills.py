"""
extract_skills.py

Extracts skill mentions from resume text by matching against the
ESCO tech-skills vocabulary (built earlier by esco_loader.py).

Uses spaCy's PhraseMatcher for exact/near-exact phrase matching,
which is the standard first-pass approach for skill extraction —
more reliable here than generic NER, since ESCO skill labels are
known, fixed phrases rather than open-ended entity types.
"""

from pathlib import Path
import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from taxonomy.custom_tech_skills import CUSTOM_TECH_SKILLS

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

# Load spaCy's small English model once at module level (expensive to reload)
nlp = spacy.load("en_core_web_sm")


def load_skill_vocabulary() -> pd.DataFrame:
    """Load the filtered ESCO tech-skill list produced by esco_loader.py."""
    path = PROCESSED_DIR / "tech_skills_filtered.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run esco_loader.py first to generate it."
        )
    return pd.read_csv(path)

def build_matcher(skill_df: pd.DataFrame) -> PhraseMatcher:
    """
    Build a spaCy PhraseMatcher from ESCO skill labels + a custom
    tech-tools list (ESCO alone misses specific frameworks/tools).
    """
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

    esco_labels = skill_df["preferredLabel"].dropna().unique().tolist()
    all_labels = list(esco_labels) + CUSTOM_TECH_SKILLS

    # Dedupe case-insensitively, filter out very short/noisy labels
    seen_lower = set()
    clean_labels = []
    for label in all_labels:
        if len(label) <= 2:
            continue
        if label.lower() in seen_lower:
            continue
        seen_lower.add(label.lower())
        clean_labels.append(label)

    patterns = [nlp.make_doc(label) for label in clean_labels]
    matcher.add("SKILL", patterns)
    return matcher


def extract_skills_from_text(text: str, matcher: PhraseMatcher) -> list[dict]:
    """
    Run the matcher over resume text and return matched skills
    with their position and matched surface form (deduplicated).
    """
    doc = nlp(text)
    matches = matcher(doc)

    seen = set()
    results = []
    for match_id, start, end in matches:
        span = doc[start:end]
        skill_text = span.text.lower()
        if skill_text in seen:
            continue
        seen.add(skill_text)
        results.append({
            "matched_text": span.text,
            "start_char": span.start_char,
            "end_char": span.end_char,
        })

    return results


def extract_skills_report(text: str) -> pd.DataFrame:
    """
    Convenience wrapper: load vocab, build matcher, extract skills,
    and return a clean DataFrame ready for gap analysis downstream.
    """
    skill_df = load_skill_vocabulary()
    matcher = build_matcher(skill_df)
    matches = extract_skills_from_text(text, matcher)
    return pd.DataFrame(matches)


if __name__ == "__main__":
    # Quick manual test using one of the sample resumes
    from extract_text import extract_resume_text

    sample_path = RAW_DIR / "sample_resume_2.pdf"
    if not sample_path.exists():
        print(f"No sample resume found at {sample_path} — add one to test.")
    else:
        resume_text = extract_resume_text(sample_path)
        skills_df = extract_skills_report(resume_text)

        print(f"Found {len(skills_df)} matched skills:\n")
        print(skills_df.to_string(index=False))