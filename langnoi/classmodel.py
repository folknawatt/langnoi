from typing_extensions import TypedDict, Annotated
from pydantic import BaseModel, Field


class State(TypedDict):
    question: str
    query: str


class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")


class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]
