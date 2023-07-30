"""facade for smarti logic"""

import os

from langchain.schema import (
    HumanMessage,
    SystemMessage
)

from langchain.chat_models import ChatOpenAI



def upload_workbook(stream: bytes) -> int:
    """upload scanned workbook"""
    return len(stream)


def ask_question(message: str) -> str:
    """sends messages to AI bot"""

    answer = ask_local_llm(message)
    if not answer:
        answer = ask_openai_llm(message)
        document = f"Question: {message}\n Answer:{answer}"
        create_embeddings(document)

    return answer


def ask_local_llm(question: str) -> str:
    """ask local LLM to answer question"""
    # implement the local LLM
    return question


def ask_openai_llm(question: str) -> str:
    """ask local LLM to answer question"""
    chat = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.3, openai_api_key=API_KEY)

    messages = [
        SystemMessage(content="Explain to a 7 years old"),
        HumanMessage(content=question)
    ]
    response = chat(messages)
    return question


def create_embeddings(document: str):
    """create embeddings in DB"""
    pass
