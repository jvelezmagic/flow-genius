from fastapi import APIRouter
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory
from pydantic import BaseModel

from app.config.settings import settings


class ConversationInput(BaseModel):
    conversation_id: str
    message: str


router = APIRouter(prefix="/conversation")


@router.get("/")
async def get_conversation():
    return {"message": "Hello World"}


@router.post("/")
async def conversation(input: ConversationInput):
    tools = [
        Tool(
            name="Dummy",
            func=lambda x: x,
            description="useful for when you need to answer questions about current events or the current state of the world",
        ),
    ]

    history = RedisChatMessageHistory(
        session_id=input.conversation_id, url=settings.redis_url
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        chat_memory=history,
    )

    llm = ChatOpenAI(temperature=0)

    # TODO: avoid infinite loop of thoughts
    agent_chain = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
    )

    response = agent_chain.run(input.message)
    # print(memory.chat_memory.messages)

    return {"answer": response}
