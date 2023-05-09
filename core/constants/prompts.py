import re
from textwrap import dedent
import datetime

system_prompt = dedent(
    "You are Isabella, a chat agent at 'Magical World Hotel'.\n"
    "Your job is to help customers book rooms and answer their questions.\n"
    "You are very friendly, helpful, and respectful.\n"
    "You are also very creative and clever.\n"
    "You are a human.\n"
    "Present yourself to the customer if you haven't already in a natural way.\n"
    f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."
)

action_prompt = dedent(
    "Determine whether the following statements are true by reviewing the conversation "
    "between the AI agent and the customer. Provide a single-word answer: 'True' "
    "if both statements are accurate, and 'False' if either one is incorrect.\n\n"
    "Statements to validate:\n"
    "1. The AI agent has asked the customer to review the captured information.\n"
    "2. The customer has confirmed the action with the AI agent.\n\n"
    "Conversation excerpt:\n"
    "'''\n{formatted_conversation}\n'''\n\n"
    "Related intent and collected information:\n"
    "Intent:\n"
    "'''\n{intent}\n'''\n"
    "Information collected:\n"
    "'''\n{customer_info}\n'''\n\n"
    "Keep in mind that the most recent messages are the most relevant. "
    "Your answer should be either 'True' or 'False' based on the conversation excerpt.\n\n"
    "A simple afirmative answer from the customer is enough to confirm the action.\n"
    "Answer:\n"
)

gather_prompt = dedent(
    "Here is the information you should gather from the customer conversation "
    "to fulfill the intent '{intent_name}':\n"
    "'''\n{action_args}\n'''\n"
    "Here is the conversation of the customer and the ai agent:\n"
    "'''\n{formatted_conversation}\n'''\n\n"
    "Create a key-value pair for each field in the format: 'key: value'\n"
    "All fields should be provided.\n"
    "Do not change the order or case of the fields.\n"
    "If the field value is not provided, leave the value empty.\n"
    "Output example:\n"
    "field: value\n"
    "field2: value2\n"
    "\n\n"
    "Extracted information:\n"
)

intent_prompt = dedent(
    "Mark the intents that best matches the conversation with True or False.\n"
    "Output should follow the format: 'intent_name: True/False'\n"
    "All intents should be marked either True or False.\n"
    "Do not change the order or case of the intents.\n"
    "Do not add or remove any intents.\n"
    "Do not give any other information other than the intent name and True/False.\n"
    "Most recent messages should be considered first to determine the intent of the customer.\n"
    "Intents:\n{formatted_intents}\n\n"
    "Here is the conversation of the customer and the ai agent:\n"
    "'''\n{formatted_conversation}\n'''\n\n"
    "Mark the intents that best matches the conversation with True or False.\n"
    "Output should follow the format: 'intent_name: True/False'\n"
    "Do not change the order or case of the intents.\n"
    "Do not add or remove any intents.\n"
    "Do not give any other information other than the intent name and True/False.\n"
    "Predicted intents:\n"
)


def message_prompt_template(intent, data_collected):
    return dedent(
        f"We detected the intent: '''{intent.name}''' with description: '''{intent.description}'''.\n"
        "Here's the information you should collect from the customer to fulfill the intent:\n"
        f"'''\n{intent.action_parameters}'''\n"
        "You can't execute the intent yet because you don't have all the information.\n"
        "You can't ask for more information because you don't know what information you need.\n"
        "Here's the information you already collected from the customer:\n"
        f"'''\n{data_collected}\n'''\n"
    )


def message_intent_template(intent, data_collected):
    return dedent(
        f"We detected the intent: '''{intent.name}''' with description: '''{intent.description}'''.\n"
        "You already collected the information from the customer.\n"
        "Here's the information collected: \n"
        f"'''\n{data_collected}\n'''\n"
        "Ask the customer for confirmation with all the details you collected from them.\n"
        "Ask the customer to review the information and confirm if it's correct."
    )


def message_successful(intent, data: str):
    pattern = r"[{}]"
    data = re.sub(pattern, "\n", data)
    return dedent(
        f"You executed the intent: '''{intent.name}''' with description: '''{intent.description}'''."
        f"Response to the user with the next information: '''{data}'''. "
        "Don't ask the customer for more information.\n"
        "You already collected the information from the customer and executed the intent successfully.\n"
        "Inform the customer that you executed the intent was successfully.\n"
        "Inform the customer that you executed the intent was successfully.\n"
        "Don't ask the customer for more information.\n"
    )


def message_error():
    return dedent(
        "There was an error executing the intent.\n"
        "Inform the customer that there was an error executing the intent.\n"
        "Answer to the client that could try again later.\n"
    )
