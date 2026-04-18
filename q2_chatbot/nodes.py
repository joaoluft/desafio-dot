import operator
from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

MODEL_NAME = "gpt-4o-mini"


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    question: str


def generate(state: AgentState) -> dict:
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0.7)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente prestativo. Responda de forma clara e objetiva."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])

    history = state["messages"][:-1] if state["messages"] else []

    chain = prompt | llm
    response = chain.invoke({"history": history, "question": state["question"]})

    return {"messages": [AIMessage(content=response.content)]}
