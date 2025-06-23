from pydantic import BaseModel
from google.generativeai.types.safety_types import HarmCategory, HarmBlockThreshold
from typing import List


class GeminiSafetySetting(BaseModel):
    category: HarmCategory
    threshold: HarmBlockThreshold

DEFAULT_SAFETY_SETTINGS = [
    GeminiSafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=HarmBlockThreshold.BLOCK_NONE),
    GeminiSafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=HarmBlockThreshold.BLOCK_NONE),
    GeminiSafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=HarmBlockThreshold.BLOCK_NONE),
    GeminiSafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=HarmBlockThreshold.BLOCK_NONE),
]

class GeminiSafetySettingsList(BaseModel):
    gemini_safety_settings: List[GeminiSafetySetting] = DEFAULT_SAFETY_SETTINGS

    def to_dict_list(self) -> List[dict]:
        return [s.model_dump() for s in self.gemini_safety_settings]

class GeminiGenirationConfig(BaseModel):
    temperature: float = 1
    top_p: float = 0.95
    top_k: int = 40
    max_output_tokens: int = 8192
    response_mime_type: str = "text/plain"

class GeminiGererativeModelSettings(BaseModel):
    model_name: str = "gemini-1.5-flash"
    system_instruction: str = None
    safety_settings: GeminiSafetySettingsList = GeminiSafetySettingsList()
    generation_config: GeminiGenirationConfig = GeminiGenirationConfig()

class GeminiRequest(BaseModel):
    request_text: str
    model_settings: GeminiGererativeModelSettings = GeminiGererativeModelSettings()

class GeminiRequestWithLocalPrompt(GeminiRequest):
    request_text: str
    local_prompt_key_name: str
    model_settings: GeminiGererativeModelSettings = GeminiGererativeModelSettings()
