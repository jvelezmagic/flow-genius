system_prompt = """
You are Isabella, a chat agent at 'Magical World Hotel'.
Your job is to help customers book rooms and answer their questions.
You are very friendly, helpful, and respectful.
You are also very creative and clever.
You are a human.
"""

action_prompt = """
Answer True if the ai agent already asked the customer to review the information provided and 
confirmed the action and the customer confirmed the action.\n
Intent:\n'''\n{intent}\n'''\n
Information collected:\n'''\n{customer_info}\n'''\n
The latest messages are more relevant.\n
Here is the conversation of the customer and the ai agent:\n
'''{formatted_conversation}\n'''\n\n
Output should follow the format: 'True/False'\n
Confirmation should be True or False.\n
"""

gather_prompt = """
Here is the information you should gather from the customer conversation 
to fulfill the intent '{intent_name}':\n
'''\n{action_args}\n'''\n
Here is the conversation of the customer and the ai agent:\n
'''{formatted_conversation}\n'''\n\n
Create a key-value pair for each argument in the format: 'key: value'\n
All arguments should be provided.\n
Do not change the order or case of the arguments.\n
"""

intent_prompt = """
Mark the intents that best matches the conversation with True or False.\n
Output should follow the format: 'intent_name: True/False'\n
All intents should be marked either True or False.\n
Do not change the order or case of the intents.\n
Do not add or remove any intents.\n
Do not give any other information other than the intent name and True/False.\n
Most recent messages should be considered first to determine the intent of the customer.\n
Intents:\n{formatted_intents}\n\n
Here is the conversation of the customer and the ai agent:\n
'''{formatted_conversation}\n'''\n\n
Intents:
"""


def message_prompt_template(intent, data_collected):
    return f"""
    We detected the intent: '''{intent.name}''' with description: '''{intent.description}'''.
    Here's the information you should collect from the customer to fulfill the intent:\n
    '''\n{intent.action_parameters}\n'''\n
    You can't execute the intent yet because you don't have all the information.
    You can't ask for more information because you don't know what information you need.
    Here's the information you already collected from the customer:\n
    '''\n{data_collected}\n'''\n
    """


def message_intent_template(intent, data_collected):
    return f"""
    We detected the intent: '''{intent.name}''' with description: '''{intent.description}'''.
    You already collected the information from the customer:\n
    '''\n{data_collected}\n'''\n
    Ask the customer for confirmation with all the details you collected from them.
    Ask the customer to review the information and confirm if it's correct.
    """


def message_successful(intent):
    return f"""
    We detected the intent: '''{intent.name}''' with description: '''{intent.description}'''.
    Don't ask the customer for more information.
    You already collected the information from the customer and executed the intent successfully.
    Inform the customer that you executed the intent was successfully.
    """


def message_error():
    return f"""
    The connection with the service is unable. Answer to the client that could try more later.
    """
