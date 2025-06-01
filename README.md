# SQL AI Agent

A powerful SQL AI agent built with Phi Data that helps you interact with your databases through natural language conversations. This project supports both **local LLM (Ollama)** and **OpenAI API** models for flexible deployment options.

**🚀 Latest Update**: Enhanced AI agent with improved system prompts for better responsiveness and proactive query execution!

---
## ✨ Features

- **🤖 Enhanced AI Agent**: Advanced system prompts for proactive SQL query execution
- **🔄 Dual Model Support**: Switch between local Ollama models and OpenAI API models
- **⚡ Intelligent Query Execution**: Agent automatically executes SQL queries without asking permission
- **🎯 Improved Responsiveness**: No more "I don't know" responses - agent actively investigates database
- **💬 Natural Language Interface**: Ask questions in plain English, get SQL results
- **🖥️ Interactive Chat Interface**: Clean web interface using **Chainlit**
- **🔒 Secure Database Handling**: Safe database connection management
- **📝 Context-Aware Conversations**: Remembers conversation history
- **🛢️ Multi-Database Support**: Works with **MySQL, PostgreSQL, SQLite, and more**
- **⚙️ Easy Configuration**: Simple environment variable setup

![img.png](img.png)

---
## 🛠️ Technology Stack

- **Phi Data**: Core AI agent functionality and tools
- **Enhanced Prompting System**: Custom system prompts for optimal performance
- **Model Options**:
  - **Ollama**: Local LLM integration (llama3.1, llama3.2, codellama, etc.)
  - **OpenAI API**: Cloud-based models (gpt-4o-mini, gpt-4o, gpt-3.5-turbo, etc.)
- **Chainlit**: Web-based chat interface
- **SQLAlchemy**: SQL toolkit and ORM
- **Database Connectors**:
  - **PyMySQL** for MySQL
  - **psycopg2** for PostgreSQL
  - Other SQLAlchemy-supported databases
- **Python-dotenv**: Environment variable management

---
## 🆕 What's New in This Version

### 🎯 Dramatically Improved AI Agent Performance
- **🧠 Advanced System Prompts**: Completely redesigned agent behavior with sophisticated system prompts
- **⚡ Proactive Query Execution**: Agent now automatically executes SQL queries instead of asking permission
- **🚫 Eliminated "I Don't Know" Responses**: Agent actively investigates database to find answers
- **📊 Smarter Database Interaction**: Immediately responds with relevant SQL queries and results
- **🔄 Better Context Understanding**: Enhanced comprehension of user intent and database structure

### 🔧 Technical Improvements
- **Optimized temperature settings** for more consistent responses
- **Enhanced error handling** with detailed feedback
- **Improved session management** for better stability
- **Streamlined model switching** between Ollama and OpenAI

---
## 🚀 Getting Started

### Prerequisites

- Python 3.10+ 
- A SQL database (**MySQL, PostgreSQL, SQLite, etc.**)
- **For Ollama**: Ollama installed and running locally
- **For OpenAI**: Valid OpenAI API key

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

3. **For Ollama usage** - Install and serve your preferred model:
```bash
ollama pull llama3.1
# or
ollama pull llama3.2
# or
ollama pull codellama
```

4. **Configure environment variables**:

   **Copy the example configuration file:**
   ```bash
   cp .env.example .env
   ```

   **Edit the `.env` file with your settings:**
   ```bash
   # On Linux/Mac
   nano .env
   
   # On Windows
   notepad .env
   ```

   **Update the following variables with your actual values:**
   - Replace `sk-your-openai-api-key-here` with your actual OpenAI API key (if using OpenAI)
   - Adjust `MODEL_PROVIDER` and `MODEL_NAME` according to your preference

### Configuration Options

#### Option 1: Using Ollama (Local)
```env
DB_URL=your_database_url
MODEL_PROVIDER=ollama
MODEL_NAME=llama3.1
```

#### Option 2: Using OpenAI API
```env
DB_URL=your_database_url
MODEL_PROVIDER=openai
MODEL_NAME=gpt-4o-mini
OPENAI_API_KEY=your_openai_api_key_here
```

### Model Options

#### Ollama Models (Local)
- `llama3.2` - **Recommended** - Better for structured tasks than 3.1
- `llama3.1` - Good but may need `prevent_hallucinations=True`
- `codellama` - **Best for SQL** - Specialized for code and database queries
- `mistral` - Good alternative with consistent performance
- And other models available in Ollama

