from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.nlp import load_nlp


def main() -> None:
    print(f"Project root: {PROJECT_ROOT}")
    print("Project structure is ready.")

    nlp = load_nlp()
    if nlp is not None:
        doc = nlp("This project is ready for NLP processing.")
        print("Sample NLP output:", [token.text for token in doc[:6]])
    else:
        print("NLP model not loaded. Install it with: python -m spacy download en_core_web_sm")


if __name__ == "__main__":
    main()
