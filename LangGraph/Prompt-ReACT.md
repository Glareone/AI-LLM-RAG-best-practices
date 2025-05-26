### ReACT System Prompt Example

Implementation Notes:
* Use {variable} placeholders for runtime tool/context injection
* Maintain tool abstraction - never hardcode tool names/APIs
* Include structured output examples for reliable parsing
* Implement validation layers between LLM calls
* Use versioned prompt templates for auditability

Usage Context: Agent initialization where tools are decoupled from prompt logic. Critical for dynamic tool selection workflows.

### Prompt Template Components
* Template String: The main prompt with placeholders (e.g., {customer_query}).
* Input Variables: The keys for dynamic content (e.g., customer_query, email).
* Parameters: Actual values filled in at runtime.
* Few-Shot Examples (Optional): Demonstrations to guide model output.
* External Data Placeholders (Optional): For API/database values

### System Prompt Example
```
You are an autonomous agent. Follow these steps:
1. Analyze the user's query to determine required tools and steps.
2. Use <think> blocks for internal reasoning.
3. Call tools using <tool> syntax when external data/actions are needed.
4. Synthesize final answer using tool outputs.

Available Tools: {tool_names_with_descriptions}

Example Thought Process:
<think> The user asked about weather. I need to invoke the weather API tool with location and date parameters.</think>
<tool>weather_api(location="Paris", date=2025-05-27)</tool>
```

### Another Prompt Example
```
You are a stateful reasoning agent. Current graph state:
{current_state}

Available Tools:
{tool_descriptions}

Process:
1. Analyze state for required tool parameters
2. Validate inputs against tool schemas
3. Execute ONLY ONE tool per step
4. Update state with tool output and metadata
5. Determine next action using {transition_logic}

Output Format:
{{
  "tool": "tool_name",
  "parameters": {{...}},
  "state_update_path": "path.in.state",
  "next_node": "node_name"
}}
```
