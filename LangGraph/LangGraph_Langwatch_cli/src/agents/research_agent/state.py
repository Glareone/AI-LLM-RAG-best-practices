from typing import Annotated

from pydantic import BaseModel
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

from models.relevant_data import RelevantData


class State(BaseModel):
    messages: Annotated[list[AnyMessage], add_messages] = []
    relevant_data: RelevantData