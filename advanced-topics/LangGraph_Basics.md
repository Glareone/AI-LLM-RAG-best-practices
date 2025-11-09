#### LangGraph Basics. Table of Content
0️⃣ When to Use What (Decision Framework)  
   - Direct OpenAI/Bedrock calls: Simple, one-shot completions  
   - LangChain: Linear chains, simple sequential workflows  
   - LangGraph: Cyclic workflows, stateful multi-step reasoning, conditional branching, agent loops

1️⃣ Core LangGraph Primitives  
   - StateGraph vs MessageGraph - which to use when  
   - Compilation model (graph.compile() and what happens)  
   - Checkpointers - MemorySaver, SqliteSaver, PostgresSaver (foundation for persistence)  
   - Thread/Run concepts - how conversations map to executions

2️⃣ Graph Execution Model  
   - How LangGraph actually runs (iterative execution, not just DAG)  
   - The START and END special nodes  
   - How edges vs conditional edges differ fundamentally  
   - Cycles and loop detection/limits  

3️⃣ Subgraphs & Composition  
   - When to use subgraphs vs separate graphs  
   - Communication patterns between graphs  
   - State sharing/isolation  

4️⃣ Error Handling & Interrupts (Critical for production)  
   - Interrupt before/after nodes  
   - Error propagation and recovery  
   - Retry strategies  

[LangGraph Advanced Topics (State Management, Graph Architecture, Conditional Routing, Human-in-the-loop, Parallel Processing) could be found here](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/advanced-topics/LangGraph_Advanced.md)  

---
### 0️⃣ When to Use What (Decision Framework)  

| Approach | Use When | Don't Use When | Example | 
| -------- | -------- | -------------- | ------- |
| Use CaseDirect API Calls within RAG Application | Single completion, no complex context needed, performance critical | Need complex conversation history or context, multi-step reasoning, or orchestration | Text classification, one-shot translation, simple Q&A | 
| LangChain, Semantic Kernel | Linear workflow (A→B→C), simple chains, basic RAG | Need loops, conditional branching, or complex state | Document summarization pipeline, basic RAG chatbot |
| LangGraph | Cycles/loops needed, conditional routing, multi-agent, human-in-loop | Simple linear flow, minimal state | Research agent, code review bot, multi-step planning | 

💡 Decision Flowchart Logic:
```python
Does your task require loops or cycles? 
├─ YES → LangGraph
└─ NO → Does it need multi-step orchestration?
    ├─ YES → Does it need conditional branching?
    │   ├─ YES → LangGraph
    │   └─ NO → LangChain (if simple) or LangGraph (if complex state)
    └─ NO → Direct API call
```

💡 Key Differentiators
LangGraph becomes necessary when you need:  
   1. Agent loops - "try, evaluate, retry" patterns  
   2. Dynamic routing - flow changes based on LLM output or conditions  
   3. Persistent state - maintain context across multiple invocations  
   4. Human checkpoints - pause for approval before continuing
   5. Parallel branches - concurrent execution with state merging  

---
### 1️⃣ Core LangGraph Primitives

🛠️ StateGraph vs MessageGraph
When to use StateGraph:
  - Need custom fields beyond messages (metadata, scores, counters)  
  - Multi-agent systems with separate concerns  
  - Complex routing logic based on state  

🛠️ When to use MessageGraph:  
  - Simple conversational agents  
  - Don't need additional state tracking  
  - Quick prototypes  

| Feature | StateGraph | MessageGraph | 
| ------- | ---------- | ------------ |
| 📊 State Type | Custom schema (Pydantic, TypedDict, dataclass) | List of messages only | 
| 🛝Flexibility | Full control over state structure | Fixed message list structure |
| Use Case | Multi-agent, complex workflows, custom data | Simple chatbots, conversation flow | 
| State Access | state["custom_field"] | state["messages"] | 
| 📗 Learning Curve | Higher (must define schema) | Lower (built-in structure) |  

#### ➡️ StateGraph declaration. Recommendation: Use TypedDict for simplicity, Pydantic when you need validation. DataClass is not recommended.
```python
# Option 1: TypedDict (simple, no validation)
from typing import TypedDict, Annotated
from operator import add

class AgentState(TypedDict):
    messages: Annotated[list, add]  # Reducer: append messages
    current_step: str
    retry_count: int
```
```python
# Option 2: Pydantic (validation, IDE support)
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    messages: list = Field(default_factory=list)
    current_step: str = "start"
    retry_count: int = Field(default=0, ge=0, le=3)
```
```python
# Option 3: Dataclass (Python standard library)
from dataclasses import dataclass, field

@dataclass
class AgentState:
    messages: list = field(default_factory=list)
    current_step: str = "start"
    retry_count: int = 0
```

