from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductionNLPConfig:
    """Configuration for production NLP service loaded from environment."""

    spacy_model: str = os.getenv("SPACY_MODEL", "pt_core_news_lg")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_ssl: bool = os.getenv("REDIS_SSL", "false").lower() == "true"
    redis_password: Optional[str] = os.getenv("REDIS_PASSWORD")

    def __post_init__(self) -> None:
        if self.redis_ssl and not self.redis_password:
            raise ValueError("Redis password required when SSL is enabled")
