import os

from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model

from langchain_tavily import TavilySearch
from langchain_core.tools import tool
import asyncio
from datetime import datetime
from os import getenv

## Define the Tavily search tool
tavily_search_tool = TavilySearch(
    max_results=5,
    timeout=10,
    search_depth="basic",
    tavily_api_key=os.getenv('TAVILY_API_KEY')
)

# Wrap the Tavily search tool in a tool decorator and make it asynchronous
@tool
async def search(query: str):
    """
    Search for general web results using Tavily.
    """
    return await asyncio.to_thread(tavily_search_tool.invoke, {"query": query})

# Store our search in the tools list
tools = [search]

today: str = datetime.now().strftime("%Y-%m-%d")

# Create our System prompt
system_prompt: str = f"""
You are a helpful assistant that can search the web for information using the search tool Tavily.
Return the latest news about Israel and Iran conflict if I ask you about global news.
For news return title, original URL, ans summary of the article.

today date is {today}
"""

# define our model
model = init_chat_model(model_provider="anthropic", model="claude-3-7-sonnet-latest")
graph = create_react_agent(model=model, tools=tools, prompt=system_prompt)
