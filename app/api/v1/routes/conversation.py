from fastapi import APIRouter
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI


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
            name="Current Search",
            func=lambda x: x,
            description="useful for when you need to answer questions about current events or the current state of the world",
        ),
    ]

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = ChatOpenAI(temperature=0)
    agent_chain = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
    )

    response = agent_chain.run(input.message)
    return {"answer": response}
