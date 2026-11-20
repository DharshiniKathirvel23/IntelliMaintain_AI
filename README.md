# ⚙️ IntelliMaintain AI
### An Agentic AI-Powered Industrial Maintenance System

<p align="center">
  An intelligent AI-powered assistant for industrial equipment troubleshooting, maintenance investigation, and technical knowledge retrieval.
</p>

---

## 📌 About the Project

**IntelliMaintain AI** is a fully software-based industrial maintenance assistant that uses Agentic AI to support industrial troubleshooting and maintenance decision-making.

The system combines Hybrid Retrieval-Augmented Generation (Hybrid RAG), Context-Aware Generation (CAG), machine-specific memory, and multi-agent investigation to understand maintenance queries and generate context-aware responses.

It aims to make industrial maintenance support smarter, faster, and more efficient.

## 🎯 Project Objectives

- Provide intelligent industrial troubleshooting assistance.
- Retrieve relevant information from technical documents.
- Maintain machine-specific historical context.
- Investigate equipment problems using multiple AI agents.
- Generate context-aware maintenance recommendations.
- Improve access to industrial technical knowledge.

## 🚀 Key Features

1. **Hybrid RAG**
   - Retrieves relevant information from technical documents.
   - Improves the relevance of generated responses.

2. **Context-Aware Generation (CAG)**
   - Uses available contextual information.
   - Generates responses based on relevant equipment knowledge.

3. **Machine-Specific Memory**
   - Maintains machine-related historical information.
   - Supports context-aware maintenance investigations.

4. **Multi-Agent Investigation**
   - Uses multiple AI agents to investigate maintenance issues.
   - Supports structured problem analysis.

5. **Intelligent Troubleshooting**
   - Helps investigate possible equipment problems.
   - Provides maintenance-related insights and recommendations.

6. **Interactive Dashboard**
   - User-friendly interface developed using Streamlit.

## 🧠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | User interface |
| Gemini API | AI-powered responses |
| LangGraph | Multi-agent workflow |
| ChromaDB | Vector database |
| SQLite | Persistent data storage |
| Hybrid RAG | Technical knowledge retrieval |

## 🏗️ System Workflow

1. User enters an industrial maintenance query.
2. System identifies the relevant machine and context.
3. Hybrid RAG retrieves relevant technical information.
4. Machine-specific memory provides historical context.
5. Multiple AI agents investigate the maintenance problem.
6. Gemini generates a context-aware response.
7. Results are presented through the Streamlit interface.

## 📂 Project Structure

```text
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
├── test_cag.py
├── test_embedding.py
├── test_nexus.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### Module Description

| Module | Description |
|---|---|
| agents/ | Contains AI agents for fault detection, knowledge retrieval and recommendations |
| data/ | Stores machine data, manuals and ChromaDB information |
| rag/ | Handles document processing, retrieval and maintenance assistance |
| app.py | Main Streamlit application |
| config.py | Project configuration |
| database.py | Database operations |
| requirements.txt | Python dependencies |
| .gitignore | Excludes sensitive and unnecessary files |
```

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/DharshiniKathirvel23/IntelliMaintain_AI.git
```

### Step 2: Navigate to the Project

```bash
cd IntelliMaintain_AI
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Environment

For Windows:

```bash
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure the Gemini API Key

Create a `.env` file in the project root directory.

Add your API key:

```env
API_KEY=your_api_key_here
```

**Important:** Never upload your actual API key or `.env` file to GitHub.

### Step 7: Run the Application

```bash
streamlit run app.py
```

## 🔐 Security

- API credentials are stored in environment variables.
- Sensitive configuration files are excluded using `.gitignore`.
- API keys should never be committed to the public repository.

## 🌟 Expected Outcome

IntelliMaintain AI aims to provide an intelligent maintenance assistant that combines technical knowledge retrieval, machine-specific memory, and multi-agent investigation to support industrial maintenance activities.

## 🔮 Future Enhancements

- Advanced predictive maintenance analysis.
- Integration with additional industrial knowledge sources.
- Improved maintenance history and reporting.
- Enhanced multi-agent collaboration.

## 👩‍💻 Developer

**Dharshini K**

B.Tech – Information Technology

Vivekanandha College of Engineering for Women

## 📜 Project Information

**Project Name:** IntelliMaintain AI

**Domain:** Agentic Artificial Intelligence

**Application Type:** Software-Based Industrial Maintenance Assistant

---

⭐ If you find this project interesting, consider giving this repository a star!

