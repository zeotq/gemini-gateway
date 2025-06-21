from fastapi import HTTPException, status
from app.core.ai_prompt_engine import AIPromptEngine, AIPromptEngineError


_prompt_engine: AIPromptEngine | None = None

async def get_prompt_engine() -> AIPromptEngine:
    global _prompt_engine
    if _prompt_engine is None:
        try:
            _prompt_engine = AIPromptEngine()
            await _prompt_engine.update_prompts_dict()
        except AIPromptEngineError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    return _prompt_engine
