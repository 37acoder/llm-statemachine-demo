import jinja2
import pytest


def test_render_decision_prompts():
    # read template from path
    template_path = "llm_statemachine_demo/templates/prompts/decision_prompts.jinja"
    with open(template_path, "r") as f:
        template = jinja2.Template(f.read())

    # render template
    rendered_template = template.render()
    print(rendered_template)
