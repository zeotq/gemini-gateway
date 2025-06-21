import json
from pathlib import Path
from typing import Dict, List

from app.core.logger import setup_logger
from app.core.paths import CONFIG_DIR


logger = setup_logger(__name__)

class AIModels:
    def __init__(self, json_dir_path: Path = CONFIG_DIR, json_name: str = "google_ai_models.example.json"):
        self.file_path = json_dir_path / json_name
        self.models: Dict[str, str] = self._load_models()

    def _load_models(self) -> Dict[str, str]:
        if not self.file_path.exists():
            logger.error(f"Model config file '{self.file_path}' not found.")

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
                else:
                    logger.error("Invalid format in model config file: expected a dictionary.")
        except Exception as e:
            logger.error(f"Failed to load models from JSON: {e}")

        return {}

    def get_all_names(self) -> List[str]:
        return list(self.models.keys())

    def get_model_pairs(self) -> Dict[str, str]:
        return self.models

    def get_model_by_alias(self, alias: str) -> str:
        return self.models.get(alias, "")
