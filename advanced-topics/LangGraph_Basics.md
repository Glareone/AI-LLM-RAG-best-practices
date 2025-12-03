#### LangGraph Basics. Table of Content
0️⃣ [When to Use What (Decision Framework)](#0%EF%B8%8F⃣-when-to-use-what-decision-framework)  
   - Direct OpenAI/Bedrock calls: Simple, one-shot completions  
   - LangChain: Linear chains, simple sequential workflows  
   - LangGraph: Cyclic workflows, stateful multi-step reasoning, conditional branching, agent loops

1️⃣ [Core LangGraph Primitives](#1%EF%B8%8F⃣-core-langgraph-primitives)  
   - StateGraph vs MessageGraph - which to use when  
   - Compilation model (graph.compile() and what happens)  
   - Checkpointers - MemorySaver, SqliteSaver, PostgresSaver (foundation for persistence)  
   - Thread/Run concepts - how conversations map to executions

2️⃣ [Graph Execution Model](#2%EF%B8%8F⃣-graph-execution-model-start--end-nodes-conditional-nodes)  
   - How LangGraph actually runs (iterative execution, not just DAG)  
   - The START and END special nodes
   - Parallel node Execution
   - How edges vs conditional edges differ fundamentally  
   - Cycles and loop detection/limits
   - Prevent infinite Loops. Attempt, Counter in State, Check Quality result, Token Budget

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
### 2️⃣ Graph Execution Model. START & END Nodes. Conditional Nodes.
How LangGraph Actually Runs  
Key concept: LangGraph executes step-by-step, not all at once.  
```python
# Each step = one node execution
Step 1: START → agent
Step 2: agent → tools
Step 3: tools → agent
Step 4: agent → END
```
Not a traditional DAG:
   1. DAGs = no cycles, run once
   2. LangGraph = allows cycles, runs iteratively until reaching `END`

Execution Flow Example with START and END special nodes.
```python
from langgraph.graph import START, END

graph = StateGraph(State)
graph.add_node("research", research_node)
graph.add_node("validate", validate_node)

graph.add_edge(START, "research") # START NODE. Specify where to begin
graph.add_edge("research", "validate")
graph.add_conditional_edges("validate", should_continue, {
    "retry": "research",  # ← Cycle!
    "done": END
}) # END NODE. Specified where to stop

app = graph.compile()
```

#### START & END Key rules:
| Rule | Explanation |
| ---- | ----------- |
| START is implicit | Every graph starts here, you don't create it | 
| Must connect START | At least one edge from START or use set_entry_point() | 
| END stops execution | Once any node reaches END, graph stops | 
| Multiple paths to END | Different nodes can route to END |

The common mistake is not connect start to the next agent or not to have the End connected.  
Example:  
```python
# Common mistake:
# ❌ Forgot to connect START
graph.add_node("agent", agent_node)
graph.add_edge("agent", END)
# Missing: graph.add_edge(START, "agent")

# ✅ Correct
graph.add_edge(START, "agent")
```
graph.add_edge("agent", END)

#### Parallel node execution
```python
# If multiple edges from same node (advanced topic)
graph.add_edge("start", "node_a")
graph.add_edge("start", "node_b")
# Both node_a and node_b run in parallel (covered in section 5)
```

#### Edges vs Conditional Edges
| Feature | Regular Edge | Conditional Edge |  
| ------- | ------------ | ---------------- |
| When to use | Always go to same next node | Route based on logic | 
| Syntax | add_edge("A", "B") | add_conditional_edges("A", router_fn, mapping) |
| Deterministic | Yes | No (depends on state/logic) |
| Example | Always validate after research | Go to tools OR end based on LLM response |

💡Conditional Edge Nuances:
   1. Router function signature:
```python
# Gets full state only
def router(state: State) -> str:
    return "next_node_name"

# Or get both state and config
def router(state: State, config: RunnableConfig) -> str:
    thread_id = config["configurable"]["thread_id"]
    return "next_node_name"
```
   2. Agent wants to use tool and you declare the tool right in the graph:
```python
def route_after_agent(state: State) -> str:
    last_message = state["messages"][-1]
    
    # Check if LLM wants to use tools
    if last_message.tool_calls:
        return "tools"
    return "end"

graph.add_conditional_edges("agent", route_after_agent, {
    "tools": "tools",
    "end": END
})
```

#### Recursion limit and graph max
By default the recursion_limit is set to 25 `recursion_limit=25`, you can execute up to 25 nodes before you get an error.  
But you also can set your own `custom` number of steps, it's useful if you check the response quality.  

```python
# Default: 25 iterations max
# Each node execution = 1 iteration
# If you hit limit → raises GraphRecursionError
app = graph.compile()

# Custom limit
app = graph.compile(recursion_limit=100)

START → agent → tools → agent → tools → agent → END
        [1]     [2]     [3]     [4]     [5]

```

| Step | Node | Iteration Count | 
| ---- | ---- | --------------- |
| 1 | agent | 1 | 
| 2 | tools | 2 |
| 3 | agent | 3 |
| 4 | tools | 4 |
| 5 | agent | 5 | 
| - | END | - |

#### How to prevent infinite loops
💡 Pattern 1: Counter in state  
```python
class State(TypedDict):
    messages: Annotated[list, add]
    loop_count: int

def router(state: State):
    if state["loop_count"] >= 5:
        return "end"
    return "continue"
```

💡 Pattern 2: Check result quality  
```python
def router(state: State):
    if state["validation_passed"]:
        return "end"
    if state["attempts"] >= 3:
        return "end"  # Give up after 3 tries
    return "retry"
```
💡 Pattern 3: Token budget  
```python
def router(state: State):
    total_tokens = sum(len(m.content) for m in state["messages"])
    if total_tokens > 10000:
        return "end"  # Stop if conversation too long
    return "continue"
```

---

### 3️⃣ Subgraphs & Composition  
