# SQL AI Agent 🤖

A powerful SQL AI agent built with Phi Data that helps you interact with your databases through natural language conversations. This project combines the power of LLMs with database operations to provide an intuitive interface for database queries.

## ✨ Features

- Natural language to SQL query conversion
- Interactive chat interface using Chainlit
- Secure database connection handling
- Context-aware conversation with history retention
- Error handling and graceful error messages
- Support for multiple SQL databases (MySQL, PostgreSQL, SQLite, etc.)
- Easy database configuration through connection URL

## 🛠️ Technology Stack

- **Phi Data**: Core AI agent functionality and tools
- **Groq**: LLM integration using the llama-3.3-70b-versatile model
- **Chainlit**: Web-based chat interface
- **SQLAlchemy**: SQL toolkit and ORM
- **Database Connectors**: 
  - PyMySQL for MySQL
  - psycopg2 for PostgreSQL
  - Other SQLAlchemy-supported databases
- **Python-dotenv**: Environment variable management

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- A SQL database (MySQL, PostgreSQL, SQLite, etc.)
- Groq API key

### Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your credentials:
```env
GROQ_API_KEY=your_groq_api_key
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

## 💡 Usage

Once the application is running, you can:
1. Open your browser and navigate to the provided Chainlit URL
2. Start chatting with the AI agent using natural language
3. Ask questions about your database and get detailed responses
4. View the SQL queries used to retrieve the information

Example queries:
- "Show me all tables in the database"
- "What are the top 10 records from users table?"
- "How many orders were placed last month?"

## ⚠️ Error Handling

The application includes robust error handling for:
- Missing API keys
- Database connection issues
- Invalid queries
- Session management errors

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contact

For any questions or concerns, please open an issue in the repository.

---
Made with ❤️ using Phi Data and Chainlit
