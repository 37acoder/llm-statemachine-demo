from typing import List, Dict, Any
from collections import UserDict


class Message(dict):
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
        self.state_name: str = ""
        self.data_collected: Dict[str, str] = {}
        self["role"] = role
        self["content"] = content

    def __getitem__(self, i):
        super().__getitem__(i)

    def with_state_name(self, name: str) -> "Message":
        self.state_name = name
        return self

    def with_data_collected(self, key: str, value: str) -> "Message":
        if not self.data_collected:
            self.data_collected = {}
        self.data_collected[key] = value
        return self


class Messages(List[Message]):
    def turn_to_open_ai_messages(self) -> List[Any]:
        return [(msg.role, msg.content) for msg in self]

    def get_now_state_name(self) -> str:
        return self.get_last_assistant_message().state_name

    def get_collected_data(self) -> Dict[str, str]:
        return self.get_last_assistant_message().data_collected

    def get_last_assistant_message(self) -> Message:
        for msg in reversed(self):
            if msg.role == "assistant":
                return msg
        raise ValueError("messages cannot be empty")
