import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv

from langchain_core.messages import AnyMessage, HumanMessage
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from tools import guest_info_tool, search_tool, weather_info_tool, hub_stats_tool

load_dotenv()

# 1. Initialize Model Endpoint with Tool Calling Capabilities
HUGGINGFACEHUB_API_TOKEN = os.getenv("HF_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    task="text-generation"
)

chat = ChatHuggingFace(llm=llm, verbose=False)

# 2. Bind Tools to Chat Model
tools = [guest_info_tool, search_tool, weather_info_tool, hub_stats_tool]
chat_with_tools = chat.bind_tools(tools)

# 3. Define Agent State Schema and Assistant Node
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def assistant(state: AgentState):
    return {"messages": [chat_with_tools.invoke(state["messages"])]}

# 4. Construct LangGraph Workflow
builder = StateGraph(AgentState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

alfred = builder.compile()

# 5. Interactive Gala Assistant Loop
if __name__ == "__main__":
    print("🎩 Alfred is at your service! Type 'exit' or 'quit' to end the conversation.\n")
    
    # Stores full conversation history for multi-turn state memory
    conversation_history = []
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["quit", "exit"]:
            print("\n🎩 Alfred: Good evening, sir. Enjoy the gala!")
            break
            
        if not user_input:
            continue
            
        # Append user query to state history
        conversation_history.append(HumanMessage(content=user_input))
        
        print("\n🎩 Alfred is thinking...")
        
        # Invoke agent passing running state
        result = alfred.invoke({"messages": conversation_history})
        
        # Update running history with tool observations and final AI response
        conversation_history = result["messages"]
        
        print(f"\n🎩 Alfred: {conversation_history[-1].content}\n")