# 🏢 WDP Office Data Analytics - SQL AI Agent

An intelligent SQL assistant specifically customized for your WDP office data analysis needs. This application combines the power of AI with your office database to provide natural language querying capabilities.

![WDP Analytics](img.png)

## 🌟 Features

- **Natural Language Queries**: Ask questions in plain English
- **Multiple AI Models**: Support for Ollama and OpenAI models
- **Real-time SQL Execution**: Instant query results with explanations
- **Custom WDP Theme**: Professional blue/teal color scheme
- **Comprehensive Help System**: Built-in guidance and tutorials
- **Multiple Output Formats**: Tables, summaries, and raw data
- **Database Schema Explorer**: Easy navigation of your data structure

## 🚀 Quick Start

### 1. Prerequisites
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Ollama (if using local AI)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.1
```

### 2. Database Setup

#### Option A: Automatic Migration
```bash
# Run the migration script
python migrate_wdp.py
```

#### Option B: Manual Setup
1. Copy your WDP database file to this directory
2. Rename it to `wdp_office.db`
3. Update `.env` file:
```env
DB_URL=sqlite:///./wdp_office.db
MODEL_PROVIDER=ollama
MODEL_NAME=llama3.1
```

### 3. Launch the Application
```bash
chainlit run app.py
```

Visit `http://localhost:8000` to start analyzing your data!

## 💡 Usage Examples

### Natural Language Queries
```
"Show me all employees in the sales department"
"What's the total revenue for this quarter?"
"Find the top 10 customers by order value"
"How many projects are currently active?"
```

### Command Reference
- `/help` - Show comprehensive help guide
- `/schema` - Display database structure
- `/tables` - List all available tables
- `/run SELECT * FROM employees LIMIT 5` - Execute raw SQL
- `/raw [query]` - Get raw table output
- `/summary [query]` - Get summarized results

## 🎨 Customization

### Theme Colors
The application uses a professional WDP color scheme:
- **Primary**: #2E86AB (Ocean Blue)
- **Secondary**: #A23B72 (Magenta)
- **Accent**: #F18F01 (Orange)
- **Background**: #F8F9FA (Light Gray)

### Custom Styling
Modify `public/style.css` to customize:
- Colors and gradients
- Table styling
- Button designs
- Layout and spacing

## 🔧 Configuration

### Environment Variables
```env
# Database Configuration
DB_URL=sqlite:///./wdp_office.db

# AI Model Configuration
MODEL_PROVIDER=ollama  # or 'openai'
MODEL_NAME=llama3.1    # or gpt-4, gpt-3.5-turbo

# OpenAI API Key (if using OpenAI)
OPENAI_API_KEY=your_api_key_here
```

### Chainlit Configuration
Edit `chainlit.toml` for:
- Application name and description
- Port settings
- UI preferences
- Feature toggles

## 📊 Database Integration

### Supported Database Types
- **SQLite** (recommended for development)
- **PostgreSQL** (recommended for production)
- **MySQL**
- **Microsoft SQL Server**

### Connection Examples
```env
# SQLite
DB_URL=sqlite:///./wdp_office.db

# PostgreSQL
DB_URL=postgresql://username:password@localhost:5432/wdp_database

# MySQL
DB_URL=mysql://username:password@localhost:3306/wdp_database
```

## 🛠️ Development

### Project Structure
```
├── app.py                 # Main application
├── chainlit.toml         # UI configuration
├── migrate_wdp.py        # Database migration helper
├── requirements.txt      # Python dependencies
├── public/
│   └── style.css        # Custom styling
└── agents_tools/
    ├── flexible_sql_tool.py
    └── raw_sql_executor.py
```

### Adding New Features
1. **Custom Commands**: Add new commands in the `@cl.on_message` handler
2. **Styling**: Modify `public/style.css` for visual changes
3. **Database Tools**: Extend the `agents_tools/` modules

## 🔍 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check database file exists
ls -la *.db

# Test connection manually
python -c "import sqlite3; conn = sqlite3.connect('wdp_office.db'); print('OK')"
```

**AI Model Not Responding**
```bash
# For Ollama
ollama list
ollama pull llama3.1

# Check if Ollama is running
curl http://localhost:11434/api/tags
```

**Port Already in Use**
```bash
# Change port in chainlit.toml
port = 8001

# Or kill existing process
lsof -ti:8000 | xargs kill -9
```

## 📈 Advanced Features

### Data Analysis Capabilities
- **Trend Analysis**: "Show me sales trends over the last 6 months"
- **Aggregations**: "Calculate average order value by customer segment"
- **Joins**: "Show customer orders with product details"
- **Filtering**: "Find all overdue projects"

### Export Options
- Copy query results to clipboard
- Download as CSV (coming soon)
- Generate reports (coming soon)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

Need help? Here are your options:

1. **Built-in Help**: Type `/help` in the application
2. **Documentation**: Check this README
3. **Issues**: Open a GitHub issue
4. **Migration**: Run `python migrate_wdp.py` for database setup help

---

**🎯 Ready to explore your WDP office data with AI-powered analytics!**
