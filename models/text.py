from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
import json
import uuid
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "texts.json"


@dataclass
class Text:
    id: str
    user_id: str
    content: str
    language: str
    domain: str
    created_at: str

    @classmethod
    def create(
        cls, content: str, language: str, domain: str, user_id: str = "anonymous"
    ) -> "Text":
        return cls(
            id=str(uuid.uuid4()),
            user_id=user_id,
            content=content,
            language=language,
            domain=domain,
            created_at=datetime.utcnow().isoformat(),
        )


def save_text(text: Text, path: Path | str = DATA_PATH) -> None:
    """Append a text entry to the JSON storage."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    texts = []
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as f:
                texts = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            texts = []
    texts.append(asdict(text))
    with path.open("w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)
