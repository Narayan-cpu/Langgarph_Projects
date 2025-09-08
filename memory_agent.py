from dotenv import load_dotenv
from typing import List,TypedDict,Union
from langchain_core.messages import HumanMessage,AIMessage
from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
import os

load_dotenv()

class AgentAction(TypedDict):
    messages:List[Union[HumanMessage,AIMessage]]

llm=ChatGroq(model="deepseek-r1-distill-llama-70b")

def process(state:AgentAction)->AgentAction:
    """Creating  a Memory Agent"""
    res=llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=res.content))
    #print("Full chat history:",state["messages"])
    print("Bot:",res.content)
    return state

graph=StateGraph(AgentAction)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)
agent=graph.compile()
chat_history=[]
user_input=input("User: ")

while user_input.lower()!="exit":
    chat_history.append(HumanMessage(content=user_input))
    res=agent.invoke({"messages":chat_history})
    #print("Full chat history:",res["messages"])
    chat_history=res["messages"]
    user_input=input("User: ")


with open("history.txt","w",encoding="utf-8") as file:
    file.write("Conversation History \n")
    for message in chat_history:
        if isinstance(message,HumanMessage):
            file.write(f"User: {message.content}\n")
        if isinstance(message,AIMessage):
            file.write(f"Bot: {message.content}\n")
    file.write("End of Conversation")

print("Chat history saved to history.txt")