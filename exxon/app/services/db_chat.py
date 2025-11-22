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

# Load environment variables
load_dotenv()
EXXON_DB_URL = os.getenv("EXXON_DB_URL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def init_database():
    return SQLDatabase.from_uri(EXXON_DB_URL)

def get_sql_chain(db):

    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
    Question: Name 10 artists
    SQL Query: SELECT Name FROM Artist LIMIT 10;
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    # Initialize ChatOpenAI with OpenRouter configuration
    llm = ChatOpenAI(
        model_name="google/gemini-2.5-flash-lite-preview-06-17",  # You can choose any OpenRouter model
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
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}"""
    prompt = ChatPromptTemplate.from_template(template)
    
    # Initialize another ChatOpenAI instance with OpenRouter for the response
    llm = ChatOpenAI(
        model_name="google/gemini-2.5-flash-lite-preview-06-17",  # You can choose any OpenRouter model
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
    )
    
    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"]),
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

# Function to get history from MySQL (Chat table)
async def get_chat_history_from_db(session: AsyncSession, limit: int = 0):
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
