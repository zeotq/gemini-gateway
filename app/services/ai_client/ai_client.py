import google.generativeai as genai

from app.core.logger import setup_logger
from app.core.ai_keys_engine import AsyncAPIKeyManager
from app.core.ai_models_engine import AIModels
from app.core.ai_prompt_engine import AIPromptEngine
from app.models.gemini import GeminiRequest, GeminiGererativeModelSettings

logger = setup_logger(__name__)


class GeminiGenerationError(Exception):
    pass


class AIGeminiClient:
    def __init__(
        self, 
        prompt_engine: AIPromptEngine,
        api_key_manager: AsyncAPIKeyManager,
        ai_models_engine: AIModels

    ):
        self.prompt_engine = prompt_engine
        self.api_key_manager = api_key_manager
        self.ai_models_engine = ai_models_engine

    async def initialize(self):
        await self.api_key_manager.load_keys()
        await self.prompt_engine.update_prompts_dict()

        # Key checking
        key = self.api_key_manager.get_current_key()
        if key is None:
            raise RuntimeError("API keys are missing. Please check server configuration.")
        genai.configure(api_key=key.key)

        logger.info(f"AIClient initialized")

    async def model_generation(self, request: GeminiGererativeModelSettings) -> genai.GenerativeModel:
        model = genai.GenerativeModel(
            model_name=request.model_name,
            generation_config=request.generation_config.model_dump(),
            system_instruction=request.system_instruction,
            safety_settings=request.safety_settings.to_dict_list()
        )
        return model

    async def generate_message(self, request: GeminiRequest) -> str:
        model: genai.GenerativeModel = await self.model_generation(request)
        response = await model.generate_content_async(contents=request.request_text)
        return response.to_dict()

    async def start_chat(self, request: GeminiGererativeModelSettings) -> genai.ChatSession:
        model: genai.GenerativeModel = await self.model_generation(request)
        chat_session: genai.ChatSession = model.start_chat()
        return chat_session
    
    async def send_message_to_chat(self, chat_session: genai.ChatSession, request: GeminiRequest) -> str:
        await chat_session.send_message_async(request.request_text)