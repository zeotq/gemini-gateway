import aiofiles
import json
from pathlib import Path

from app.core.logger import setup_logger
from app.core.paths import DATA_DIR, PROMPTS_DIR


logger = setup_logger(__name__)

class AIPromptEngineError(Exception):
    pass

class AIPrompt:
    def __init__(self, name: str, description: str, file_name: str):
        self.__name = name
        self.__description = description
        self.__prompt_file_name = file_name

    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self.__description

    @property
    async def content(self):
        return await self.load_content()

    async def load_content(self) -> str:
        file_path = PROMPTS_DIR / f"{self.__prompt_file_name}"
        if file_path.exists():
            try:
                async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
                    return await file.read()
            except Exception as e:
                logger.error(f"Error reading prompt file '{file_path}': {e}")
                raise AIPromptEngineError(f"Error reading prompt file '{file_path}': {e}")
        else:
            logger.error(f"Prompt file '{file_path}' does not exist.")
            raise AIPromptEngineError(f"Prompt file '{file_path}' does not exist.")

    def __repr__(self):
        return f"AIPrompt(name={self.__name}, description={self.__description}, file_name={self.__prompt_file_name})"
    
    def __str__(self):
        return self.__name


class AIPromptEngine:
    def __init__(self, json_path: Path = DATA_DIR, json_name: str = "prompts.json"):
        self.json_path = json_path
        self.json_name = json_name
        self.prompts: dict[str, AIPrompt] = dict()

    async def update_prompts_dict(self) -> dict[str, AIPrompt]:
        file_path = self.json_path / self.json_name

        if not file_path.exists():
            logger.error(f"Prompts config file '{self.json_name}' not found.")
            raise AIPromptEngineError(f"Prompts config file '{self.json_name}' not found.")

        try:
            async with aiofiles.open(self.json_path / self.json_name, mode="r", encoding="utf-8") as file:
                content = await file.read()
                data = json.loads(content)
                logger.info(f"Loaded prompts from {self.json_path}: {data}")
                if isinstance(data, dict):
                    self.prompts: dict[str, AIPrompt]
                    for name, info_raw in data.items():
                        info: dict[str, str] = info_raw
                        self.prompts[name] = AIPrompt(
                            name=name,
                            description=info.get("description", "No description provided"),
                            file_name=info.get("prompt", "example.txt")
                        )
                else:
                    logger.error("Invalid format in prompts config file: expected a dictionary of dictionaries.")
                    raise AIPromptEngineError("Invalid format in prompts config file: expecteda dictionary of dictionaries.")
                
        except Exception as e:
            logger.error(f"Failed to load models from JSON: {e}")
            raise AIPromptEngineError(f"Failed to load prompts from JSON")

        return self.prompts
    