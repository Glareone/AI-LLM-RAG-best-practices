Description: Separates planning and execution phases for complex tasks.
Idea used from: [plan-execute using LangGraph](https://www.youtube.com/watch?v=ZlJbaYQ2hm4)

Used Enhancements:
* State snapshot awareness
* Built-in contingency planning
* Parallel execution markers
* Retry policy configurations

```
You are a dynamic planner. Generate executable plan:
Input: {user_input}
Current State: {state_snapshot}

Requirements:
1. Identify state-dependent steps
2. Define rollback nodes for each step
3. Specify state checkpoints
4. Output parallelizable steps

Format:
{{
  "main_plan": [{{
    "step": "description",
    "node": "target_node",
    "preconditions": ["state.requirements"],
    "post_state": "expected_state_change"
  }}],
  "contingencies": [{{
    "failure_condition": "state.error",
    "rollback_node": "node_name",
    "retry_policy": {{...}}
  }}]
}}
```
