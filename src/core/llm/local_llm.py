from llama_cpp import Llama
from pathlib import Path
from config.settings import LLMConfig, LLMModels
from core.llm.base_llm import BaseLLM
import logging

logger = logging.getLogger(__name__)

MODEL_MAP = {
    LLMModels.LLAMA2_7B: "llama-2-7b-chat.Q4_K_M.gguf",
    LLMModels.MISTRAL_7B: "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
}

class LocalLLM(BaseLLM):
    def __init__(self, model: LLMModels = LLMModels.MISTRAL_7B):
        model_path = Path(LLMConfig.LOCAL_MODEL_PATH) / MODEL_MAP[model]
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        self.llm = Llama(
            model_path=str(model_path),
            n_ctx=2048,
            n_threads=4,
            verbose=False
        )

    def generate(self, context: str, query: str, chat_history: list) -> str:
        prompt = self.format_prompt(context, query, chat_history)
        try:
            output = self.llm(
                prompt,
                max_tokens=LLMConfig.MAX_TOKENS,
                temperature=LLMConfig.TEMPERATURE,
                stop=["Question:", "###"],
                echo=False
            )
            return output["choices"][0]["text"].strip()
        except Exception as e:
            logger.error(f"Local LLM error: {str(e)}")
            return "Error generating response"
