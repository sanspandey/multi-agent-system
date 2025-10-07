# 🧠 Multi-Agent System

 Overview

This project is a Multi-Agent AI System that automatically decides how to handle user queries using different specialized agents.
Each agent focuses on a specific information source — PDFs, web, or research papers (via Arxiv) — and the system intelligently combines their responses into a single, synthesized answer.

Agents Involved (Short Overview)

🧩 Decision Agent

Chooses which agents (PDF, Web, or Arxiv) should handle a user’s question.
Uses the Gemini model to understand query intent.

📄 PDF RAG Agent

Reads and searches uploaded PDFs.
Finds the most relevant sections using text extraction and retrieval techniques.

🌐 Web Search Agent

Collects fresh information from the internet.
Ideal for real-time or general questions.

📚 Arxiv Agent

Looks up academic papers from the Arxiv API.
Provides short summaries of scientific research.

🧠 Answer Synthesizer Agent

Merges all responses from other agents into one clear, well-written answer.
Removes duplicates and keeps the final response human-readable.

Controller (Main Brain)

The Controller connects all agents together.
It receives the user’s query and decides which agents to call (PDF, Web, Arxiv, etc.).
After collecting all their responses, it sends them to the Answer Synthesizer Agent to form one final clean answer.
It works like a manager — coordinating the entire multi-agent workflow.

How It Works

1. User uploads a PDF (optional).
2. User asks a question in the UI.
3. The Decision Agent analyzes the query and chooses which agents to use.
4. Selected agents fetch relevant information.
5. The Answer Synthesizer merges everything into a final, clear answer.
6. The result is displayed on the frontend.

Frontend

A simple and elegant web interface built with:
HTML + CSS (modern, minimal UI)
JavaScript (fetch-based API calls)

Features:

PDF upload widget
Query input box
Auto-filled File ID
Formatted answer + agents used display

⚙️ Backend

Built with FastAPI and Uvicorn, providing endpoints:
/upload_pdf → Upload and process a PDF file
/ask → Handle query processing, agent decision, and answer synthesis

| Component             | Technology Used       |
| --------------------- | --------------------- |
| Backend Framework     | FastAPI               |
| AI Model              | Google Gemini 2.5 Pro |
| PDF Parsing           | PyMuPDF, pytesseract  |
| Web & Research Agents | Requests, Arxiv API   |
| Frontend              | HTML, CSS, JavaScript |
| Runtime               | Python 3.12           |


Installation

1. Clone this repo
   
git clone https://github.com/yourusername/multi_agent_system.git
cd multi_agent_system

2. Create a virtual environment

python -m venv env
env\Scripts\activate  # (Windows)

3. Install dependencies

pip install -r requirements.txt

4. Set your Gemini API key
   
set GEMINI_API_KEY=your_api_key_here

5. Run the server
   
uvicorn app.main:app --reload


Example

User Query:

“Show me the latest research about LLM engineering.”

System Response:
✅ Agents Used: arxiv, web
🧠 Final Answer:

Large Language Model (LLM) engineering involves optimizing model architecture, fine-tuning methods, and context handling. Recent papers focus on retrieval-augmented generation, instruction-following, and multi-modal fusion.

🧾 Folder Structure

backend/
 ├── app/
 │   ├── agent/
 │   │   ├── pdf_rag.py
 │   │   ├── web_search.py
 │   │   ├── arxiv_agent.py
 │   │   ├── decision_agent.py
 │   │   ├── answer_synthesizer.py
 │   │   └── controller.py
 │   ├── utils/
 │   │   └── pdf_utils.py
 │   ├── main.py
 ├── uploads/
frontend/
 ├── index.html
 └── app.js

💬 Future Enhancements

1. Add chat-style interface
2. Store chat history per user
3. Integrate voice input/output
4. Add more specialized agents (e.g., YouTube summarizer, GitHub data agent)

🧑‍💻 Author

Sanskar Pandey
💼 Developer — AI, FastAPI, and Multi-Agent Systems

📜 License

MIT License – see the LICENSE file for details.