> **💡 Tip**: For Ollama models, consider setting `prevent_hallucinations=True` in `app.py` for better SQL task performance.

#### OpenAI Models (API)
- `gpt-4o-mini` - **Recommended** - Cost-effective with excellent SQL performance
- `gpt-4o` - Best quality but more expensive
- `gpt-3.5-turbo` - Fast and efficient for simple queries
- `gpt-4-turbo` - High-performance for complex analysis

> **💡 Tip**: OpenAI models generally work well with the default `prevent_hallucinations=False` setting.

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

The application will automatically detect your configured model provider and initialize accordingly.

---

## 💡 Usage

Once the application is running:
1. Open the provided Chainlit link in your browser.
2. The welcome message will show which model and database type are being used.
3. Start chatting with the AI agent using natural language queries.
4. **The agent will automatically execute SQL queries and show results!**
5. View both the SQL queries used and their formatted results.

### ✨ Example Interactions

**Before (Old Version):**
```
User: "What's the database name?"
Agent: "I don't know. You can run SELECT current_database();"
```

**After (New Version):**
```
User: "What's the database name?"
Agent: "The database name is 'my_database'.

SQL Query Used:
SELECT current_database();

Result: my_database"
```

### 🎯 Example Queries
- **"What's the database name?"** - Instantly shows database name
- **"What tables exist?"** - Lists all tables immediately  
- **"Show me the users table structure"** - Displays table schema
- **"List the first 5 records from orders"** - Shows sample data
- **"How many records are in the products table?"** - Gives count
- **"What columns does the customers table have?"** - Shows column info

## 🔄 Switching Between Models

To switch between Ollama and OpenAI:

1. **Update your `.env` file**:
   ```env
   # For Ollama
   MODEL_PROVIDER=ollama
   MODEL_NAME=llama3.1
   
   # For OpenAI
   MODEL_PROVIDER=openai
   MODEL_NAME=gpt-4o-mini
   OPENAI_API_KEY=your_api_key
   ```

2. **Restart the application**:
   ```bash
   chainlit run app.py
   ```

## ⚠️ Error Handling

The application includes robust error handling for:
- Database connection issues
- Model initialization errors
- Invalid queries
- Session management errors
- API key validation (for OpenAI)
- SQL execution errors with helpful suggestions

---

## 🔒 Privacy & Security

- **Ollama**: Completely local processing, no data sent to external services
- **OpenAI**: Data is sent to OpenAI's servers, ensure compliance with your privacy requirements
- **Database**: Always stays local, never sent to external model providers beyond query context

---

## 🎯 Performance Improvements

| Aspect | Before | After |
|--------|--------|-------|
| **Response Time** | Asks permission first | Immediate execution |
| **User Experience** | Manual query requests | Automatic investigation |
| **Error Handling** | Generic "I don't know" | Specific helpful guidance |
| **Proactivity** | Reactive only | Proactive query execution |
| **Intelligence** | Basic responses | Context-aware decisions |

---

## 🆚 Model Comparison

| Feature | Ollama (Local) | OpenAI API |
|---------|----------------|------------|
| **Privacy** | ✅ Complete | ⚠️ Data sent to OpenAI |
| **Cost** | ✅ Free | 💰 Pay per usage |
| **Speed** | ⚡ Hardware dependent | ⚡ Generally fast |
| **Setup** | 🔧 Requires local installation | 🔑 Just need API key |
| **Offline** | ✅ Works offline | ❌ Requires internet |
| **Models** | 🎯 Open source models | 🚀 Latest GPT models |

Choose the option that best fits your privacy, cost, and performance requirements!

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

We welcome contributions! Feel free to:
- Report bugs
- Suggest new features  
- Submit pull requests
- Improve documentation

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the documentation
- Review the example configurations

**Happy querying! 🚀**
## ⚙️ Advanced Configuration & Optimization

### 🎛️ Fine-tuning Agent Behavior

The agent behavior can be customized by modifying parameters in `app.py`. Here are key settings that affect performance:

#### `prevent_hallucinations` Parameter

```python
prevent_hallucinations=False  # Current default setting
```

