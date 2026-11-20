# ⚙️ IntelliMaintain AI
### An Agentic AI-Powered Industrial Maintenance System

<p align="center">
  <b>Intelligent Maintenance | Hybrid RAG | Multi-Agent AI | Machine-Specific Memory</b>
</p>

---

## 📌 About the Project

**IntelliMaintain AI** is an Agentic AI-powered industrial maintenance assistant designed to support equipment troubleshooting, technical knowledge retrieval, and intelligent maintenance decision-making.

The system integrates Hybrid Retrieval-Augmented Generation (Hybrid RAG), Context-Aware Generation (CAG), machine-specific memory, and multi-agent investigation to provide context-aware responses to industrial maintenance problems.

Unlike traditional maintenance support systems, IntelliMaintain AI combines AI-powered knowledge retrieval and collaborative agent workflows to investigate equipment-related issues and generate relevant maintenance recommendations.

## 🎯 Project Objectives

- Develop an intelligent industrial maintenance assistant.
- Simplify industrial equipment troubleshooting.
- Retrieve relevant technical information from maintenance manuals.
- Maintain machine-specific historical information.
- Implement multi-agent investigation for maintenance problems.
- Generate context-aware maintenance recommendations.
- Improve accessibility to industrial technical knowledge.

## 🚀 Key Features

### 1. Hybrid Retrieval-Augmented Generation (Hybrid RAG)
- Retrieves relevant information from industrial technical documents.
- Uses document processing and retrieval.
- Provides knowledge-grounded responses.

### 2. Context-Aware Generation (CAG)
- Uses relevant contextual information to improve response generation.
- Supports context-aware maintenance assistance.

### 3. Machine-Specific Memory
- Maintains machine-related information.
- Supports historical context during maintenance investigations.
- Helps provide machine-specific responses.

### 4. Multi-Agent Investigation
The system includes specialized AI agents:

- **Fault Agent:** Supports investigation of equipment faults.
- **Knowledge Agent:** Retrieves relevant technical knowledge.
- **Recommendation Agent:** Generates maintenance-related recommendations.

### 5. Intelligent Maintenance Assistant
- Accepts industrial maintenance queries.
- Combines retrieved knowledge and machine context.
- Generates AI-powered troubleshooting assistance.

### 6. Interactive User Interface
- Built using Streamlit.
- Provides an interactive interface for maintenance queries and AI responses.

## 🧠 System Architecture

IntelliMaintain AI follows a multi-stage intelligent maintenance workflow.

1. **User Input:** The user submits an industrial maintenance query.
2. **Machine Identification:** The system identifies the relevant machine context.
3. **Knowledge Retrieval:** Hybrid RAG retrieves relevant technical information.
4. **Context Processing:** CAG and machine-specific memory provide contextual information.
5. **Multi-Agent Investigation:** Specialized agents investigate the maintenance problem.
6. **AI Response Generation:** The system generates a context-aware response.
7. **Output:** Maintenance insights and recommendations are presented through the Streamlit interface.

## 🏗️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive user interface |
| Gemini API | AI-powered response generation |
| LangGraph | Agent workflow orchestration |
| ChromaDB | Vector database and knowledge retrieval |
| SQLite | Persistent database storage |
| Hybrid RAG | Technical knowledge retrieval |
| CAG | Context-aware generation |

## 📂 Project Structure

```text
IntelliMaintain_AI/
│
├── agents/
│   ├── fault_agent.py
│   ├── knowledge_agent.py
│   ├── recommendation_agent.py
│   └── workflow.py
│
├── data/
│   ├── chroma_db/
│   ├── chroma_db_backup/
│   ├── manuals/
│   └── machine_memory.db
│
├── rag/
│   ├── document_processor.py
│   ├── maintenance_assistant.py
│   └── retriever.py
│
├── app.py
├── assign_machine_id.py
├── check_documents.py
├── check_models.py
├── config.py
├── database.py
│
├── test_cag.py
├── test_embedding.py
├── test_nexus.py
│
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

## 📁 Module Description

| Module | Description |
|---|---|
| agents/ | Contains specialized AI agents and workflow |
| fault_agent.py | Fault investigation agent |
| knowledge_agent.py | Technical knowledge agent |
| recommendation_agent.py | Maintenance recommendation agent |
| workflow.py | Agent workflow coordination |
| data/ | Stores machine data, manuals and vector database files |
| chroma_db/ | ChromaDB vector database |
| manuals/ | Industrial maintenance documents |
| machine_memory.db | Machine-specific memory storage |
| rag/ | Retrieval-Augmented Generation components |
| document_processor.py | Processes technical documents |
| maintenance_assistant.py | Maintenance assistant logic |
| retriever.py | Retrieves relevant technical information |
| app.py | Main Streamlit application |
| config.py | Application configuration |
| database.py | Database operations |
| requirements.txt | Python dependencies |

## ⚙️ Installation and Setup

Follow these steps to run IntelliMaintain AI locally.

### Step 1: Clone the Repository

```bash
git clone https://github.com/DharshiniKathirvel23/IntelliMaintain_AI.git
```

### Step 2: Navigate to the Project Directory

```bash
cd IntelliMaintain_AI
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure Environment Variables

Create a `.env` file in the project root directory.

Add the required API credentials according to the application's configuration.

Example:

```env
API_KEY=your_api_key_here
```

Replace the placeholder with your own API key.

**Security:** Never upload your `.env` file or API credentials to GitHub.

### Step 7: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🗄️ Database and Knowledge Storage

IntelliMaintain AI uses:

- **ChromaDB:** For storing and retrieving vector-based technical knowledge.
- **SQLite:** For persistent machine-specific information and database operations.
- **Maintenance Manuals:** For providing technical knowledge to the retrieval system.

## 🧪 Testing

The project includes testing and verification scripts:

- `test_cag.py`
- `test_embedding.py`
- `test_nexus.py`
- `check_documents.py`
- `check_models.py`

These scripts support testing and checking different components of the application.

## 🔐 Security

- Store API credentials in environment variables.
- Exclude `.env` from version control.
- Never expose private API keys or credentials.
- Avoid committing virtual environments and unnecessary generated files.

## 🌟 Expected Outcome

IntelliMaintain AI aims to provide a smart industrial maintenance assistant capable of combining technical knowledge retrieval, contextual memory, and multi-agent investigation to support equipment troubleshooting and maintenance decision-making.

## 🔮 Future Enhancements

- Enhanced predictive maintenance capabilities.
- Advanced equipment failure analysis.
- Expanded industrial technical knowledge base.
- Improved multi-agent collaboration.
- Advanced maintenance analytics and reporting.
- Integration with additional industrial maintenance data sources.

## 👩‍💻 Developer

**Dharshini K**

B.Tech – Information Technology

Vivekanandha College of Engineering for Women

## 📌 Project Information

| Category | Details |
|---|---|
| Project Name | IntelliMaintain AI |
| Domain | Agentic Artificial Intelligence |
| Application | Industrial Maintenance Assistant |
| Development Type | Software-Based |
| Programming Language | Python |
| Interface | Streamlit |
| AI Integration | Gemini API |
| Knowledge Retrieval | Hybrid RAG |
| Agent Framework | LangGraph |

---

## ⭐ Support

If you find this project interesting, consider giving this repository a star!

**IntelliMaintain AI – Making Industrial Maintenance Smarter with Agentic AI.**
