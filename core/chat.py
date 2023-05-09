import json

from langchain.llms import AI21

from core.constants.prompts import (
    system_prompt,
    action_prompt,
    gather_prompt,
    intent_prompt,
)
from core.constants.prompts import (
    message_prompt_template,
    message_intent_template,
    message_successful,
    message_error,
)
from core.models.intents import Intent
from core.execute_action import ExecuteIntent
from core.text_format.message_format import (
    format_conversation_with_incoming,
    parse_intents,
)
from core.text_format.message_format import (
    parse_action_confirmation,
    parse_data_parameters,
)

from langchain.chains import ConversationChain, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from app.config.settings import settings
from typing import Union


class FlowGenius:
    def __init__(self, _id, business_path):
        self.conversation_id: str = _id
        self.business_path: str = business_path

        self.intents: Union[list[Intent], None] = None
        self.auth: Union[dict, None] = None

        self.history: Union[RedisChatMessageHistory, None] = None
        self.memory: Union[ConversationBufferMemory, None] = None
        self.memory_key: str = "history"

        self.conversation_llm: ChatOpenAI | AI21 = ChatOpenAI(
            temperature=0, model_name="gpt-3.5-turbo"
        )
        self.intent_llm: ChatOpenAI | AI21 = AI21(
            temperature=0, model="j2-jumbo-instruct"
        )

        self.schema_llm: ChatOpenAI | AI21 = AI21(
            temperature=0, model="j2-jumbo-instruct"
        )

        self.confirmation_llm: ChatOpenAI | AI21 = AI21(
            temperature=0, model="j2-jumbo-instruct"
        )

        self.verbose: bool = settings.verbose

        self.load_business_data()

        self.execute_intent_class = ExecuteIntent(self.auth)

        self.history = RedisChatMessageHistory(
            session_id=self.conversation_id, url=settings.redis_url
        )
        self.memory = ConversationBufferMemory(
            memory_key=self.memory_key, return_messages=True, chat_memory=self.history
        )

    class Config:
        arbitrary_types_allowed = True

    def converse(self, message: str) -> str:
        messages_template = [
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name=self.memory_key),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]

        formatted_conversation = format_conversation_with_incoming(
            self.history.messages, message
        )
        predicted_intents = self.predict_intents(formatted_conversation)

        should_we_gather_data = True
        for i, intent in enumerate(predicted_intents, 1):
            data_collected = self.predict_gathered_data_for_intent(
                intent, formatted_conversation
            )

            try:
                parsed_info = parse_data_parameters(
                    intent.action_parameters, data_collected
                )

                should_we_gather_data = False

                execute_intent = self.predict_check_for_intent_action(
                    intent=intent,
                    formatted_conversation=formatted_conversation,
                    customer_info=data_collected,
                )

                if execute_intent:
                    (
                        response_action,
                        execution_ok,
                    ) = self.execute_intent_class.execute_action(intent, parsed_info)

                    if execution_ok:
                        messages_template.append(
                            SystemMessagePromptTemplate.from_template(
                                message_successful(intent, response_action)
                            )
                        )
                    else:
                        messages_template.append(
                            SystemMessagePromptTemplate.from_template(message_error())
                        )

                else:
                    messages_template.append(
                        SystemMessagePromptTemplate.from_template(
                            message_intent_template(intent, data_collected)
                        )
                    )

            except ValueError as e:
                print(f"Error: {e}")

            if should_we_gather_data:
                messages_template.append(
                    SystemMessagePromptTemplate.from_template(
                        message_prompt_template(intent, data_collected)
                    )
                )

        chat_prompt_template = ChatPromptTemplate.from_messages(
            messages=messages_template
        )

        conversation_chain = ConversationChain(
            memory=self.memory,
            prompt=chat_prompt_template,
            llm=self.conversation_llm,
            verbose=self.verbose,
        )

        return conversation_chain.predict(input=message)

    def predict_intents(self, formatted_conversation: str) -> list[Intent]:
        intent_prompt_template = PromptTemplate.from_template(intent_prompt)

        intent_chain = LLMChain(
            prompt=intent_prompt_template, llm=self.intent_llm, verbose=self.verbose
        )

        intents_text = intent_chain.predict(
            formatted_intents=self.formatted_intents,
            formatted_conversation=formatted_conversation,
        )

        return parse_intents(self.intents, intents_text)

    def predict_gathered_data_for_intent(
        self, intent: Intent, formatted_conversation: str
    ) -> str:
        gather_data_prompt = PromptTemplate.from_template(gather_prompt)

        gather_data_chain = LLMChain(
            prompt=gather_data_prompt, llm=self.schema_llm, verbose=self.verbose
        )

        gathered_data_text = gather_data_chain.predict(
            intent_name=intent.name,
            action_args=intent.action_parameters,
            formatted_conversation=formatted_conversation,
        )

        return gathered_data_text

    def predict_check_for_intent_action(
        self, intent: Intent, formatted_conversation: str, customer_info: str
    ) -> bool:
        action_confirmation_prompt = PromptTemplate.from_template(action_prompt)

        action_confirmation_chain = LLMChain(
            prompt=action_confirmation_prompt,
            llm=self.confirmation_llm,
            verbose=self.verbose,
        )

        action_confirmation_text = action_confirmation_chain.predict(
            intent=intent.name,
            formatted_conversation=formatted_conversation,
            customer_info=customer_info,
        )

        return parse_action_confirmation(
            action_confirmation_text=action_confirmation_text
        )

    @property
    def formatted_intents(self) -> str:
        return "\n".join(
            [f"- {intent.name} ({intent.description})" for intent in self.intents]
        )

    def load_business_data(self):
        with open(settings.intents_path + self.business_path) as f:
            data = json.load(f)
            data["auth"]["token"] = settings.magic_hotel_api_token

        self.intents = [
            Intent(
                name=intent.get("name"),
                description=intent.get("description"),
                action_url=intent.get("action_url"),
                action_method=intent.get("action_method"),
                action_parameters=intent.get("action_parameters"),
            )
            for intent in data.get("intents")
        ]
        self.auth = data.get("auth")