**When to use `prevent_hallucinations=True`:**
- ✅ **Ollama models** (llama3.1, llama3.2, codellama) - Often provide better, more focused responses
- ✅ **Production environments** - Ensures more predictable behavior
- ✅ **When accuracy is critical** - Reduces creative but potentially incorrect responses
- ✅ **Smaller or less capable models** - Helps maintain focus on database tasks

**When to use `prevent_hallucinations=False`:**
- ✅ **OpenAI models** (gpt-4o-mini, gpt-4o) - Generally perform well with more flexibility
- ✅ **Development/testing** - Allows more creative problem-solving approaches
- ✅ **Complex queries** - May help with nuanced database analysis
- ✅ **When you want more conversational responses**

### 🔧 Model-Specific Recommendations

#### For Ollama Models:
```python
# In create_agent() function, consider using:
prevent_hallucinations=True,  # More focused responses
temperature=0.1,              # Lower temperature for consistency
```

#### For OpenAI Models:
```python
# Current settings work well:
prevent_hallucinations=False, # Allows flexibility
temperature=0.1,              # Good balance
```

### 🎯 Troubleshooting Poor Responses

If you're experiencing poor quality responses:

1. **Try different models:**
   ```bash
   # For Ollama - try these models:
   ollama pull llama3.2        # Often better than 3.1 for structured tasks
   ollama pull codellama       # Specialized for code/SQL
   ollama pull mistral         # Good alternative
   ```

2. **Adjust `prevent_hallucinations`:**
   ```python
   # Edit app.py, line ~75:
   prevent_hallucinations=True  # Try this for Ollama models
   ```

3. **Modify temperature settings:**
   ```python
   # For more consistent responses:
   temperature=0.05  # Very focused
   
   # For more creative responses:
   temperature=0.3   # More flexible
   ```

4. **Switch to OpenAI temporarily:**
   ```env
   MODEL_PROVIDER=openai
   MODEL_NAME=gpt-4o-mini
   ```

### 📊 Model Performance Comparison

Based on testing with SQL tasks:

| Model | Best Settings | Performance | Notes |
|-------|---------------|-------------|-------|
| **gpt-4o-mini** | `prevent_hallucinations=False`, `temp=0.1` | ⭐⭐⭐⭐⭐ | Excellent for SQL tasks |
| **gpt-4o** | `prevent_hallucinations=False`, `temp=0.1` | ⭐⭐⭐⭐⭐ | Best overall, but expensive |
| **llama3.2** | `prevent_hallucinations=True`, `temp=0.1` | ⭐⭐⭐⭐ | Good with proper settings |
| **llama3.1** | `prevent_hallucinations=True`, `temp=0.05` | ⭐⭐⭐ | Can be inconsistent |
| **codellama** | `prevent_hallucinations=True`, `temp=0.1` | ⭐⭐⭐⭐ | Great for SQL structure queries |

### 🛠️ Custom Configuration Example

Create a custom configuration for your specific use case:

```python
def create_agent():
    model = create_model()
    
    # Custom settings based on your model choice
    if model_provider == 'ollama':
        hallucination_prevention = True
        temp_setting = 0.05
    else:  # OpenAI
        hallucination_prevention = False
        temp_setting = 0.1
    
    sql_agent = Agent(
        tools=[SQLTools(db_url=db_url)],
        model=model,
        add_history_to_messages=True,
        num_history_responses=10,
        prevent_hallucinations=hallucination_prevention,  # Dynamic setting
        # ... rest of configuration
    )
```

### 💡 Pro Tips

1. **Test with your specific database:** Different models may perform better with different database structures
2. **Monitor response quality:** Keep track of which settings work best for your use case
3. **Consider hybrid approach:** Use OpenAI for complex analysis, Ollama for simple queries
4. **Adjust based on hardware:** More powerful hardware may handle higher temperatures better

### 🚨 Known Issues & Solutions

**Issue: Ollama models giving poor responses**
```bash
# Solution: Try these steps in order:
1. Set prevent_hallucinations=True in app.py
2. Lower temperature to 0.05
3. Try llama3.2 instead of llama3.1
4. Switch to codellama for SQL-heavy tasks
```

**Issue: Responses too verbose or unfocused**
```python
# Solution: Increase constraints
prevent_hallucinations=True
temperature=0.05
max_tokens=500  # Limit response length
```

**Issue: Responses too rigid or unhelpful**
```python
# Solution: Increase flexibility
prevent_hallucinations=False
temperature=0.2
```