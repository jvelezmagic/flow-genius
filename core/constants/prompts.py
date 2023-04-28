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
    "If the AI agent has asked the customer to review the provided information, "
    "confirmed the action with the customer, and received confirmation from the "
    "customer, respond with 'True' otherwise respond with 'False'.\n"
    "Intent:\n'''\n{intent}\n'''\n"
    "Information collected:\n'''\n{customer_info}\n'''\n"
    "The latest messages are more relevant.\n"
    "Here is the conversation of the customer and the ai agent:\n"
    "'''\n{formatted_conversation}\n'''\n\n"
    "Output should follow the format: 'True/False'\n"
    "Confirmation should be True or False.\n"
)

gather_prompt = dedent(
    "Here is the information you should gather from the customer conversation "
    "to fulfill the intent '{intent_name}':\n"
    "'''\n{action_args}\n'''\n"
    "Here is the conversation of the customer and the ai agent:\n"
    "'''\n{formatted_conversation}\n'''\n\n"
    "Create a key-value pair for each argument in the format: key: value\n"
    "All arguments should be provided.\n"
    "Do not change the order or case of the arguments.\n"
    "If the argument is not provided, leave the value empty.\n"
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
    "Intents:\n"
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


def message_successful(intent):
    return dedent(
        f"You executed the intent: '''{intent.name}''' with description: '''{intent.description}'''."
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
