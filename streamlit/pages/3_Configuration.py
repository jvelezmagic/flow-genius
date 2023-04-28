import streamlit as st
import json
from pydantic import BaseModel


class ActionParameter(BaseModel):
    field: str
    format: str
    required: bool


class Intent(BaseModel):
    name: str
    description: str
    action_url: str
    action_method: str
    action_parameters: list[ActionParameter]


def load_intents_from_json(path: str) -> list[Intent]:
    with open(path, "r") as f:
        data = json.load(f)

    intents = [
        Intent(
            name=intent.get("name"),
            description=intent.get("description"),
            action_url=intent.get("action_url"),
            action_method=intent.get("action_method"),
            action_parameters=intent.get("action_parameters"),
        )
        for intent in data.get("intents")
    ]

    return intents


intents_json_file = "./templates/hotel.json"

intents = load_intents_from_json(intents_json_file)


st.title("🧞‍♀️ Flow Genius Configuration")
st.subheader("Service Name")

st.write("The name of the service that will be displayed to the user.")
st.text_input(
    "Service Name", key="service-name", value="Magical World Hotel", disabled=True
)

st.subheader("Agent Name")
st.write("The name of the agent that will be displayed to the user.")
st.text_input("Agent Name", key="agent-name", value="Isabella", disabled=True)

st.subheader("Agent Avatar")
st.write("The avatar of the agent that will be displayed to the user.")
st.text_input(
    "Agent Avatar",
    key="agent-avatar",
    value="https://i.imgur.com/8YQ2Z6j.png",
    disabled=True,
)

st.subheader("Agent Role")
st.write("What should the agent's role be?")
st.text_area(
    "Agent Role",
    key="agent-role",
    value="You are {agent.name}, a chat agent at {agent.service_name}. "
    "Your job is to help customers book rooms and answer their questions. "
    "You are very friendly, helpful, and respectful. "
    "You are also very creative and clever. "
    "You are a human.",
    disabled=True,
)

st.subheader("Agent Intents Detector")
st.write("The intents detector that will be used to detect the user's intent. ")

intent_ui, intent_json = st.tabs(["UI", "JSON Schema"])

with intent_ui:
    add_parameter, remove_parameter = st.columns([2, 2])
    add_parameter.button("Add Intent", key="add-intent", disabled=True)
    remove_parameter.button("Remove Intent", key="remove-intent", disabled=True)
    for i, intent in enumerate(intents):
        expanded = True if i == 0 else False
        with st.expander(f"{intent.name}", expanded=expanded):
            st.subheader(f"{intent.name}")

            with st.container():
                st.text_input(
                    "Intent Name",
                    key=f"intent-name-{intent.name}",
                    value=intent.name,
                    disabled=True,
                )

                st.text_area(
                    "Intent Description",
                    key=f"intent-description-{intent.name}",
                    value=intent.description,
                    disabled=True,
                )

            with st.container():
                st.subheader("Action")

                action_url, action_method = st.columns(2)

                action_url.text_input(
                    "Action URL",
                    key=f"action-url-{intent.name}",
                    value=intent.action_url,
                    disabled=True,
                )

                action_method.selectbox(
                    "Action Method",
                    key=f"action-method-{intent.name}",
                    options=["GET", "POST"],
                    index=0 if intent.action_method == "GET" else 1,
                    disabled=True,
                )

                with st.container():
                    st.subheader("Parameters")

                    add_parameter, remove_parameter = st.columns([2, 2])
                    add_parameter.button(
                        "Add",
                        key=f"add-parameter-{intent.name}",
                        disabled=True,
                    )

                    remove_parameter.button(
                        "Remove",
                        key=f"remove-parameter-{intent.name}",
                        disabled=True,
                    )

                    for action_parameter in intent.action_parameters:
                        ui_name, ui_format, ui_required = st.columns(3)

                        ui_name.text_input(
                            "Field",
                            key=f"field-{intent.name}-{action_parameter.field}",
                            value=action_parameter.field,
                            disabled=True,
                        )

                        ui_format.text_input(
                            "Format",
                            key=f"format-{intent.name}-{action_parameter.field}",
                            value=action_parameter.format,
                            disabled=True,
                        )

                        ui_required.selectbox(
                            "Required",
                            key=f"required-{intent.name}-{action_parameter.field}",
                            options=[True, False],
                            index=0 if action_parameter.required else 1,
                            disabled=True,
                        )

    st.subheader("Authentication")
    st.text_input(
        "Bearer Token",
        key="authentication",
        value="Bearer ",
        disabled=True,
        type="password",
    )

with intent_json:
    intent_json.write("The JSON schema for the intents detector.")

    with open(intents_json_file) as f:
        intents_data = json.load(f)
        del intents_data["auth"]

    intent_json.json(intents_data)
