## Evaluating Agentic Applications
### Table of Content
* [General Agentic Application Evaluations](#general-agentic-applications-evaluations)
* [Monitoring](#monitoring)
* [Trajectory Evaluation](#trajectory-evaluation)
* Structure of the Evaluation
* Application Improvements using G-Eval (LLM-as-a-Judge)

---

### General Agentic Applications Evaluations.
Agentic apps differ from standard LLM applications because they involve multi-step reasoning, tool use, and autonomous decision-making.    
Evaluation must capture:   
1️⃣ Task Success: Did the agent complete the goal?  
2️⃣ Efficiency: How many steps did it take?  
3️⃣ Tool Usage: Were the right tools called with correct parameters?  
4️⃣ Reasoning Quality: Was the decision-making sound?  

Key Metrics for AgentsBasic Metrics:  
1️⃣ Precision: Of all actions taken, how many were correct?  
2️⃣ Recall: Of all required actions, how many did the agent perform?  
3️⃣ F1 Score: Harmonic mean of precision and recall.  
4️⃣ Success Rate: % of tasks completed successfully.  
5️⃣ Average Steps to Completion: Efficiency measure.  

Agent-Specific Metrics:  
1️⃣ Tool Call Accuracy: Correct tool selection and parameters.
2️⃣ Trajectory Coherence: Logical flow of decisions.  
3️⃣ Recovery Rate: Ability to recover from errors.  
4️⃣ Hallucination Rate: Incorrect tool calls or non-existent actions. 

--- 
### Monitoring
Real-time observation of agent behavior in production. What to Monitor.
Agent-Specific Evaluations:  
1️⃣ Tool call sequences and patterns.  
2️⃣ Reasoning steps and intermediate outputs.  
3️⃣ Error rates per tool.  
4️⃣ Infinite loop detection (agent gets stuck).  
5️⃣ Token usage per trajectory.  
6️⃣ Latency per step vs. end-to-end.  

---

### Trajectory Evaluation
Evaluating the complete sequence of agent actions from start to finish, not just the final output. What It Is.  
A trajectory is the full path an agent takes: observations → reasoning → actions → results.  

Trajectory Evaluations:  
1️⃣ Path Optimality: Did it take unnecessary detours?  
2️⃣ Tool Selection: Right tools at right times?  
3️⃣ Context Preservation: Did it remember important info?  
4️⃣ Error Handling: How did it respond to failed tool calls?  
