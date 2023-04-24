from core.agent import FlowGeniusAgent


def execute_query_agent(prompt) -> str:
    print(prompt)
    # TODO connect controller with FlowGeniusAgent and return the answer

    openapi_template = 'pet.yaml'
    agent = FlowGeniusAgent(openapi_template)
    return agent.run(prompt)
