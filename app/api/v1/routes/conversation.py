import os
import json
from fastapi import APIRouter
from langchain.chains import ConversationChain, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import AI21
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import messages_to_dict
from pydantic import BaseModel, constr

from app.config.settings import settings

from core.chat import FlowGeniusChat


class Message(BaseModel):
    type: constr(regex="^(human|ai)$")
    content: str


class Conversation(BaseModel):
    messages: list[Message]


class ConversationInput(BaseModel):
    conversation_id: str
    message: str


router = APIRouter(prefix="/conversation")


@router.get("/")
async def get_conversation(conversation_id: str) -> Conversation:
    history = RedisChatMessageHistory(
        session_id=conversation_id, url=settings.redis_url
    )

    output = [
        {
            "type": message.get("type"),
            "content": message.get("data").get("content"),
        }
        for message in messages_to_dict(history.messages)
    ]
    return {"messages": output}


@router.post("/")
async def conversation(input: ConversationInput):
    system_prompt = (
        "You are Isabella, a chat agent at 'Magical World Hotel'."
        "Your job is to help customers book rooms and answer their questions."
        "You are very friendly, helpful, and respectful."
        "You are also very creative and clever."
        "You are a human."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )

    llm = ChatOpenAI(temperature=0)

    history = RedisChatMessageHistory(
        session_id=input.conversation_id, url=settings.redis_url
    )

    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True,
        chat_memory=history,
    )

    conversation = ConversationChain(
        memory=memory,
        prompt=prompt,
        llm=llm,
    )

    formatted_conversation = (
            "\n".join(
                [
                    f"{message.get('type')}: {message.get('data').get('content')}"
                    for message in messages_to_dict(history.messages)
                ]
            )
            + f"\nhuman: {input.message}"
    )

    print(formatted_conversation)

    intent = identify_intent(formatted_conversation)

    print(intent)
    # TODO: Implement a method to detect client's intent (e.g., booking a room, change reservation, cancel reservation, etc.)
    # TODO: Implement a method to gather all the information needed through user conversation (e.g., name, dastes, price, type of room, etc.)
    # TODO: Implement a method to run the intention once all the information is gathered.
    # TODO: Implement a method to inform the user about the result of ther intention.

    result = conversation.predict(input=input.message)

    return {"answer": result}


@router.post("/start")
async def start_conversation(data: ConversationInput):
    path = os.getcwd() + os.sep + 'templates' + os.sep + 'base.json'
    with open(path, 'r') as file:
        file_data = file.read()
        file.close()
    business = json.loads(file_data)

    intents = business['intents']

    chat = FlowGeniusChat(data.conversation_id, intents)

    return {"answer": chat.run_chain(data.message)}


def identify_intent(conversation):
    llm = AI21(model='j2-grande-instruct', temperature=0)

    prompt = PromptTemplate(
        template=(
            "Indicate whether the client wants to do some of the following intents:\n"
            "- create-reservation: 1 for True / 0 for False \n"
            "- update-reservation: 1 for True / 0 for False \n"
            "- cancel-reservation: 1 for True / 0 for False \n"
            "- ask-for-information: 1 for True / 0 for False \n"
            "\n"
            "Mark the intent(s) that the client wants to do with 1 for True or 0 for False\n"
            "Do not change the order and case of the intents."
            "\n\n"
            "This is the conversation between you and the client:\n"
            "'''\n{conversation}'''"
            "\n\n"
            "Intents:"
        ),
        input_variables=["conversation"],
    )

    chain = LLMChain(
        llm=llm,
        prompt=prompt,
    )

    result = chain.predict(conversation=conversation)

    return {"answer": result}
