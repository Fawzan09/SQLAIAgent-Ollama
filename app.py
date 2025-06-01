from phi.agent import Agent
from phi.tools.sql import SQLTools
from phi.model.ollama import Ollama
from phi.model.openai import OpenAIChat
import chainlit as cl
from dotenv import load_dotenv
import os
from sqlalchemy.engine import create_engine
from engineio.payload import Payload

load_dotenv()
Payload.max_decode_packets = 1000
db_url = os.getenv('DB_URL')
openai_api_key = os.getenv('OPENAI_API_KEY')
model_provider = os.getenv('MODEL_PROVIDER', 'ollama').lower()  # 'ollama' or 'openai'
model_name = os.getenv('MODEL_NAME', 'llama3.1')  # for ollama or openai model name

# Remove telemetry
os.environ["PHI_TELEMETRY"] = "false"
print("Telemetry status:", os.environ["PHI_TELEMETRY"])
print(f"Model provider: {model_provider}")
print(f"Model name: {model_name}")

# Initialize variables
engine = None
db_type = "unknown"

# Detecting the database's type
try:
    engine = create_engine(db_url)
    with engine.connect() as connection:
        print("Database connection successful")
    db_type = engine.dialect.name  # sqlite, postgresql, etc
except Exception as e:
    print(f"Database connection error: {e}")
    # Set a default database type or exit the application
    db_type = "sqlite"  # or you could exit here if database is critical


def create_model():
    """Create and return the appropriate model based on configuration"""
    if model_provider == 'openai':
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI models")

        print(f"Initializing OpenAI model: {model_name}")
        return OpenAIChat(
            id=model_name,
            api_key=openai_api_key,
            temperature=0.1,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
    else:  # ollama
        print(f"Initializing Ollama model: {model_name}")
        return Ollama(
            id=model_name,
            host="http://localhost:11434",
            options={
                "temperature": 0.1,
                "top_p": 1.0,
                "top_k": 50,
                "presence_penalty": 0.0,
                "frequency_penalty": 0.0
            }
        )


# Creating an agent with selected model
def create_agent():
    try:
        model = create_model()

        sql_agent = Agent(
            tools=[SQLTools(db_url=db_url)],
            model=model,
            add_history_to_messages=True,
            num_history_responses=10,
            prevent_hallucinations=False,
            system_prompt=f"""You are an expert SQL assistant connected to a {db_type} database.

IMPORTANT BEHAVIOR RULES:
1. When asked about database information (name, tables, data, structure) - IMMEDIATELY execute the appropriate SQL query
2. Never say "I don't know" if you can find out with a SQL query
3. Always show both the SQL query and the results
4. Be proactive and helpful

Examples:
- "What's the database name?" → Execute SELECT current_database(); immediately
- "What tables exist?" → Execute SELECT table_name FROM information_schema.tables; immediately  
- "Show me users" → Execute SELECT * FROM users LIMIT 5; immediately

Always be helpful and execute queries to answer questions!""",

            instructions=[
                "Execute SQL queries immediately when asked about database information",
                "Always show the SQL query and results",
                "Be proactive - don't ask permission to run queries",
                "Help users understand their database through queries"
            ],
        )
        return sql_agent
    except Exception as e:
        print(f"Error creating agent: {e}")
        raise


# Chat start processor
@cl.on_chat_start
async def on_chat_start():
    try:
        print(f"Starting chat. Detected database type: {db_type}")
        print(f"Using {model_provider} model: {model_name}")

        sql_agent = create_agent()
        cl.user_session.set("agent", sql_agent)

        # Send welcome message with model info
        welcome_msg = f"🤖 **SQL AI Agent Ready!**\n\n"
        welcome_msg += f"📊 **Database**: {db_type}\n"
        welcome_msg += f"🧠 **Model**: {model_provider.upper()} - {model_name}\n\n"
        welcome_msg += "Ask me anything about your database!"

        await cl.Message(content=welcome_msg).send()
        print(f"Agent initialized for {db_type} database using {model_provider}.")

    except Exception as e:
        error_msg = f"❌ **Initialization Error**: {str(e)}"
        await cl.Message(content=error_msg).send()
        print(f"Error during chat start: {e}")


# Messages processor
@cl.on_message
async def on_message(message: cl.Message):
    try:
        print(f"Received message: {message.content}")
        agent = cl.user_session.get("agent")

        if not agent:
            await cl.Message(content="❌ Agent not initialized. Please refresh the page.").send()
            return

        msg = cl.Message(content="")
        for chunk in await cl.make_async(agent.run)(message.content, stream=True):
            await msg.stream_token(chunk.get_content_as_string())
        await msg.send()

    except KeyError as e:
        print(f"KeyError: {e}")
        await cl.Message(content=f"❌ **Session Error**: Missing key in session: {e}").send()
    except AttributeError as e:
        print(f"AttributeError: {e}")
        await cl.Message(content=f"❌ **Operation Error**: Invalid operation: {e}").send()
    except Exception as e:
        print(f"Unexpected error: {e}")
        await cl.Message(content=f"❌ **Unexpected Error**: {e}").send()