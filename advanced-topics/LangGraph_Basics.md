### Table of Content

#### LangGraph Basics
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

LangGraph Advanced Topics (State Management, Graph Architecture, Conditional Routing, Human-in-the-loop, Parallel Processing) Could be found [here](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/advanced-topics/LangGraph_Advanced.md)
