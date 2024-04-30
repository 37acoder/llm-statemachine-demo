import logging

logging.basicConfig(level=logging.INFO)
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
import os
from llm_statemachine_demo.components.llm import llm
from llm_statemachine_demo.models.message import Message, Messages
from llm_statemachine_demo.llm_call import GetTemplate, ParseLLMResponse
from llm_statemachine_demo.decision_tree import setup_nodes, get_node

setup_nodes("./llm_statemachine_demo/templates/decision_trees/user_register.yaml")


def default_messages() -> Messages:
    m = Messages()
    m.append(
        Message(
            "assistant",
            "I'm your register bot, a bot can help you to register, Do you want to register?",
        ).with_state_name("user_enter")
    )
    return m


if "messages" not in st.session_state:
    st.session_state["messages"] = default_messages()

with st.sidebar:
    st.title("💬 State LLM Chat")
    stateInfo = get_node(st.session_state["messages"].get_now_state_name())
    st.header("Now state")
    st.table(
        [
            {
                "state": stateInfo.name,
                "description": stateInfo.description,
                "data_need_to_collect": str(stateInfo.data_need_to_collect),
            }
        ]
    )
    st.header("available next state")
    st.table(
        [
            {
                "state": state.to_node.name,
                "description": state.to_node.description,
                "conditions": state.conditions,
            }
            for state in stateInfo.paths
        ]
    )
for msg in st.session_state.messages:
    if msg.role == "system":
        continue
    st.chat_message(msg.role).write(msg.content)

if user_input := st.chat_input():
    st.session_state.messages.append(Message("user", user_input))
    st.chat_message("user").write(user_input)

    result = ""
    with st.chat_message("assistant"):
        text_element = st.markdown(result)
        prompt = GetTemplate(st.session_state.messages)
        print(prompt)
        in_reply = False
        reply = ""
        for chunk in llm.stream(prompt):
            result += chunk.content
            if "<reply>" in result and not in_reply and reply == "":
                in_reply = True
                reply += result[result.find("<reply>") + 6 :]
                continue
            if in_reply:
                reply += chunk.content
                if "</reply>" in result and in_reply:
                    in_reply = False
                    reply = reply.replace("</reply>", "")
                text_element.markdown(reply)
        print("LLM RESPONSE \n: {}".format(result))

    st.session_state.messages.append(ParseLLMResponse(result))
    st.rerun()
