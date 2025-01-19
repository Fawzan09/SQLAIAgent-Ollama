from phi.agent import Agent
from phi.tools.sql import SQLTools
from phi.model.ollama import Ollama
import chainlit as cl
from dotenv import load_dotenv
import os
from sqlalchemy.engine import create_engine
from engineio.payload import Payload


load_dotenv()
Payload.max_decode_packets = 1000
db_url = os.getenv('DB_URL')
# Remove telemetry
os.environ["PHI_TELEMETRY"] = "false"
print("Telemetry disabled:", os.environ["PHI_TELEMETRY"])
# Detecting the database's type
try:
    engine = create_engine(db_url)
    with engine.connect() as connection:
        print("Database connection successful")
except Exception as e:
    print(f"Database connection error: {e}")
db_type = engine.dialect.name  # sqlite, postgresql, etc


# Creating an agent with Ollama model
def create_agent():
    ollama_model = Ollama(
        id="llama3.1",
        host="http://localhost:11434",
        options={
            "temperature": 0.1,
            # "max_tokens": 300,
            #"top_p": 8.0,
            #"top_k": 50,
            #"presence_penalty": 0.0,
            #"frequency_penalty": 0.1
        }
    )

    sql_agent = Agent(
        tools=[SQLTools(db_url=db_url)],  # Connect to SQL-tool
        model=ollama_model,
        # using Ollama running model
        add_history_to_messages=True,
        num_history_responses=10,
        prevent_hallucinations=True,
        description=f"You are a helpful AI agent that answers questions for a {db_type} database. Your responses must be detailed, accurate, and strictly based on the database context. Avoid answering out-of-context questions.",
        instructions=[
            f"Answer the questions related to the {db_type} SQL database in detail.",
            "Do not answer any questions which are out of the context of the database.",
            "Execute the SQL query on the connected database.",
            "Return the query results in a readable format.",
            "Include the SQL query used to get the answer in your reply."
        ],

    )
    return sql_agent

# Chat start processor
@cl.on_chat_start
async def on_chat_start():
    print(f"Starting chat. Detected database type: {db_type}")
    sql_agent = create_agent()
    cl.user_session.set("agent", sql_agent)
    print(f"Agent initialized for {db_type} database.")

# Messages processor
@cl.on_message
async def on_message(message: cl.Message):
    try:
        print(f"Received message: {message.content}")
        agent = cl.user_session.get("agent")
        msg = cl.Message(content="")
        for chunk in await cl.make_async(agent.run)(message.content, stream=True):
            await msg.stream_token(chunk.get_content_as_string())
        await msg.send()
    except KeyError as e:
        print(f"KeyError: {e}")
        await cl.Message(content=f"Error: Missing key in session: {e}").send()
    except AttributeError as e:
        print(f"AttributeError: {e}")
        await cl.Message(content=f"Error: Invalid operation: {e}").send()
    except Exception as e:
        print(f"Unexpected error: {e}")
        await cl.Message(content=f"An unexpected error occurred: {e}").send()
