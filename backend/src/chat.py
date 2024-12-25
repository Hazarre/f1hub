import os
from typing import TypedDict, List
from typing_extensions import Annotated
from dotenv import load_dotenv

from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langgraph.graph import START, StateGraph

# Type def
class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

# Initialization 
load_dotenv() 
db = SQLDatabase.from_uri("sqlite:///perm.db")
llm = ChatOpenAI(model="gpt-4o-mini")
query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
# Config 

# Helpers 
def get_db_dialect() -> str:
	return db.dialect

def get_table_names() -> str: 
	return db.get_usable_table_names()

def run_sql(sql_query:str )-> str:
	result = db.run(sql_query)
	print(type(result))
	return result

# MAIN FUNCS
# 1) converts the question into a SQL query;
# 2) executes the query;
# 3) uses the result to answer the original question.

# FUNC 1) converts the question into a SQL query;
class QueryOutput(TypedDict):
    """Generated SQL query."""
    query: Annotated[str, ..., "Syntactically valid SQL query."]

def write_query(state):
    """Generate SQL query to fetch information."""
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}

# FUNC 2) executes the query;
def execute_query(state):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDataBaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}

# FUNC 3): uses the result to answer the original question.
def generate_answer(state: State):
    """Answer question using retrieved information as context."""
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}

# BUILD 
graph_builder = StateGraph(State).add_sequence(
	[write_query, execute_query, generate_answer])
graph_builder.add_edge(START, "write_query")
graph = graph_builder.compile()
         
def ask(question): 
    state: State = {"question": question}    
    ans = {}
    for step in graph.stream(state, stream_mode="updates"):
        ans = ans | step
    return ans

# ask("What are the total unique cases?") 