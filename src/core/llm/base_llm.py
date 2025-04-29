from abc import ABC, abstractmethod
from typing import List, Dict

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, context: str, query: str) -> str:
        """Generate response given context and query"""
        pass

    @staticmethod
    def format_prompt(context: str, query: str, chat_history: List[Dict]) -> str:
        """Format RAG prompt with context and history"""
        history_str = "\n".join([f"{msg['role']}: {msg['content']}"
           for msg in chat_history[-4:]])
        return f"""Context:
{context}

Chat History:
{history_str}

Question: {query}
Answer:"""
