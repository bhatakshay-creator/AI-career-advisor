from __future__ import annotations

from typing import Optional

import spacy


def load_nlp(model_name: str = "en_core_web_sm") -> Optional[spacy.language.Language]:
    """Load the spaCy English model if it is installed."""
    try:
        nlp = spacy.load(model_name)
        return nlp
    except OSError:
        print(f"Model '{model_name}' is not installed. Run: python -m spacy download {model_name}")
        return None
