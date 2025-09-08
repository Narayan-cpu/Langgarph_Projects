from dotenv import load_dotenv
from typing import List,TypedDict
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq

load_dotenv()

class AgentAction(TypedDict):
    message:List[HumanMessage]

llm=ChatGroq(model="deepseek-r1-distill-llama-70b")

def process(state:AgentAction)->AgentAction:
    '''LLM Integration'''
    response=llm.invoke(state["message"])
    print("Bot:",response.content)
    return state


graph=StateGraph(AgentAction)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)
agent=graph.compile()

user_input=input("User: ")
while user_input.lower()!="exit":
    agent.invoke({"message":[HumanMessage(content=user_input)]})
    user_input=input("User:")