🛠️ StateGraph Reducer. State Update Strategies
```python
from operator import add
from typing import Annotated

class State(TypedDict):
    # Append to list (default for messages)
    messages: Annotated[list, add]
    
    # Replace value (default behavior if no annotation)
    current_tool: str
    
    # Custom reducer
    scores: Annotated[list[float], lambda x, y: x + [max(y)]]
```

#### ➡️ MessageGraph. Example. Reducer  

Minimal example of MessageGraph:    
```python
from langgraph.graph import MessageGraph, END

# 1. DECLARE the messageGraph
graph = MessageGraph()

# 2. UPDATE STATE in nodes
def my_agent(messages: list):
    # messages = current state
    response = llm.invoke(messages)
    return [response]  # Return list to APPEND to messages

graph.add_node("agent", my_agent)
graph.set_entry_point("agent")
graph.add_edge("agent", END)

app = graph.compile(checkpointer=MemorySaver())

# 3. FETCH STATE
config = {"configurable": {"thread_id": "123"}}

# Invoke (updates state)
result = app.invoke([HumanMessage("Hello")], config)
# result = full message list: [HumanMessage("Hello"), AIMessage("Hi!")]

# Get state later
state = app.get_state(config)
print(state.values)  # {'messages': [HumanMessage(...), AIMessage(...)]}
```

❗️ Reducer in MessageGraph:  
   1. MessageGraph has a built-in reducer for messages (automatically appends). Cannot be customized or add other reducers.  
   2. MessageGraph does use the fixed schema: {"messages": [...]}.  
   3. If you need to customize the reducer - you need to switch to StateGraph  


##### ➡️ Compilation model
Pretty simple, consist of two steps, Build and Compile.  
❗️ Important: Graph is immutable after compilation. Can't add nodes/edges post-compile.  
What happens during Compile `compile():`:  
1. Validates all edges point to existing nodes
2. Checks for unreachable nodes
3. Ensures START and END are properly connected
4. Attaches checkpointer for persistence
5. Creates runnable execution engine
```
# Build graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_edge(START, "agent")
graph.add_edge("agent", END)

# Compile (this is when LangGraph validates structure)
app = graph.compile(checkpointer=MemorySaver())
```

##### ➡️ Checkpointers - MemorySaver, SqliteSaver, PostgresSaver (foundation for persistence)  

| Checkpointer | Persistence | Use Case | Setup Complexity | 
| ------------ | ----------- | -------- | ---------------- |
| MemorySaver | In-memory only | Development, testing, and cases when rerun cost is low | Low (no setup) |
| SqliteSaver | Local file | Single-machine production, demos | Low (one file path) | 
| PostgresSaver | Database | Multi-instance production | Medium (DB setup) | 
| Custom | Your choice | Special requirements (Redis, S3) | High (implement interface) |

Checkpoint contains:
   1. Full state at each step.
   2. Metadata
   3. Parent checkpoint ID (for time-travel).

Implementation:  
```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver

# Development
app = graph.compile(checkpointer=MemorySaver())

# Production (local)
app = graph.compile(checkpointer=SqliteSaver.from_conn_string("checkpoints.db"))

# Production (distributed)
app = graph.compile(
    checkpointer=PostgresSaver.from_conn_string("postgresql://...")
)
```

#### ➡️ Thread/Run Concepts.
💡 Ability to run your LangGraph application in different threads:  
💡 Key concept: Thread ID determines which checkpoint chain to use. Same thread = shared history.  
```python
# Step 1: Build graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)  # Your code
graph.add_edge(START, "agent")
graph.add_edge("agent", END)

# Step 2: Compile = create runnable app
app = graph.compile()

# Step 3. Thread = Conversation/Session ID
# Run = Single execution within a thread

config = {
    "configurable": {
        "thread_id": "user-123-conversation-1"  # Unique per conversation
    }
}

# First invocation (creates thread)
response1 = app.invoke({"messages": [("user", "Hello")]}, config)

# Second invocation (continues the same thread)
response2 = app.invoke({"messages": [("user", "Follow-up")]}, config)

# Different thread (separate conversation)
config2 = {"configurable": {"thread_id": "user-123-conversation-2"}}
response3 = app.invoke({"messages": [("user", "New topic")]}, config2)
```

What's happening behind `invoke`?  
   1. Loads checkpoint (if thread_id provided)  
   2. Runs your nodes in order (following edges)  
   3. Inside your nodes → you call OpenAI/Bedrock  
   4. Saves checkpoint after execution  
   5. Returns final state  

---
