# Claude Code Instructions for LangGraph + LangWatch Project

## Project Overview
This project investigates LangGraph capabilities for building AI agent applications with LangWatch CLI monitoring. Focus on best practices for multi-agent workflows and behavior tracking using a modular architecture.

## Development Environment
- **Python Version**: 3.12
- **Package Manager**: UV (preferred) and PIP support
- **Virtual Environment**: `.venv` (already configured in PyCharm)
- **Project Structure**: `src/` based package layout with separate monitoring module
- **Package Name**: `langgraph-langwatch-cli`

## Key Dependencies (installed)
- `langgraph>=0.2.0`: Core multi-agent workflow framework
- `langwatch>=0.1.0`: Local monitoring and tracking
- `langchain-core>=0.3.0`: Base LangChain components
- `langchain-openai>=0.2.0`: OpenAI integration
- `python-dotenv>=1.0.0`: Environment variable management
- `pydantic>=2.0.0`: Data validation and serialization

## Testing & Quality Commands
- **Install dependencies**: `uv pip install -e .`
- **Install dev dependencies**: `uv pip install -e .[dev]`
- **Run tests**: `pytest`
- **Code formatting & linting**: `ruff format src/ tests/ monitoring/`
- **Linting & import sorting**: `ruff check src/ tests/ monitoring/`
- **Fix auto-fixable issues**: `ruff check --fix src/ tests/ monitoring/`
- **Type checking**: `mypy src/`

## Project Structure Guidelines
```
src/
├── __init__.py
├── agents/                    # Individual agent implementations
├── workflows/                 # LangGraph workflow definitions
├── examples/                  # Sample use cases and demos
├── main.py                   # Main application entry point
└── orchestrator.py           # Central workflow orchestration
monitoring/                   # Separate LangWatch integration module
├── __init__.py
└── langwatch_tracker.py     # LangWatch monitoring implementation
tests/
├── test_agents/             # Agent-specific tests
├── test_workflows/          # Workflow pattern tests
└── test_monitoring/         # Monitoring integration tests
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

## Implementation Guidelines

### Architecture Patterns
- **Modular Design**: Separate concerns between agents, workflows, and monitoring
- **Dependency Injection**: Use constructor injection for testability
- **Configuration Management**: Use `.env` files and environment variables
- **Error Recovery**: Implement graceful degradation and retry mechanisms

### LangGraph Integration
- Utilize StateGraph for complex multi-agent workflows
- Implement proper state management between agent interactions
- Design reusable workflow patterns and templates
- Focus on conditional branching and parallel execution

### LangWatch Monitoring
- Separate monitoring module in `monitoring/` directory
- Track agent performance, errors, and execution metrics
- Implement structured logging for debugging and analysis
- Monitor workflow state transitions and decision points

### Environment Configuration
- Use `.env.example` as template for required environment variables
- Store API keys and sensitive configuration separately
- Support both development and production configurations

## Claude Code Behavior
- Always run quality checks after significant changes: `ruff format`, `ruff check`, `mypy`
- Create tests alongside implementation in appropriate test directories
- Follow the established project structure with `src/` and separate `monitoring/`
- Use UV for package management when possible
- Include `monitoring/` directory in formatting and linting commands
- Maintain focus on LangGraph + LangWatch integration goals
- Test both unit functionality and integration between components