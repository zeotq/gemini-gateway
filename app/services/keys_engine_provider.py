from fastapi import HTTPException, status
from app.core.ai_keys_engine import AsyncAPIKeyManager


_keys_engine: AsyncAPIKeyManager | None = None

async def get_keys_engine() -> AsyncAPIKeyManager:
    global _keys_engine
    if _keys_engine is None:
        try:
            _keys_engine = AsyncAPIKeyManager()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    return _keys_engine
