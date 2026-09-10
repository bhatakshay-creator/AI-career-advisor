import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

TECH_KEYWORDS = [
    "software", "data", "programming", "cloud", "database",
    "machine learning", "web", "network", "security", "python",
]

def load_esco_skills() -> pd.DataFrame:
    """Load ESCO skills CSV and filter to tech-relevant entries."""
    df = pd.read_csv(DATA_DIR / "skills_en.csv")
    mask = df["preferredLabel"].str.lower().str.contains(
        "|".join(TECH_KEYWORDS), na=False
    )
    return df[mask][["conceptUri", "preferredLabel", "description"]]

if __name__ == "__main__":
    skills = load_esco_skills()
    print(f"Loaded {len(skills)} tech-relevant skills")
    print(skills.head())