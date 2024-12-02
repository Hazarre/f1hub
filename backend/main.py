from langchain_community.utilities import SQLDatabase
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
# print(db.dialect)
# print(db.get_usable_table_names())
# db.run("SELECT * FROM Artist LIMIT 10;")


# converts the question into a SQL query;
# executes the query;
# uses the result to answer the original question.

from typing import TypedDict
# import getpass
# import os
# os.environ["OPENAI_API_KEY"] = getpass.getpass()


from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")


from langchain import hub
query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
# assert len(query_prompt_template.messages) == 1
# query_prompt_template.messages[0].pretty_print()


from typing_extensions import Annotated


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


# print(write_query({"question": "How many Employees are there?"}))


from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool


def execute_query(state):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDataBaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}


print(execute_query({"query": "SELECT COUNT(EmployeeId) AS EmployeeCount FROM Employee;"}))