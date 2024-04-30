from llm_statemachine_demo.models.message import Messages, Message
from llm_statemachine_demo.render_templates import render_decision_prompts
from llm_statemachine_demo.models.state import StateTransitionResult
from llm_statemachine_demo.decision_tree import get_node  


def GetTemplate(messages: Messages) -> Messages:
    now_state_name = messages.get_now_state_name()
    if now_state_name == "":
        raise ValueError("now state name is empty")
    now_state_node = get_node(now_state_name)
    if now_state_node is None:
        raise ValueError(f"now state name {now_state_name} is not in NodeNameMapping")
    user_input = messages[-1].content

    return render_decision_prompts(
        now_state_node,
        messages.get_collected_data(),
        history=messages[-5:-1],
        user_input=user_input,
    )


def ParseLLMResponse(llm_response: str) -> Message:
    if not llm_response.startswith("<response>"):
        llm_response = llm_response[llm_response.find("<response>") :]
    state_transition_result = StateTransitionResult.from_xml(llm_response)
    new_message = Message(
        role="assistant",
        content=state_transition_result.reply_text,
    ).with_state_name(state_transition_result.state)
    for item in state_transition_result.data_collected:
        new_message = new_message.with_data_collected(item.key, item.value)
    return new_message
