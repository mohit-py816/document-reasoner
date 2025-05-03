import os
import json
from pathlib import Path

class FileManager:
    def __init__(self):
        self.data_path = Path("data/chat_history")
        self.data_path.mkdir(parents=True, exist_ok=True)

    def get_history_path(self, filename):
        return self.data_path / f"{Path(filename).stem}_history.json"

    def save_chat(self, filename, messages):
        with open(self.get_history_path(filename), "w") as f:
            json.dump(messages, f)

    def load_chat(self, filename):
        path = self.get_history_path(filename)
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return []

    def save_conversation(self, doc_id: str, messages: list):
        """Save conversation history for a document"""
        path = self.data_path / f"{doc_id}_convo.json"
        with open(path, "w") as f:
            json.dump({
                "doc_id": doc_id,
                "timestamp": datetime.now().isoformat(),
                "messages": messages
            }, f)

    def load_conversations(self, doc_id: str) -> list:
        """Load all conversations for a document"""
        pattern = f"{doc_id}_convo_*.json"
        return sorted(self.data_path.glob(pattern), key=os.path.getmtime, reverse=True)
