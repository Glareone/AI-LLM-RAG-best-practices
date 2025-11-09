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
#### 0️⃣ When to Use What (Decision Framework)  

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

➡️ Agent loops - "try, evaluate, retry" patterns  
➡️ Dynamic routing - flow changes based on LLM output or conditions  
➡️ Persistent state - maintain context across multiple invocations  
➡️Human checkpoints - pause for approval before continuing  
➡️ Parallel branches - concurrent execution with state merging  
