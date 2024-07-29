import logging
import logging

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate
)
from langchain_community.chat_models.openai import ChatOpenAI

class LLMModel:
    def __init__(self, api_key):
        self.api_key = api_key
        self.temperature = 0.7
        self.max_tokens = 1000
        self.top_p = 1.0
        self.frequency_penalty = 0.0
        self.presence_penalty = 0.0
        self.max_retries = 4
        self.request_timeout = 900

    def format_human_template(self, prompt: str) -> HumanMessagePromptTemplate:
        return HumanMessagePromptTemplate(
            prompt=PromptTemplate.from_template(prompt)
        )

    def format_ai_template(self, prompt: str) -> AIMessagePromptTemplate:
        return AIMessagePromptTemplate(
            prompt=PromptTemplate.from_template(prompt)
        )

    def _format_chat_template(self, prompt: str, llm_instructions: str, messages: list=None) -> ChatPromptTemplate:
        human_message_prompt = self.format_human_template(prompt)

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            llm_instructions
        )
        messages.append(system_message_prompt)
        messages.append(human_message_prompt)

        chat_prompt_template = ChatPromptTemplate.from_messages(
            messages
        )

        return chat_prompt_template

    def _create_chain(self, model: ChatOpenAI, formatted_prompt: ChatPromptTemplate) -> LLMChain:
        return LLMChain(llm=model, prompt=formatted_prompt)


class OpenAIModel(LLMModel):
    def __init__(self, api_key, model):
        super().__init__(api_key)
        self.model = model

    def _get_llm(
        self
    ) -> ChatOpenAI:
        print(f"api key: {self.api_key}")
        logging.info(
            f"\n\n Initializing OpenAI Class with parameters model: {self.model}, temperature: {self.temperature}, max_token: {self.max_tokens}, top_p: {self.top_p}, frequency_penalty: {self.frequency_penalty} and presence_penalty: {self.presence_penalty}"
        )
        try:
            return ChatOpenAI(
                openai_api_key=self.api_key,
                max_retries=self.max_retries,
                request_timeout=self.request_timeout,
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
            )
        except Exception as e:
            logging.error(f"Exception in LLM: {e}")
            return None

    async def send_prompt_to_llm(self, prompt: str, llm_instructions: str, messages: list) -> str:
        formatted_prompt = self._format_chat_template(prompt, llm_instructions, messages)
        logging.info(f"Formatted Prompts: {formatted_prompt}")
        chain = self._create_chain(self._get_llm(), formatted_prompt)
        result = await chain.arun({})
        logging.info(f"Result: {result}")
        return result
