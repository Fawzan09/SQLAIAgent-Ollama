from phi.agent import Agent
from phi.tools.sql import SQLTools
from phi.model.groq import Groq
from phi.model.google import Gemini
import chainlit as cl
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.getenv('GROQ_API_KEY')
db_url=os.getenv('DB_URL')


def create_agent():
    sql_agent=Agent(
    tools=[SQLTools(db_url=db_url)],
    model=Groq(id="llama-3.3-70b-versatile",api_key=api_key),
    add_chat_history_to_messages=True,
    num_history_responses=3,
    description="You are a helpful AI agent, that answers regarding the questions of the sql database and the tables in it, Your responses must be detailed and accurate, You should not respond to any out of the context questions.",
    instructions=["Answer the questions related to the MySQL database in detail.","Do not answer any questions which are out of the context of the database.","If the user greets you greet them back politely.","Make sure to also include the SQL Query used to get the answer in your reply."]
)
    return sql_agent

@cl.on_chat_start
async def on_chat_start():
    print("Hello there, you can now chat with your MySQL Database :D")
    sql_agent=create_agent()
    cl.user_session.set("agent", sql_agent)

@cl.on_message
async def on_message(message : cl.Message):
    try:
        agent=cl.user_session.get("agent")
        cl.chat_context.to_openai()
        msg=cl.Message(content="")
        for chunk in await cl.make_async(agent.run)(message.content,stream=True):
            await msg.stream_token(chunk.get_content_as_string())
    
        await msg.send()
    
    except KeyError as e:
         await cl.Message(content=f"Error: Missing key in session: {e}").send()
    
    except AttributeError as e:
        # Handle AttributeError (e.g., issues with 'agent.run')
        await cl.Message(content=f"Error: Invalid operation: {e}").send()
    
    except Exception as e:
        # Handle all other exceptions
        await cl.Message(content=f"An unexpected error occurred: {e}").send()






