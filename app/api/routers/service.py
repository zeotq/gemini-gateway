from fastapi import Depends, Path
from fastapi.routing import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse

from app.core.ai_prompt_engine import AIPromptEngine
from app.core.ai_models_engine import AIModels
from app.api.endpoints.prompts import \
    get_prompts_list, get_prompts_with_content, get_prompt, \
    get_models_list
from app.services.prompt_engine_provider import get_prompt_engine    
from app.services.models_engine_provider import get_models_engine


service_router = APIRouter(tags=["root, service"])

@service_router.get("/", response_class=RedirectResponse)
async def _redirect_to_docs():
    return RedirectResponse(url="/docs", status_code=302)

@service_router.get("/models", response_class=JSONResponse)
async def _get_models_list(
    ai_models_engine: AIModels = Depends(get_models_engine)
):
    return {"models": await get_models_list(ai_models_engine)}

@service_router.get("/prompts/list", response_class=JSONResponse)
async def _get_prompts_list(prompt_engine: AIPromptEngine = Depends(get_prompt_engine)):
    return JSONResponse(content=await get_prompts_list(prompt_engine))

@service_router.get("/prompts/content", response_class=JSONResponse)
async def _get_prompts_with_content(prompt_engine: AIPromptEngine = Depends(get_prompt_engine)):
    return JSONResponse(content=await get_prompts_with_content(prompt_engine))

@service_router.get("/prompts/{name}", response_class=JSONResponse)
async def _get_prompt_by_name(
    prompt_engine: AIPromptEngine = Depends(get_prompt_engine),
    name: str = Path(..., description="Название промпта"),
):
    return JSONResponse(content=await get_prompt(prompt_engine, name))
