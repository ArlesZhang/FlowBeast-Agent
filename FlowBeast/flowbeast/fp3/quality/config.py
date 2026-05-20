from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class QualitySettings(BaseSettings):
    """
    FP3 Quality Gate configuration.
    All values are overridable via environment variables with QUALITY_ prefix.
    """

    QUALITY_GATE_ENABLED: bool = Field(default=True)

    WEIGHT_HOOK_STRENGTH: float = Field(default=0.20, ge=0.0, le=1.0)
    WEIGHT_EMOTIONAL_INTENSITY: float = Field(default=0.15, ge=0.0, le=1.0)
    WEIGHT_NOVELTY: float = Field(default=0.10, ge=0.0, le=1.0)
    WEIGHT_RETENTION_POTENTIAL: float = Field(default=0.15, ge=0.0, le=1.0)
    WEIGHT_VIRALITY_SIGNALS: float = Field(default=0.10, ge=0.0, le=1.0)
    WEIGHT_PACING: float = Field(default=0.08, ge=0.0, le=1.0)
    WEIGHT_ENGAGEMENT_DENSITY: float = Field(default=0.08, ge=0.0, le=1.0)
    WEIGHT_CONFLICT_DENSITY: float = Field(default=0.08, ge=0.0, le=1.0)
    WEIGHT_REPLAY_POTENTIAL: float = Field(default=0.06, ge=0.0, le=1.0)

    QUALITY_ACCEPT_THRESHOLD: float = Field(default=0.60, ge=0.0, le=1.0)
    QUALITY_REVIEW_THRESHOLD: float = Field(default=0.40, ge=0.0, le=1.0)

    DEDUP_SIMILARITY_THRESHOLD: float = Field(default=0.85, ge=0.0, le=1.0)
    DEDUP_SEARCH_K: int = Field(default=5, ge=1)

    QUALITY_AUDIT_DIR: str = "flowbeast/data/quality_audit"

    model_config = {
        "env_prefix": "QUALITY_",
        "case_sensitive": False,
        "extra": "ignore",
    }

    @property
    def weights_dict(self) -> dict:
        return {
            "hook_strength": self.WEIGHT_HOOK_STRENGTH,
            "emotional_intensity": self.WEIGHT_EMOTIONAL_INTENSITY,
            "novelty": self.WEIGHT_NOVELTY,
            "retention_potential": self.WEIGHT_RETENTION_POTENTIAL,
            "virality_signals": self.WEIGHT_VIRALITY_SIGNALS,
            "pacing": self.WEIGHT_PACING,
            "engagement_density": self.WEIGHT_ENGAGEMENT_DENSITY,
            "conflict_density": self.WEIGHT_CONFLICT_DENSITY,
            "replay_potential": self.WEIGHT_REPLAY_POTENTIAL,
        }


quality_settings = QualitySettings()
