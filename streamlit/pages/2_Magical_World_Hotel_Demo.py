import streamlit as st
from streamlit_chat import message
import requests
from pydantic import BaseModel
import uuid


class ConversationInput(BaseModel):
    conversation_id: str
    message: str


class ConversationResponse(BaseModel):
    message: str


class Message(BaseModel):
    type: str
    content: str


class Conversation(BaseModel):
    messages: list[Message]


def get_conversation_id(conversation_id: str) -> Conversation:
    conversation_url = "http://127.0.0.1:8000/v1/conversation/"
    method = "GET"

    response = requests.request(
        method,
        conversation_url,
        params={"conversation_id": conversation_id},
    )

    return response.json()


def converse(input: ConversationInput) -> ConversationResponse:
    conversation_url = "http://127.0.0.1:8000/v1/conversation/"

    response = requests.post(
        conversation_url,
        json=input.dict(),
    )

    return response.json()


# Set the page title
st.title("🪄 Magical World Hotel")

# Initialize the conversation
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

# Initialize the conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Display the conversation history
for index, chat_message in enumerate(st.session_state.conversation_history):
    message(
        message=chat_message["message"],
        is_user=chat_message["is_user"],
        key=f"chat-message-{index}",
    )

with st.form(key="input_form"):
    # Handle user input
    user_input = st.text_input("Enter your message here:")
    submit_button = st.form_submit_button("Send")

    if submit_button:
        # Send the user's message to the server
        server_response = converse(
            ConversationInput(
                conversation_id=st.session_state.conversation_id, message=user_input
            )
        )

        # Update the conversation history with the user's message
        st.session_state.conversation_history.append(
            {"message": user_input, "is_user": True}
        )

        # Display the server's response
        response_message = server_response["message"]

        # Update the conversation history with the server's response
        st.session_state.conversation_history.append(
            {"message": response_message, "is_user": False}
        )

        # Rerun the app to immediately display the updated conversation history
        st.experimental_rerun()
