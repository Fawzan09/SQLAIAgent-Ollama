import os
import json
import json5
from dotenv import load_dotenv
from sqlalchemy.engine import create_engine
from engineio.payload import Payload
import chainlit as cl

from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.model.openai import OpenAIChat

from agents_tools.raw_sql_executor import RawSQLExecutor
# from phi.tools.sql import SQLTools
from agents_tools.flexible_sql_tool import FlexibleSQLTool

load_dotenv()
Payload.max_decode_packets = 1000

# Environment setup
db_url = os.getenv('DB_URL')
openai_api_key = os.getenv('OPENAI_API_KEY')
model_provider = os.getenv('MODEL_PROVIDER', 'ollama').lower()
model_name = os.getenv('MODEL_NAME', 'llama3.1')

# Disable telemetry
os.environ["PHI_TELEMETRY"] = "false"

# Determine DB type
try:
    engine = create_engine(db_url)
    with engine.connect():
        db_type = engine.dialect.name
except Exception as e:
    print(f"Database connection error: {e}")
    db_type = "sqlite"

# Model selector
def create_model():
    if model_provider == 'openai':
        return OpenAIChat(
            id=model_name,
            api_key=openai_api_key,
            temperature=0.1,
            max_tokens=6000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
    else:
        return Ollama(
            id=model_name,
            host="http://localhost:11434",
            options={
                "temperature": 0.1,
                "top_p": 1.0,
                "top_k": 50,
                "presence_penalty": 0.0,
                "frequency_penalty": 0.0,
                "num_predict": 2048
            }
        )

# Create structured-response agent
def create_agent():
    model = create_model()
    return Agent(
        tools=[FlexibleSQLTool(db_url=db_url)],
        model=model,
        add_history_to_messages=True,
        num_history_responses=10,
        prevent_hallucinations=True,
        system_prompt=f"""
You are an expert SQL assistant connected to a {db_type} database.

IMPORTANT BEHAVIOR RULES:
1. When asked about database information (name, tables, data, structure) – IMMEDIATELY execute the appropriate SQL query.
2. Never say "I don't know" if you can find out with a SQL query.
3. Always show both the SQL query and the results.
4. Always respond STRICTLY in valid JSON according to this schema:

{{
  "thought": "A brief reasoning about the user's request.",
  "sql": "The SQL query you executed.",
  "result": [ ... array of objects with the query results ... ],
  "explanation": "Explanation of the result in plain English."
}}

If an error occurs, return:

{{
  "thought": "...",
  "sql": "...",
  "error": "A description of the error or reason for the absence of data.",
  "explanation": "A human-readable clarification."
}}

Return the SQL query as a plain text string, do NOT escape any quotes or use Unicode escapes.
Do not add comments, Markdown, or extra formatting outside the JSON object.
""",
        instructions=[
            "STRICT JSON FORMAT",
            "Execute SQL queries immediately when asked about database information",
            "Always show the SQL query and results",
            "Be proactive – don't ask permission to run queries"
        ],
    )

def render_response(data):
    parts = []

    if 'thought' in data:
        parts.append(f"🧠 **Thought:** {data['thought']}")

    if 'sql' in data:
        parts.append(f"📝 **SQL Query:**\n```sql\n{data['sql']}\n```")

    if 'error' in data:
        parts.append(f"❌ **Error:**\n```\n{data['error']}\n```")

    if 'result' in data:
        result = data['result']
        if isinstance(result, list) and result and isinstance(result[0], dict):
            keys = result[0].keys()
            header = "| " + " | ".join(keys) + " |\n"
            separator = "| " + " | ".join(["---"] * len(keys)) + " |\n"
            rows = "\n".join("| " + " | ".join(str(row.get(k, "")) for k in keys) + " |" for row in result)
            parts.append(f"📊 **Result:**\n{header}{separator}{rows}")
        elif isinstance(result, list) and all(isinstance(r, str) for r in result):
            parts.append("📊 **Result:**\n" + "\n".join(f"- {r}" for r in result))
        else:
            parts.append(f"📊 **Result:** {result}")

    if 'explanation' in data:
        parts.append(f"💡 **Explanation:** {data['explanation']}")

    return "\n\n".join(parts)

@cl.on_chat_start
async def on_chat_start():
    agent = create_agent()
    flex_sql = FlexibleSQLTool(db_url=db_url)
    cl.user_session.set("agent", agent)
    cl.user_session.set("raw_sql", RawSQLExecutor(db_url=db_url))
    cl.user_session.set("flex_sql", flex_sql)

    # Get database info for welcome message
    try:
        tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        raw = RawSQLExecutor(db_url=db_url)
        tables_result = raw.run_query(tables_query)
        tables_list = [row['name'] for row in tables_result.get('result', [])]
        tables_info = ", ".join(tables_list) if tables_list else "No tables found"
    except:
        tables_info = "Unable to fetch table information"

    msg = f"""🏢 **WDP Office Data Analytics - SQL AI Agent Ready!**

📊 **Database**: {db_type}  
🧠 **Model**: {model_provider.upper()} – {model_name}  
📋 **Available Tables**: {tables_info}

---

### 🚀 **Quick Start Guide**

**Natural Language Queries:**
- "Show me all employees in the marketing department"
- "What's the total revenue this quarter?"
- "Find the top 5 customers by sales volume"

**Commands:**
- `/run SELECT * FROM employees LIMIT 5` - Execute raw SQL
- `/raw [query]` - Get raw table output
- `/summary [query]` - Get summarized results
- `/help` - Show detailed help
- `/schema` - Show database structure

**Pro Tips:**
- Ask about data relationships and insights
- Request charts and analysis (coming soon)
- Use natural language - the AI understands context!

---

**🎯 Ready to explore your WDP office data!** Ask me anything about your database."""

    await cl.Message(content=msg).send()




@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    raw = cl.user_session.get("raw_sql")        # instance of RawSQLExecutor
    flex = cl.user_session.get("flex_sql")      # instance of FlexibleSQLTool
    content = message.content.strip()

    # Check for special commands
    lowered = content.lower()
    
    if lowered.startswith("/help") or lowered == "help":
        help_msg = """## 📚 **WDP Office Data Analytics - Help Guide**

### 🔍 **Natural Language Queries**
You can ask questions in plain English:
- "Show me all employees"
- "What's the average salary by department?"
- "Find customers from New York"
- "Count how many orders were placed last month"

### 💻 **Command Reference**
- `/run [SQL]` - Execute raw SQL query
- `/raw [query]` - Get raw table format output
- `/summary [query]` - Get summarized analysis
- `/schema` - Show complete database structure
- `/tables` - List all available tables
- `/help` - Show this help guide

### 📊 **Sample Queries to Try**
- "Describe the database structure"
- "Show me sample data from each table"
- "What are the column names and types?"
- "Give me insights about the data relationships"

### 🎯 **Pro Tips**
- Be specific about what data you want
- Ask for explanations if results are unclear
- Use follow-up questions to dive deeper
- The AI remembers your conversation context

### 🚀 **Getting Started**
1. Ask `/schema` to see your database structure
2. Try a simple query like "show me sample data"
3. Ask specific business questions about your data

**Need specific help?** Just ask! I'm here to help you analyze your WDP office data efficiently."""
        
        await cl.Message(content=help_msg).send()
        return
    
    elif lowered.startswith("/schema"):
        schema_query = "SELECT sql FROM sqlite_master WHERE type='table';"
        result = raw.run_query(schema_query)
        if result.get('result'):
            schema_info = "## 🗂️ **Database Schema**\n\n"
            for row in result['result']:
                schema_info += f"```sql\n{row['sql']}\n```\n\n"
        else:
            schema_info = "❌ Could not retrieve schema information."
        await cl.Message(content=schema_info).send()
        return
    
    elif lowered.startswith("/tables"):
        tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        result = raw.run_query(tables_query)
        if result.get('result'):
            tables_list = [row['name'] for row in result['result']]
            tables_info = f"## 📋 **Available Tables**\n\n" + "\n".join([f"- **{table}**" for table in tables_list])
        else:
            tables_info = "❌ No tables found."
        await cl.Message(content=tables_info).send()
        return

    elif lowered.startswith("/run"):
        query = content[4:].strip()
        result = raw.run_query(query)
        response_md = render_response(result)
        await cl.Message(content=response_md).send()
        return

    elif lowered.startswith("/raw"):
        query = content[4:].strip()
        result = flex.use(query, format="table")
        await cl.Message(content=f"📄 **Raw Output:**\n```\n{result}\n```").send()
        return

    elif lowered.startswith("/summary"):
        query = content[8:].strip()
        result = flex.use(query, format="summary")
        await cl.Message(content=f"📊 **Summary:**\n```\n{result}\n```").send()
        return

    # Default: send to model (SQLAgent)
    try:
        chunks = []
        result = await cl.make_async(agent.run)(content, stream=True)
        for chunk in result:
            chunks.append(chunk.get_content_as_string())
        response_text = "".join(chunks).strip()

        try:
            data = json.loads(response_text)
        except json.JSONDecodeError:
            data = json5.loads(response_text)

        response_md = render_response(data)
        await cl.Message(content=response_md).send()

    except Exception as e:
        print(f"Unexpected error: {e}")
        await cl.Message(content=f"❌ **Unexpected Error**: {e}").send()

