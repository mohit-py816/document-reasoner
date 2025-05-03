import openai
from config.settings import LLMConfig, LLMModels
from core.llm.base_llm import BaseLLM
import logging

logger = logging.getLogger(__name__)

class OpenAIManager(BaseLLM):
    def __init__(self, model: LLMModels = LLMModels.OPENAI_GPT4):
        openai.api_key = LLMConfig.OPENAI_API_KEY
        self.model = model.value

    def generate(self, context: str, query: str, chat_history: list) -> str:
        try:
            prompt = self.format_prompt(context, query, chat_history)
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=LLMConfig.TEMPERATURE,
                max_tokens=LLMConfig.MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return "I'm having trouble connecting to the AI service."
