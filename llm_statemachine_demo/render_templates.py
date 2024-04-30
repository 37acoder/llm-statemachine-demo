import jinja2
import sys

print(sys.path)
from llm_statemachine_demo.models.state import StateNode

templates = jinja2.Environment(
    loader=jinja2.FileSystemLoader("llm_statemachine_demo/templates"),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_decision_prompts(
    now: StateNode, data_collected: dict, history: list, user_input: str
):
    template = templates.get_template("prompts/decision_prompts.jinja")
    rendered_template = template.render(
        {
            "now": now,
            "data_collected": data_collected,
            "history": history,
            "user_input": user_input,
            "data_need_to_collect": [
                i for i in now.data_need_to_collect if i.key not in data_collected
            ],
        }
    )
    return rendered_template


if __name__ == "__main__":
    print(render_decision_prompts(StateNode("now", "description", [], []), {}, [], ""))
