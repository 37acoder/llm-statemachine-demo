import logging
from typing import Dict
from llm_statemachine_demo.models.state import StateNode, DataItem, Path
import yaml


def parse_yaml_config(yaml_config: str) -> Dict[str, StateNode]:
    logging.info("Parsing YAML config, path: %s", yaml_config)
    yaml_data = yaml.safe_load(yaml_config)
    nodes = {}

    # First iteration: create nodes
    for node_name, node_config in yaml_data["nodes"].items():
        node = StateNode(
            name=node_config["name"],
            description=node_config["description"],
        )
        if "data_need_to_collect" in node_config:
            node.data_need_to_collect = []
            for data_item_config in node_config["data_need_to_collect"]:
                data_item = DataItem(
                    key=data_item_config["key"],
                    value=data_item_config.get("value", ""),
                    data_type=data_item_config.get("data_type", ""),
                    description=data_item_config.get("description", ""),
                )
                node.data_need_to_collect.append(data_item)
        nodes[node_name] = node

    # Second iteration: set paths
    for node_name, node in nodes.items():
        node.paths = []
        for path_config in yaml_data["nodes"][node_name].get("paths", []):
            path = Path(
                from_node=node_name,
                to_node=nodes[path_config["to_node"]],
                conditions=path_config.get("conditions", ""),
                need_llm_reply=path_config.get("need_llm_reply", False),
                llm_reply_guidance=path_config.get("llm_reply_guidance", ""),
                reply_example=path_config.get("reply_example", ""),
            )
            node.paths.append(path)

    return nodes


node_mapping = {}


def setup_nodes(path):
    with open(path, "r") as f:
        yaml_config = f.read()
    global node_mapping
    node_mapping = parse_yaml_config(yaml_config)


def get_node(name: str):
    return node_mapping[name]


if __name__ == "__main__":
    with open(
        "./llm_statemachine_demo/templates/decision_trees/user_register.yaml", "r"
    ) as f:
        yaml_config = f.read()
    nodes = parse_yaml_config(yaml_config)
    print(nodes)
