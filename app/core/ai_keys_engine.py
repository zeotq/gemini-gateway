import json
import aiofiles
from pathlib import Path
from typing import List, Optional

from app.core.logger import setup_logger
from app.core.paths import CONFIG_DIR


logger = setup_logger(__name__)

class AIKeyError(Exception):
    pass

class APIKey:
    def __init__(self, name: str, key: str):
        self.name = name
        self.key = key

    def __repr__(self):
        return f"APIKey(name={self.name}, key=***{self.key[-4:]})"


class AsyncAPIKeyManager:
    def __init__(self, dir_path: Path = CONFIG_DIR, json_name: str = "google_api_keys.json"):
        self.json_path = dir_path / json_name
        self.api_keys: List[APIKey] = []
        self.index = 0

    async def load_keys(self):
        if not self.json_path.exists():
            logger.error(f"API keys file '{self.json_path}' not found.")
            raise AIKeyError(f"API keys file '{self.json_path}' not found.")
        try:
            async with aiofiles.open(self.json_path, mode="r", encoding="utf-8") as file:
                content = await file.read()
                data = json.loads(content)

            if not isinstance(data, list):
                logger.error("Invalid format in API key file: expected a list.")
                return

            self.api_keys = [APIKey(entry["name"], entry["key"]) for entry in data if "name" in entry and "key" in entry]
            self.index = 0
            logger.info(f"Loaded {len(self.api_keys)} API keys.")
        except Exception as e:
            logger.error(f"Failed to load API keys: {e}")
            raise AIKeyError(f"Error loading API keys: {e}")

    def get_current_key(self) -> Optional[APIKey]:
        if not self.api_keys:
            logger.warning("No API keys available.")
            return None
        return self.api_keys[self.index]

    def switch_key(self) -> Optional[APIKey]:
        if not self.api_keys:
            logger.warning("No API keys to switch.")
            return None
        self.index = (self.index + 1) % len(self.api_keys)
        logger.info(f"Switched to API key: {self.api_keys[self.index].name}")
        return self.api_keys[self.index]

    def get_all_keys(self) -> List[str]:
        return [k.key for k in self.api_keys]

    def get_all_named_pairs(self) -> List[dict]:
        return [{"name": k.name, "key": k.key} for k in self.api_keys]
