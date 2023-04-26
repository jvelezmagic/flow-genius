import os
from typing import List

from langchain import ConversationChain, PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import AI21
from langchain.memory import RedisChatMessageHistory, ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate
from langchain.prompts import MessagesPlaceholder
from langchain.prompts import HumanMessagePromptTemplate

from langchain.schema import messages_to_dict


class FlowGeniusChat:
    def __init__(self, _id, intents: List):
        self._id = _id
        self.intents = intents

        self.intent_prompt_template = None
        self.history = None
        self.conv_chain = None
        self.prompt = None

        self.prompt_model = ChatOpenAI(temperature=0)
        self.intent_model = AI21(model='j2-grande-instruct', temperature=0)
        self.params_model = ChatOpenAI(temperature=0)

        self.start_chat()
        self.start_intent()

    def start_chat(self):
        system_prompt = (
            "You are Isabella, a chat agent at 'Magical World Hotel'."
            "Your job is to help customers book rooms and answer their questions."
            "You are very friendly, helpful, and respectful."
            "You are also very creative and clever."
            "You are a human."
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(system_prompt),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )

        self.history = RedisChatMessageHistory(session_id=self._id, url=os.getenv('REDIS_URL'))

        memory = ConversationBufferMemory(
            memory_key=os.getenv('CONV_MEMORY_VAL'),
            return_messages=True,
            chat_memory=self.history,
        )

        self.conv_chain = ConversationChain(
            memory=memory,
            prompt=prompt,
            llm=self.prompt_model,
        )

    def start_intent(self):
        def rename_intent(action: str) -> str:
            return f'- {action} : 1 for True, 0 for False \n'

        actions = [rename_intent(i['action']) for i in self.intents]

        self.intent_prompt_template = PromptTemplate(
            template=(
                "Indicate whether the client wants to do some of the following intents:\n"
                f"'''\n{actions}'''\n\n"
                "\n"
                "Mark the intent(s) that the client wants to do with 1 for True or 0 for False\n"
                "Do not change the order and case of the intents.\n\n"
                "This is the conversation between you and the client:\n"
                "'''\n{conversation}'''\n\n"
                "Intents:"
            ),
            input_variables=["conversation"],
        )

    def run_chain(self, message):
        action = self.detect_intent(message)

        def rename_parameter(parameter: dict) -> str:
            return '-' + parameter['field'] + ' as ' + parameter['format'] + '\n'

        if action:
            intent = [i for i in self.intents if i['action'] == action]

            if intent:
                parameters = ' '.join([rename_parameter(i) for i in intent[0]['parameters']])

                self.check_parameter_and_run_intent(message, str(parameters))

        return self.conv_chain.predict(input=message)

    def detect_intent(self, message):
        formatted_conversation = (
                "\n".join(
                    [
                        f"{message.get('type')}: {message.get('data').get('content')}"
                        for message in messages_to_dict(self.history.messages)
                    ]
                )
                + f"\nhuman: {message}"
        )

        chain = LLMChain(
            llm=self.intent_model,
            prompt=self.intent_prompt_template,
        )

        result = chain.predict(conversation=formatted_conversation)

        intention_list = [i.split(':') for i in result.split('\n') if len(i.split(':')) == 2]

        intent = None
        pos = 0
        while pos < len(intention_list) and intent is None:
            name = intention_list[pos][0]
            is_true = int(intention_list[pos][1])

            if is_true:
                intent = name

        return intent

    def check_parameter_and_run_intent(self, message, parameters: str):

        formatted_conversation = (
                "\n".join(
                    [
                        f"{message.get('type')}: {message.get('data').get('content')}"
                        for message in messages_to_dict(self.history.messages)
                    ]
                )
                + f"\nhuman: {message}"
        )

        parameters_prompt = PromptTemplate(
            template=(
                "Check if the user has entered the following parameters: \n"
                f"'''\n{parameters}'''\n\n"
                "\n"
                "response 1 for True or 0 for False\n"
                "This is the conversation between you and the client:\n"
                "'''\n{conversation}'''\n\n"
            ),
            input_variables=["conversation"],
        )

        chain = LLMChain(
            llm=self.params_model,
            prompt=parameters_prompt,
        )

        result = chain.predict(conversation=formatted_conversation)

        print(result)

        return result
