import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import ChatOpenAI
from app.database import Chat
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import re

# Load environment variables
load_dotenv()
EXXON_DB_URL = os.getenv("EXXON_DB_URL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def init_database():
    return SQLDatabase.from_uri(EXXON_DB_URL)

def get_sql_chain(db):

    template = """
    You are an expert MySQL query generator.
    You generate raw SQL queries that will be executed directly in MySQL without modification.

    CRITICAL MYSQL RULES (MUST FOLLOW EXACTLY):
    - Generate SQL exactly as MySQL expects it.
    - Never escape percent (%) signs for any reason.
    - Never output double-percent signs such as %%Y, %%m, or %% anything.
    - Always write DATE_FORMAT(column, '%Y-%m') exactly like this.
    - Never wrap SQL in Python formatting or escape sequences.
    - Never output backslashes.
    - Never output Python-style strings.
    - Output only pure SQL, nothing else.

    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}

    Question: {question}

    Write only the SQL query and nothing else.
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(
        model_name="x-ai/grok-4.1-fast",
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.1,
        max_tokens=1000,
    )

    def get_schema(_):
        return db.get_table_info()

    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )



def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    sql_chain = get_sql_chain(db)

    template = """
    You are a helpful and professional data analyst assistant.
    Your task is to answer the user’s question based on the SQL query result.

    <DATABASE_SCHEMA>
    {schema}
    </DATABASE_SCHEMA>

    <CONVERSATION_HISTORY>
    {chat_history}
    </CONVERSATION_HISTORY>

    <USER_QUESTION>
    {question}
    </USER_QUESTION>

    <SQL_QUERY>
    {query}
    </SQL_QUERY>

    <SQL_RESULT>
    {response}
    </SQL_RESULT>

    Write a clear, concise, and well-structured response in natural language.


    Formatting requirements:

    - Use section titles such as **Findings**, **Details**, and **Summary**.
    - Between each section, use two newlines to separate them.
    - Present lists using bullet points for readability.
    - Dates must be formatted as “YYYY-MM-DD” unless the user asks otherwise.
    - Include units (e.g., MT) whenever relevant.
    - If multiple items share the same material code, group them (e.g., “MAT-0265 appears 2 times, total 49.500 MT”).
    - Provide helpful aggregations (counts, totals, earliest and latest dates).
    - Avoid repeating raw SQL output unless necessary.
    - If the result is empty or ambiguous, state this clearly.

    End with a short **Summary** section that highlights:
    - Key insights
    - Total counts
    - Totals or ranges if applicable
    """


    prompt = ChatPromptTemplate.from_template(template)
    
    # Initialize another ChatOpenAI instance with OpenRouter for the response
    llm = ChatOpenAI(
        model_name="x-ai/grok-4.1-fast",  # You can choose any OpenRouter model
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
    )
    
    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            # sanitize SQL returned from LLM before running it against the DB
            response=lambda vars: db.run(sanitize_sql(vars.get("query"))),
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    print('chain-->',chain)
    return chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
    })


def sanitize_sql(raw_query: str) -> str:
    """
    Clean up SQL text returned by the LLM before executing it.

    Handles common wrappers the model may return, e.g.:
    - Triple-backtick fenced blocks (```sql ... ```)
    - Inline language fences (```sql)
    - <SQL>...</SQL> tags
    - Leading labels like 'SQL Query:'

    Returns the cleaned SQL string.
    """
    if not raw_query:
        return raw_query

    if not isinstance(raw_query, str):
        raw_query = str(raw_query)

    q = raw_query.strip()

    # 1) Extract between <SQL>...</SQL> if present
    m = re.search(r"<SQL>([\s\S]*?)</SQL>", q, flags=re.IGNORECASE)
    if m:
        q = m.group(1).strip()

    # 2) Extract first fenced code block if present (``` or ```sql)
    m = re.search(r"```(?:sql)?\n([\s\S]*?)```", q, flags=re.IGNORECASE)
    if m:
        q = m.group(1).strip()

    # 3) If there are any leading labels like 'SQL Query:' or 'SQL:' remove them
    q = re.sub(r"^\s*(SQL Query:|SQL:)\s*", "", q, flags=re.IGNORECASE)

    # 4) Remove any leading/trailing markdown quoting or fences (like > )
    #    and remove any trailing explanatory text after a semicolon block
    #    Keep whole statement; do not truncate final semicolon.
    q = q.strip()

    return q

# Function to get history from MySQL (Chat table)
async def get_chat_history_from_db(session: AsyncSession, limit: int = 10):
    result = await session.execute(select(Chat).order_by(Chat.createdAt.desc()).limit(limit))
    history = list(reversed(result.scalars().all()))
    chat_history = []
    for m in history:
        if m.sender == "user":
            chat_history.append(HumanMessage(content=m.message))
        else:
            chat_history.append(AIMessage(content=m.message))

    return chat_history

# Function to save a user message to the Chat table
async def save_user_message(session: AsyncSession, message: str):
    user_chat = Chat(message=message, sender="user")
    session.add(user_chat)
    await session.commit()


# Function to save a bot message to the Chat table
async def save_bot_message(session: AsyncSession, message: str):
    bot_chat = Chat(message=message, sender="bot")
    session.add(bot_chat)
    await session.commit()
    await session.close()  # Close session to avoid caching

# Async function for Q&A using history from db and save both user and bot messages
async def get_response_with_db_history(user_query: str, db: SQLDatabase, session: AsyncSession):
    # Save user message
    await save_user_message(session, user_query)
    chat_history = await get_chat_history_from_db(session,limit=0)
    print('chat_history-->',chat_history)
    answer = get_response(user_query, db, chat_history)
    # Save bot message
    await save_bot_message(session, answer)
    return answer
