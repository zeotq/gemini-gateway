from fastapi import HTTPException, status

from app.core.ai_prompt_engine import AIPromptEngine, AIPromptEngineError
from app.core.ai_models_engine import AIModels


async def get_prompts_list(prompt_engine: AIPromptEngine):
    result = []
    try:
        prompts = prompt_engine.prompts.values()
        for prompt in prompts:
            result.append(prompt.name)
    except AIPromptEngineError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return result

async def get_prompts_with_content(prompt_engine: AIPromptEngine):
    result = []
    try:
        prompts = prompt_engine.prompts.values()
        for prompt in prompts:
            content = await prompt.content
            result.append({
                "name": prompt.name,
                "description": prompt.description,
                "content": content
            })
    except AIPromptEngineError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return result

async def get_prompt(prompt_engine: AIPromptEngine, name: str):
    try:
        prompt = prompt_engine.prompts.get(name, None)
        if prompt:
            content = await prompt.content
            return {
                "name": prompt.name,
                "description": prompt.description,
                "content": content
            }
    except AIPromptEngineError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Prompt '{name}' not found"
    )

async def get_models_list(ai_models_engine: AIModels):
    return ai_models_engine.get_model_pairs()
