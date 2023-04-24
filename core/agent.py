import yaml

from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain.llms.ai21 import AI21
from langchain.agents.agent_toolkits.openapi import planner
from langchain.llms.base import LLM
from langchain.requests import RequestsWrapper


class FlowGeniusAgent:
    """
    Flow Genius Agent
    """

    def __init__(self, openapi_template, llm: LLM = None):
        self.requests_wrapper = None
        self.openai_api_spec = None
        self.raw_openai_api_spec = None

        self.openapi_template = openapi_template
        self.load_openapi_template()

        if llm is None:
            self.llm = AI21(model_name="j2-jumbo-instruct", temperature=0.0)
        self.llm = llm

        # TODO agent should have memory to keep in mind the before questions and answer.

    def load_openapi_template(self):
        with open(self.openapi_template) as f:
            self.raw_openai_api_spec = yaml.load(f, Loader=yaml.Loader)
        self.openai_api_spec = reduce_openapi_spec(self.raw_openai_api_spec)

    def create_request_wrapper(self):
        headers = custom_auth_headers(self.raw_openai_api_spec)
        self.requests_wrapper = RequestsWrapper(headers=headers)

    def run(self, prompt):
        agent = planner.create_openapi_agent(self.openai_api_spec, self.requests_wrapper, self.llm)
        agent.run(prompt)


def custom_auth_headers(token):
    return {
        'Authorization': f'Bearer {token}'
    }
