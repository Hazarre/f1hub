from typing import Union
from fastapi import FastAPI

from src.chat import run_sql, write_query, State, ask
from sqlmodel import Field, SQLModel, Session, create_engine, select


# Database setup
DATABASE_URL = "sqlite:///./PERM_data/perm_shared.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create the database
SQLModel.metadata.create_all(engine)

# Dependency to get the database session
def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "You've connected to the api" }

@app.get("/items", response_model=list[Item])
def read_items(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0), session: Session = Depends(get_session)):
    """
    Endpoint to fetch items with pagination.

    Parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Maximum number of records to fetch (default: 10)
    """
    statement = select(Item).offset(skip).limit(limit)
    results = session.exec(statement).all()
    return results 

@app.get("/run_sql/")
def run():
    return run_sql("SELECT * FROM y2023 LIMIT 10;")

@app.get("/ask/")
def ask_text(query_str: str | None = "What are employers with certified rates higher than 90%?" ):
    state: State = {"question": query_str}
    executions = ask(state)
    # {'write_query': {'query': 'SELECT COUNT(DISTINCT case_id) AS total_unique_cases FROM cases;'},
    # 'execute_query': {'result': 'Error: (sqlite3.OperationalError) no such table: cases\n[SQL: SELECT COUNT(DISTINCT case_id) AS total_unique_cases FROM cases;]\n(Background on this error at: https://sqlalche.me/e/20/e3q8)'},
    # 'generate_answer': {'answer': "The SQL query attempted to count the total unique cases by selecting distinct `case_id` values from a table called `cases`. However, the query resulted in an error indicating that the table `cases` does not exist in the database.\n\nTherefore, it's not possible to determine the total unique cases due to the absence of the `cases` table. You may need to check if the table exists or if there is a different table name you should be querying."}}
    return executions['generate_answer']








@app.on_event("startup")
def on_startup():
    create_db_and_tables()