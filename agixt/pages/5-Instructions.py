import streamlit as st
from streamlit import (
    markdown,
    header,
    checkbox,
    container,
    text_input,
    button,
    spinner,
    error,
    warning,
)
from auth_libs.Users import check_auth_status
from components.agent_selector import agent_selector
from ApiClient import ApiClient

check_auth_status()
agent_name = agent_selector()


def render_history(instruct_container, chat_history):
    instruct_container.empty()
    with instruct_container:
        for instruct in chat_history:
            if "sender" in instruct and "message" in instruct:
                if instruct["sender"] == "User":
                    markdown(
                        f'<div style="text-align: left; margin-bottom: 5px;"><strong>User:</strong> {instruct["message"]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    markdown(
                        f'<div style="text-align: left; margin-bottom: 5px;"><strong>Agent:</strong> {instruct["message"]}</div>',
                        unsafe_allow_html=True,
                    )


header("Instruct an Agent")

smart_instruct_toggle = checkbox("Enable Smart Instruct")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = {}

instruct_container = container()

if agent_name:
    try:
        st.session_state.chat_history[agent_name] = ApiClient.get_chat_history(
            agent_name
        )
    except:
        st.session_state.chat_history[
            agent_name
        ] = []  # initialize as an empty list, not a dictionary

    render_history(instruct_container, st.session_state.chat_history[agent_name])

    instruct_prompt = text_input("Enter your message", key="instruct_prompt")
    send_button = button("Send Message")

    if send_button:
        if agent_name and instruct_prompt:
            with spinner("Thinking, please wait..."):
                if smart_instruct_toggle:
                    response = ApiClient.smartinstruct(
                        agent_name=agent_name,
                        prompt=instruct_prompt,
                        shots=3,
                    )
                else:
                    response = ApiClient.instruct(
                        agent_name=agent_name,
                        prompt=instruct_prompt,
                    )

            instruct_entry = [
                {"sender": "User", "message": instruct_prompt},
                {"sender": "Agent", "message": response},
            ]
            st.session_state.chat_history[agent_name].extend(instruct_entry)
            render_history(
                instruct_container,
                st.session_state.chat_history[agent_name],
            )
        else:
            error("Agent name and message are required.")
else:
    warning("Please select an agent to start instructting.")
