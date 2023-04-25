from fastapi import APIRouter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.schema import messages_to_dict
from pydantic import BaseModel, constr

from app.config.settings import settings


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
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."
            ),
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

    # TODO: Implement a method to detect client's intent (e.g., booking a room, change reservation, cancel reservation, etc.)
    # TODO: Implement a method to gather all the information needed through user conversation (e.g., name, dastes, price, type of room, etc.)
    # TODO: Implement a method to run the intention once all the information is gathered.
    # TODO: Implement a method to inform the user about the result of ther intention.

    result = conversation.predict(input=input.message)

    return {"answer": result}
