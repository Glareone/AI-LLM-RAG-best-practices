# Claude Code Instructions for LangGraph + LangWatch Project

## Project Overview
This project investigates LangGraph capabilities for building AI agent applications with LangWatch CLI monitoring. Focus on best practices for multi-agent workflows and behavior tracking.

## Development Environment
- **Python Version**: 3.12
- **Package Manager**: UV (preferred) and PIP support
- **Virtual Environment**: `.venv` (already configured in PyCharm)
- **Project Structure**: `src/` based package layout

## Key Dependencies (to be added incrementally)
- `langgraph`: Core multi-agent workflow framework
- `langwatch`: Local monitoring and tracking
- `langchain-core`: Base LangChain components
- `langchain-openai`: OpenAI integration (if needed)

## Testing & Quality Commands
- **Install dependencies**: `uv pip install -e .`
- **Install dev dependencies**: `uv pip install -e .[dev]`
- **Run tests**: `pytest`
- **Code formatting & linting**: `ruff format src/ tests/`
- **Linting & import sorting**: `ruff check src/ tests/`
- **Fix auto-fixable issues**: `ruff check --fix src/ tests/`
- **Type checking**: `mypy src/`



## Project Structure Guidelines
```
src/
├── langgraph_langwatch_cli/
│   ├── __init__.py
│   ├── agents/          # Individual agent implementations
│   ├── workflows/       # LangGraph workflow definitions  
│   ├── monitoring/      # LangWatch integration
│   └── examples/        # Sample use cases
tests/
├── test_agents/
├── test_workflows/
└── test_monitoring/
```

## Development Priorities
1. **Agent Architecture**: Design modular, reusable agents
2. **Workflow Patterns**: Implement common multi-agent patterns
3. **Monitoring Integration**: Seamless LangWatch tracking
4. **Error Handling**: Robust error management and recovery
5. **Documentation**: Clear examples and usage patterns

## Best Practices
- Follow Python type hints throughout
- Implement comprehensive error handling
- Create modular, testable components
- Document all public interfaces
- Use dependency injection for testability
- Implement proper logging and monitoring

## Claude Code Behavior
- Always run quality checks after significant changes
- Create tests alongside implementation
- Follow the established project structure
- Use UV for package management when possible
- Maintain focus on LangGraph + LangWatch integration goals