## LanGraph

List of Content
1. [LangGraph Patterns and their difference. ReACT, Reflection, Multi-Agent, Decision Tree, Plan-Execute](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/LangGraph/LangGraph-Patterns.md)
2. System Prompt Examples  
   a. [Decision Tree System Prompt](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/LangGraph/Prompt-Decision-Tree.md)  
   b. [Multi-Agent System Prompt](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/LangGraph/Prompt-Multi-Agent.md)  

## LangChain vs LangGraph

### LangGraph usage
```python
from langgraph.graph import StateGraph

builder = StateGraph(StateType)
builder.add_node("react_node", react_function)
builder.add_edge("react_node", decision_node)
builder.set_entry_point("react_node")
graph = builder.compile()
```
