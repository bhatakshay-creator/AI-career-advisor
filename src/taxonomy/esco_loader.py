import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"

TECH_KEYWORDS = [
    # Core CS / programming
    "software", "programming", "algorithm", "data structure",
    "python", "java", "javascript", "sql", "code", "coding",
    # Data & ML
    "data", "database", "machine learning", "artificial intelligence",
    "statistics", "analytics", "data science", "data mining",
    # Web & systems
    "web", "network", "cloud", "server", "api", "frontend", "backend",
    # Security & infra
    "security", "cybersecurity", "encryption", "devops",
    # Tools & practices
    "version control", "testing", "debugging", "agile", "automation",
]

def load_esco_skills() -> pd.DataFrame:
    """Load ESCO skills CSV and filter to tech-relevant entries."""
    df = pd.read_csv(DATA_DIR / "skills_en.csv")
    mask = df["preferredLabel"].str.lower().str.contains(
        "|".join(TECH_KEYWORDS), na=False
    ) | df["description"].str.lower().str.contains(
        "|".join(TECH_KEYWORDS), na=False
    )
    return df[mask][["conceptUri", "preferredLabel", "description"]]

def export_for_review(df: pd.DataFrame) -> Path:
    """Save filtered skills to CSV so they can be manually reviewed."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "tech_skills_filtered.csv"
    df.to_csv(out_path, index=False)
    return out_path

if __name__ == "__main__":
    skills = load_esco_skills()
    print(f"Loaded {len(skills)} tech-relevant skills")
    out_path = export_for_review(skills)
    print(f"Exported to {out_path}")