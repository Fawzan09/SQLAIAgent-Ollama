# SQL AI Agent

A powerful SQL AI agent built with Phi Data that helps you interact with your databases through natural language conversations. This project leverages a **local LLM (Ollama)** for secure and efficient database interactions.

---
## ✨ Features

- Natural language to SQL query conversion
- Interactive chat interface using **Chainlit**
- Secure database connection handling
- Context-aware conversation with history retention
- Customizable agent behavior with prompts
- Support for multiple SQL databases (**MySQL, PostgreSQL, SQLite, etc.**)
- Easy database configuration via connection URLs
- Local LLM model support (**Ollama**)

![img.png](img.png)
---
## 🛠️ Technology Stack

- **Phi Data**: Core AI agent functionality and tools
- **Ollama**: Local LLM integration with **llama3.1**
- **Chainlit**: Web-based chat interface
- **SQLAlchemy**: SQL toolkit and ORM
- **Database Connectors**:
  - **PyMySQL** for MySQL
  - **psycopg2** for PostgreSQL
  - Other SQLAlchemy-supported databases
- **Python-dotenv**: Environment variable management
---
## 🚀 Getting Started

### Prerequisites

- Python 3.10+ 
- A SQL database (**MySQL, PostgreSQL, SQLite, etc.**)
- **Ollama** installed and running on your system (follow [Ollama's documentation](https://www.ollama.com/docs/installation) to install and run it)
- Llama3.1 model preloaded in Ollama

### Installation

1. Clone the repository:
```bash
git clone https://github.com/loglux/SQLAIAgent-Ollama.git
cd SQLAIAgent-Ollama
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Install and serve the llama3.1 model locally with Ollama:
```bash
ollama pull llama3.1
```

4. Create a `.env` file in the root directory with your credentials:
```env
DB_URL=your_database_url
```

### Database Connection URLs

The application supports various SQL databases. Here are examples of connection URLs for different databases:

#### MySQL
```
DB_URL=mysql+pymysql://username:password@host:port/database_name
```

#### PostgreSQL
```
DB_URL=postgresql://username:password@host:port/database_name
```

#### SQLite
```
DB_URL=sqlite:///path/to/database.db
```

Note: Make sure to install the appropriate database connector package for your chosen database.

### Running the Application

Start the application using Chainlit:
```bash
chainlit run app.py
```
---

## 💡 Usage

Once the application is running:
1. Open the provided Chainlit link in your browser.
2. Start chatting with the AI agent using natural language queries.
3. Ask questions about your database and get detailed responses.
4. View the SQL queries used in the responses.

Example queries:
- "List the first 2 records from the table 'users'"
- "Show me all records from 'users' table"

## ⚠️ Error Handling

The application includes robust error handling for:
- Database connection issues
- Invalid queries
- Session management errors

---
## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

# Key Differences Between the Original and Forked Versions:

---

#### 1. **Model**:
   - **Original**: Uses the `Groq` model with `llama-3.3-70b-versatile` via an API key.
     ```python
     model=Groq(id="llama-3.3-70b-versatile", api_key=api_key)
     ```
   - **Forked**: Uses the locally deployed `Ollama` model with ID `llama3.1`.
     ```python
     ollama_model = Ollama(
         id="llama3.1",
         host="http://localhost:11434",
         options={...}
     )
     ```

   **Difference**: The forked version replaces the external model with a locally deployed one, removing the dependency on an external API and adding parameters for fine-tuning the model (e.g., `temperature`, `top_p`).

---

#### 2. **Database Handling**:
   - **Original**: Assumes the database is MySQL.
     ```python
     instructions=[
         "Answer the questions related to the MySQL database in detail."
     ]
     ```
   - **Forked**: Automatically detects the database type using SQLAlchemy.
     ```python
     engine = create_engine(db_url)
     db_type = engine.dialect.name  # sqlite, postgresql, etc
     ```
     Instructions and descriptions dynamically adapt to the detected database type:
     ```python
     description=f"You are a helpful AI agent that answers questions for a {db_type} database."
     instructions=[f"Answer the questions related to the {db_type} SQL database in detail."]
     ```

   **Difference**: The forked version is versatile and supports multiple database types instead of being limited to MySQL.

---

#### 3. **Message History**:
   - **Original**: Keeps only 3 previous responses.
     ```python
     num_history_responses=3
     ```
   - **Forked**: Extends the history to 10 previous responses for better context.
     ```python
     num_history_responses=10
     ```

   **Difference**: The forked version supports longer conversational context for handling more complex queries.

---

#### 4. **Hallucination Prevention**:
   - **Original**: Does not include measures to prevent "hallucinated" responses.
   - **Forked**: Adds a `prevent_hallucinations` parameter to minimise incorrect responses:
     ```python
     prevent_hallucinations=True
     ```

   **Difference**: The forked version explicitly instructs the model to avoid making up answers and respond appropriately when data is unavailable.

---

#### 5. **Telemetry**:
   - **Original**: Does not disable telemetry.
   - **Forked**: Explicitly disables telemetry for privacy:
     ```python
     os.environ["PHI_TELEMETRY"] = "false"
     ```

   **Difference**: The forked version ensures the system operates in a private environment.

---

#### 6. **Model Configuration**:
   - **Original**: No configuration for parameters like `temperature` or `max_tokens`.
   - **Forked**: Includes additional model configuration options for better output control:
     ```python
     options={
         "temperature": 0.1,
         "top_p": 1.0,
         "presence_penalty": 0.0,
         "frequency_penalty": 0.0
     }
     ```

   **Difference**: The forked version allows precise control over the model's behaviour and responses.

---

#### 7. **Message Processing**:
   - **Original**: Adds chat context to OpenAI explicitly:
     ```python
     cl.chat_context.to_openai()
     ```
   - **Forked**: Removes the `cl.chat_context.to_openai()` call as it is unnecessary for a locally running model.

   **Difference**: The forked version simplifies message processing for the local setup.

---

#### 8. **Code Formatting and Documentation**:
   - **Original**: Minimal comments, specific to MySQL.
   - **Forked**: Includes detailed comments for universal usage:
     ```python
     # Detecting the database's type
     engine = create_engine(db_url)
     db_type = engine.dialect.name  # sqlite, postgresql, etc
     ```

   **Difference**: The forked version has more structured and readable code with better documentation.

---

### Conclusion:

The forked version:
- Supports multiple database types instead of being limited to MySQL.
- Utilises a locally deployed model (Ollama) rather than an external API.
- Enhances response accuracy by adding hallucination prevention and better control over model behaviour.
- Extends conversational history for improved context in complex interactions.
- Disables telemetry for privacy and has more detailed documentation.

If flexibility and local operation are your priorities, the forked version is the better choice. The original version works well if you only need MySQL and external API integration.
