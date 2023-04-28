from fastapi import APIRouter
from langchain.memory import RedisChatMessageHistory
from langchain.schema import messages_to_dict
from pydantic import BaseModel, constr

from app.config.settings import settings
from core.chat import FlowGenius


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
async def conversation(data: ConversationInput):
    flow_genius = FlowGenius(data.conversation_id, 'hotel.json')

    return flow_genius.converse(data.message)
