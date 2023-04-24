from fastapi import APIRouter
from typing import Union
from app.api.v1.controllers import agent_controllers

router = APIRouter(prefix='/agent')


@router.post("/query")
async def query_agent(prompt: Union[str, None]) -> str:
    if prompt is None:
        raise ValueError('Prompt is required')

    response = agent_controllers.execute_query_agent(prompt)
    return response  # TODO we could create a model response
