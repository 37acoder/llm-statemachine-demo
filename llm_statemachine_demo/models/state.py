from dataclasses import dataclass, field
import xml.etree.ElementTree as ET


@dataclass
class StateNode:
    name: str
    description: str
    paths: list["Path"] = field(default_factory=list)
    data_need_to_collect: list["DataItem"] = field(default_factory=list)

    def add_path(
        self,
        to_node: "StateNode",
        conditions: str,
        need_llm_reply: bool = False,
        llm_reply_guidance: str = "",
        reply_example: str = "",
    ):
        self.paths.append(
            Path(
                self,
                to_node,
                conditions,
                need_llm_reply,
                llm_reply_guidance,
                reply_example,
            )
        )


@dataclass
class StateTransitionResult:
    state: str
    reply_text: str
    data_collected: list = field(default_factory=list)

    @classmethod
    def from_xml(cls, xml_string):
        root = ET.fromstring(xml_string)
        state = root.find("state").text
        reply_text = root.find("reply").text
        data_collected = []
        for item in root.findall("data-collected/item"):
            # Assuming DataItem is a simple class with a value attribute
            data_collected.append(DataItem(item.attrib["key"], item.text))
        return cls(state, reply_text, data_collected)


@dataclass
class DataItem:
    key: str
    value: str = ""
    data_type: str = ""
    description: str = ""


@dataclass
class Path:
    from_node: StateNode
    to_node: StateNode
    conditions: str
    need_llm_reply: bool
    llm_reply_guidance: str
    reply_example: str
