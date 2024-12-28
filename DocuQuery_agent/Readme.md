# PDF and Web Search Agent with Memory  

This project is an intelligent query-answering system built using the **Phidata** framework. The system is capable of retrieving answers from PDF documents and web searches while maintaining conversational context using memory.

---

## Features  
- **PDF Document Search**: Upload PDF documents to create a searchable knowledge base.  
- **Web Search Integration**: Retrieve information from the web when the answer isn't found in the PDFs.  
- **Conversational Memory**: Maintain the context of conversations to provide coherent and relevant answers.  
- **Agentic AI System**: Combines natural language understanding with knowledge retrieval for dynamic query resolution.  

---

## Prerequisites  
Before running the project, ensure the following are installed:  
- Python 3.10 or higher
- Dependencies from `requirements.txt`  

---

## Configure Environment  
Add the key values in `.env` file:
```dotenv
QDRANT_API_KEY=
QDRANT_URL=
OPENAI_API_KEY=
PHI_API_KEY=