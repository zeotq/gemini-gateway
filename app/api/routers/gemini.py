from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from app.api.endpoints.gemini_single_requests import send_request_to_gemini, send_text_to_gemini, request_for_gemini_with_local_instructions, double_request_for_gemini_with_local_instruction
from app.services.ai_client import AIGeminiClient
from app.services.ai_client import get_ai_client
from app.models.gemini import GeminiRequest, GeminiRequestWithLocalPrompt

gemini_router = APIRouter(prefix="/gemini", tags=["gemini"])

@gemini_router.get("/", response_class=JSONResponse)
async def _only_text_request_for_gemini(
    ai_client: AIGeminiClient = Depends(get_ai_client),
    request_text: str = "",
):
    return await send_text_to_gemini(
        ai_client=ai_client,
        request_text=request_text,
    )

@gemini_router.post("/", response_class=JSONResponse)
async def _full_request_for_gemini_with_settings(
    request: GeminiRequest,
    ai_client: AIGeminiClient = Depends(get_ai_client),
):
    return await send_request_to_gemini(
        ai_client=ai_client,
        request=request,
    )

@gemini_router.post("/withinst", response_class=JSONResponse)
async def _request_for_gemini_with_local_instructions(
    request: GeminiRequestWithLocalPrompt,
    ai_client: AIGeminiClient = Depends(get_ai_client),
):
    return await request_for_gemini_with_local_instructions(
        ai_client=ai_client,
        request=request,
    )
    
@gemini_router.post("/warminst", response_class=JSONResponse)
async def _double_request_for_gemini_with_local_instruction(
    request: GeminiRequestWithLocalPrompt,
    ai_client: AIGeminiClient = Depends(get_ai_client),
):
    """
    Double request with warming up the model
    """
    return await double_request_for_gemini_with_local_instruction(
        ai_client=ai_client,
        request=request,
    )
    