### Core Patterns for LangGraph
1. [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
2. [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651)
3. [Alpha-Codium](https://arxiv.org/abs/2401.08500)

---------------
### Modern Patterns to work with LangGraph
---------------

1. Flow - How nodes connect and loop
2. System Prompt - System Prompt example for each Pattern
3. State Structure - What data you track and how
4. Logic (Decision Logic) - When to continue/stop/branch
5. Context Management - What information each node sees
6. Error Recovery - How failures are handled

### 1. ReACT Pattern (Reasoning & Acting)

**ReACT Flow**:   
```
# ReACT has a LOOP with conditional exit
reasoning → action → should_continue_check
    ↓           ↑
   END ←── reasoning (if continue)
```

**ReACT System Prompt**:  
```
You are an agent that reasons step by step and takes actions.
Format your thoughts as:
Thought: [your reasoning]
Action: [tool to use]
Observation: [result]
```

**ReACT State**:   
```python
state = {
    "observations": [],  # Grows with each action
    "reasoning_history": [],
    "current_thought": str
}
```

**ReACT Logic**:  
```python
def should_continue(state):
    if goal_achieved(state.observations):
        return "end"
    if max_iterations_reached(state):
        return "end"
    return "continue_reasoning"
```

**ReACT Context Handling**:  
```python
# Only keeps recent reasoning + observations
context = last_3_reasoning_steps + last_3_observations
```

**ReACT Error Handling Strategy: Retry with additional reasoning**:  
```python
def handle_error(state, error):
    state.observations.append(f"Error: {error}")
    return "reasoning"  # Go back to reasoning with error info
```

* Classic loop: Think → Act → Observe → Think again  
* Great for exploratory tasks where you don't know the path ahead  
* Each iteration builds on previous observations  
* Best for: Research, problem-solving, debugging  

---------------
### 2. Plan-and-Execute Pattern

**Plan-Execute Flow**:  
```
# Plan-Execute is LINEAR
planning → execute_step → execute_step → ... → END
```

**Plan-Execute System Prompt**:  
```
You are a planning agent. First create a detailed plan, then execute each step.
Plan Format:
1. Step 1. Collect Knowledge
2. Step 2. Get The Data From Source
3. Step 3. Execute Step 3, Bring results to the Step 4.
4. Step 4. ...
```

**Plan-Execute State**:  
```python
state = {
    "original_plan": [],  # Static
    "remaining_steps": [],  # Shrinks
    "completed_steps": []  # Grows
}
```

**Plan-Execute Logic**:
```python
def should_continue(state):
    if len(state.remaining_steps) > 0:
        return "execute_next"
    return "end"
```

**Plan-Execute Context Handling**:
```python
# Always has access to complete plan
context = original_plan + progress_status + current_step
```

**Plan-Execute Error Handling Strategy: Replan or skip step**:  
```python
def handle_error(state, error):
    # Either replan or mark step as failed and continue
    state.failed_steps.append(current_step)
    return "execute_next" or "replan"
```

* Plan the entire approach upfront, then execute systematically
* More predictable and traceable than ReACT
* Good for complex, multi-step tasks with clear requirements
* Best for: Data processing pipelines, report generation, structured workflows

---------------
### 3. Reflection Pattern

**Reflection Flow**:  
```
# Reflection has NESTED loops for improvement
initial → reflection → improve → should_improve_check
                         ↑           ↓
                       END ←── reflection (if improve)
```

**Reflection System Prompt**:  
```
You are a self-improving agent. First respond, then critique your response and improve it.
Critique: [what could be better]
Improvement: [better version]
```

**Reflection State**:
```python
state = {
    "original_response": str,
    "critiques": [],
    "improved_versions": [],
    "iteration_count": int
}
```

**Reflection Logic**:
```python
def should_continue(state):
    if quality_score(state.latest_version) > threshold:
        return "end"
    if state.iteration_count >= max_iterations:
        return "end"
    return "reflect_more"
```

**Reflection Context Handling**:
```python
# Compares versions for improvement
context = original + all_critiques + current_version
```

**Reflection Error Handling Strategy: Incorporate error into critique**:  
```python
def handle_error(state, error):
    state.critiques.append(f"Error encountered: {error}")
    return "improve"  # Use error as improvement feedback
```

* Generate initial response, then iteratively improve through self-critique  
* Powerful for quality improvement and error correction  
* Can combine with other patterns (ReACT + Reflection)  
* Best for: Content creation, code review, quality assurance  

-----------------
### 4. Multi-Agent Collaboration

**Multi-Agent Flow**:
```
# Multi-Agent has PARALLEL or SEQUENTIAL agent calls
agent1 → agent2 → agent3 → synthesizer → END
```

**Multi-Agent Prompt Recommendations**:
```
* Emphasize collaboration and communication
* Define roles within the team context
* Include coordination and handoff procedures
* Built-in quality control and iteration
```

**Multi-Agent System Prompt Example**: [Multi-Agent System Prompt](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/LangGraph/Prompt-Multi-Agent.md)

**Multi-Agent State Management**:  
```python
state = {
    "agent_results": {
        "researcher": None,
        "analyzer": None, 
        "writer": None
    },
    "current_agent": str,
    "inter_agent_messages": [],  # Communication between agents
    "shared_context": {},        # Global knowledge base
    "agent_status": {            # Track which agents are done
        "researcher": "pending",
        "analyzer": "waiting", 
        "writer": "waiting"
    }
}
```

**Multi-Agent Decision Logic: ""Which agent should run next?""**:
```python
def route_next_agent(state):
    # Check dependencies - analyzer needs researcher to finish
    if state.agent_status["researcher"] == "complete" and \
       state.agent_status["analyzer"] == "pending":
        return "analyzer"
    
    # Check if all prerequisite agents are done
    if all_prerequisites_complete(state):
        return "synthesizer"
    
    # Or run agents in parallel
    return get_next_available_agent(state)
```

**Multi-Agent Context Handling: Shared knowledge base**:  
```python
# Each agent gets:
# 1. Original user request
# 2. Results from prerequisite agents
# 3. Shared context updated by previous agents
context = {
    "user_request": original_query,
    "researcher_findings": state.agent_results["researcher"],
    "previous_analysis": state.agent_results["analyzer"],
    "shared_knowledge": state.shared_context
}
```

**Multi-Agent Error Handling Strategy: Agent substitution and retry**:  
```python
def handle_agent_error(state, failed_agent, error):
    if failed_agent == "researcher":
        # Try backup research method or different agent
        state.agent_status["backup_researcher"] = "active"
        return "backup_researcher"
    
    # Or skip non-critical agent
    state.agent_status[failed_agent] = "skipped"
    state.shared_context[f"{failed_agent}_error"] = str(error)
    return get_next_agent_in_sequence(state)
```


* Different agents with specialized roles work together  
* Each agent has specific expertise and responsibilities  
* Sequential or parallel execution depending on dependencies  
* Best for: Complex domains requiring different expertise areas  

----------------
### 5. Decision Tree Pattern

**Decision-Tree Flow**:
```
# Decision Tree BRANCHES based on input
classifier → math_handler → END
          → research_handler → END
          → communication_handler → END
```

**Decision Tree Recommendations**:
```
* Focus on domain expertise and specialization
* Emphasize independence and completeness
* Include fallback strategies for edge cases
* Clear input/output specifications
```

**Decision Tree System Prompt Example**: [Decision Tree System Prompt](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/LangGraph/Prompt-Decision-Tree.md)


**Decision Tree Logic: Which specialized handler should process this?**:  
```python
def route_decision(state):
    classification = state["input_classification"]
    confidence = state["confidence_scores"].get(classification, 0)
    
    # High confidence routing
    if confidence > 0.8:
        return classification  # "math", "research", "communication"
    
    # Low confidence - try general handler or ask for clarification
    if confidence < 0.3:
        return "clarification_handler"
    
    # Medium confidence - route but flag for review
    state["needs_review"] = True
    return classification
```

**Decision Tree Context Handling: Specialized Context per handler**:
```python
# Math Handler gets:
context = {
    "user_input": original_request,
    "extracted_numbers": parse_numbers(input),
    "math_operations": identify_operations(input),
    "calculation_history": []
}

# Research Handler gets:
context = {
    "user_input": original_request,
    "search_keywords": extract_keywords(input),
    "research_depth": determine_depth(input),
    "source_preferences": user_preferences
}

# Communication Handler gets:
context = {
    "user_input": original_request,
    "recipient_info": extract_recipients(input),
    "message_type": classify_message_type(input),
    "urgency_level": assess_urgency(input)
}
```

**Decision Tree Error Handling**:
```python
def handle_routing_error(state, error):
    # If classification fails, use keyword-based fallback
    if "classification_failed" in str(error):
        fallback_route = keyword_based_routing(state.user_input)
        state["routing_history"].append(f"fallback_to_{fallback_route}")
        return fallback_route
    
    # If specific handler fails, try general handler
    if "handler_failed" in str(error):
        state["handler_context"]["original_error"] = str(error)
        state["fallback_attempted"] = True
        return "general_handler"
    
    # Last resort - human handoff
    return "human_handoff"
```


* Route different inputs to specialized handlers  
* Clean separation of concerns  
* Easy to extend with new input types  
* Best for: Chatbots, command processing, workflow automation

-----------------
### Patterns Comparison
------------------

#### Comparison of State Complexity:

* ReACT: Simple accumulative state (observations growing)
* Plan-Execute: Linear state (plan shrinking, completed growing)
* Reflection: Versioned state (multiple versions tracked)
* Multi-Agent: Distributed state (multiple agent results + coordination)
* Decision Tree: Metadata-heavy state (classification info + routing context)

#### Error Recovery Strategies:
* ReACT: "Learn from error and continue reasoning"
* Plan-Execute: "Replan or skip failed step"
* Reflection: "Use error as feedback for improvement"
* Multi-Agent: "Replace failed agent or continue without it"
* Decision Tree: "Fall back to simpler routing or general handler"

Wrap up: The Multi-Agent pattern has the most complex state management because it needs to coordinate between multiple independent agents, while Decision Tree has the most sophisticated routing logic because it needs to handle classification uncertainty and handler failures gracefully.
