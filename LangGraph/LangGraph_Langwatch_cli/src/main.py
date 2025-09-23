"""Simple example showing basic LangGraph usage."""

import asyncio
from langchain_core.messages import HumanMessage
from agents.research_agent.research_agent import ResearchAgent
from dotenv import load_dotenv

async def main():
    """Simple example - just one agent doing research."""

    load_dotenv()

    # Create agent
    agent = ResearchAgent()

    # Test query
    query = "What is LangGraph?"
    message = HumanMessage(content=query)

    print(f"Query: {query}")
    print("Processing...")

    # Execute agent
    result = await agent.execute([message])

    print(f"Result: {result.content}")


if __name__ == "__main__":
    asyncio.run(main())