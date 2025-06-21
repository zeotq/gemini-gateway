from fastapi import HTTPException, status
from app.core.ai_models_engine import AIModels


_models_engine: AIModels | None = None

async def get_models_engine() -> AIModels:
    global _models_engine
    if _models_engine is None:
        try:
            _models_engine = AIModels()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    return _models_engine
