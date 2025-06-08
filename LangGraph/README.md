## LangGraph

List of Content
1. [LangGraph Patterns and their difference. ReACT, Reflection, Multi-Agent, Decision Tree, Plan-Execute](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/LangGraph/LangGraph-Patterns.md)
2. System Prompt Examples  
   a. [Decision Tree System Prompt](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/LangGraph/Prompt-Decision-Tree.md)    
   b. [Multi-Agent System Prompt](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/LangGraph/Prompt-Multi-Agent.md)  
   c. [Plan-Execute](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/LangGraph/Prompt-Plan-Execute.md)  
   d. [ReACT](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/LangGraph/Prompt-ReACT.md)  
   e. [Reflection](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/LangGraph/Prompt-Reflection.md)    
3. [ReACT Implementation Recommendations are here](https://til.simonwillison.net/llms/python-react-pattern)

## LangChain vs LangGraph

## LangGraph Patterns
![image](https://github.com/user-attachments/assets/336652b8-71ad-441b-a530-a333fd60a1cd)


### LangGraph usage
```python
from langgraph.graph import StateGraph

builder = StateGraph(StateType)
builder.add_node("react_node", react_function)
builder.add_edge("react_node", decision_node)
builder.set_entry_point("react_node")
graph = builder.compile()
```

### Simple usecase without LangGraph framework
![image](https://github.com/user-attachments/assets/75c79161-8868-4938-ac06-d4b2bf8267c9)

