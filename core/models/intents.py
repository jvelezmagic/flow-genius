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
