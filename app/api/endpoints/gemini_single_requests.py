from fastapi import HTTPException, status
from app.core.logger import setup_logger
from app.services.ai_client import AIGeminiClient, GeminiGenerationError
from app.models.gemini import GeminiRequest, GeminiRequestWithLocalPrompt, GeminiGererativeModelSettings, GeminiGenirationConfig

logger = setup_logger(__name__)

async def send_text_to_gemini(
    ai_client: AIGeminiClient,
    request_text: str,
):
    if not request_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request text cannot be empty"
        )

    model_settings = GeminiGererativeModelSettings(
        generation_config=GeminiGenirationConfig()
    )

    gemini_request = GeminiRequest(
        request_text=request_text,
        model_settings=model_settings
    )

    return await send_request_to_gemini(ai_client, gemini_request)


async def request_for_gemini_with_local_instructions(
    request: GeminiRequestWithLocalPrompt,
    ai_client: AIGeminiClient,
):
    instruction = ai_client.prompt_engine.prompts.get(
        request.local_prompt_key_name, None
    )
    if instruction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt '{request.local_prompt_key_name}' not found"
        )
    request.model_settings.system_instruction = await instruction.content

    return await send_request_to_gemini(
        ai_client=ai_client,
        request=request,
    )


async def double_request_for_gemini_with_local_instruction(
    request: GeminiRequestWithLocalPrompt,
    ai_client: AIGeminiClient,
):
    instruction = ai_client.prompt_engine.prompts.get(
        request.local_prompt_key_name, None
    )
    if instruction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt '{request.local_prompt_key_name}' not found"
        )
    request.model_settings.system_instruction = await instruction.content
    try:
        chat_session = await ai_client.start_chat(request.model_settings)
        preanswer = await chat_session.send_message_async(content="Начать!")
        answer = await chat_session.send_message_async(content=request.request_text)
    except Exception as e:
        logger.error(f"Error during double request to Gemini: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return [preanswer.to_dict(), answer.to_dict()]


async def send_request_to_gemini(
    ai_client: AIGeminiClient,
    request: GeminiRequest,
):
    try:
        result = await ai_client.generete_message_safe(request)
    except GeminiGenerationError as e:
        logger.error(e.with_traceback())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return result