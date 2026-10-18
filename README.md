🚀 Getting Started
1. Prerequisites
Clone the repository and navigate into the workspace:

Bash
git clone [https://github.com/WoWVaquas/HF-Agentic-AI-Unit3-RAG.git](https://github.com/WoWVaquas/HF-Agentic-AI-Unit3-RAG.git)
cd HF-Agentic-AI-Unit3-RAG
2. Environment Setup
Create a virtual environment and activate it:

Bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
Install the dependencies:

Bash
pip install -r "Unit 3 Agentic RAG/requirement.txt"
3. API Token Configuration
Create a .env file in the root directory and add your Hugging Face API token:

Plaintext
HF_TOKEN=your_huggingface_token_here
4. Running the Agent
Run the application from your terminal:

Bash
python "Unit 3 Agentic RAG/app.py"
🛠️ Built With
LangGraph: ReAct agent graph orchestration

LangChain Community: Tooling & retriever abstraction

Hugging Face Datasets: Gala guest invitee dataset

Llama 3.1 8B Instruct: Model endpoint for reasoning & tool execution