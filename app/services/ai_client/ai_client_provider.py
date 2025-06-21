from fastapi import Depends, HTTPException, status
from app.services.ai_client.ai_client import AIGeminiClient

from app.core.ai_prompt_engine import AIPromptEngine
from app.core.ai_models_engine import AIModels
from app.core.ai_keys_engine import AsyncAPIKeyManager

from app.services.prompt_engine_provider import get_prompt_engine
from app.services.keys_engine_provider import get_keys_engine
from app.services.models_engine_provider import get_models_engine


_ai_client: AIGeminiClient | None = None

async def get_ai_client(
    prompt_engine: AIPromptEngine = Depends(get_prompt_engine),
    keys_engine: AsyncAPIKeyManager = Depends(get_keys_engine),
    models_engine: AIModels = Depends(get_models_engine)

) -> AIGeminiClient:
    global _ai_client
    if _ai_client is None:
        try:
            _ai_client = AIGeminiClient(prompt_engine, keys_engine, models_engine)
            await _ai_client.initialize()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    return _ai_client
