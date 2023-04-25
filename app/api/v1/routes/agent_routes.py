from fastapi import APIRouter, Body
from app.api.v1.controllers import agent_controllers
from pydantic import BaseModel


class QueryPrompt(BaseModel):
    prompt: str


router = APIRouter(prefix="/agent")


@router.post("/query")
async def query_agent(prompt: QueryPrompt) -> str:
    prompt = prompt.prompt

    response = agent_controllers.execute_query_agent(prompt)
    return response  # TODO we could create a model response
