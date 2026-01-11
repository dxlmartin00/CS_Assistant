# 🎓 CS Dept. Curriculum Chatbot (RAG System)

A Contextual AI Assistant built for the **Bachelor of Science in Computer Science** curriculum.
This project uses **Retrieval-Augmented Generation (RAG)** to provide accurate, source-based answers to student inquiries regarding subjects, units, and prerequisites.

## 🚀 Features
* **Contextual Memory:** Remembers previous questions in the conversation (e.g., "How many units is it?").
* **RAG Architecture:** Searches a specific curriculum database (`curriculum_data.txt`) to prevent hallucinations.
* **Powered by Google Gemini:** Uses the efficient **Gemini 2.5 Flash Lite** model for fast, logical reasoning.
* **Streamlit UI:** Simple, clean, and responsive chat interface.

## 🛠️ Tech Stack
* **Framework:** Streamlit
* **Language:** Python 3.10+
* **LLM Engine:** Google Gemini (`gemini-2.5-flash-lite`)
* **Embeddings:** Hugging Face (`all-MiniLM-L6-v2`) via `sentence-transformers`
* **Vector Database:** FAISS (Facebook AI Similarity Search)

## 📂 Project Structure
```text
cs_chatbot/
├── .streamlit/
│   └── secrets.toml       # API Keys (Google Gemini) - NOT uploaded to Git
├── app.py                 # Main application logic
├── curriculum_data.txt    # The knowledge base (Subjects, Units, Pre-reqs)
├── requirements.txt       # Python dependencies
└── README.md              # Project Documentation
```

## ⚙️ Installation & Setup
# 1. Clone the Repository
```
git clone [https://github.com/your-username/cs-curriculum-bot.git](https://github.com/your-username/cs-curriculum-bot.git)
cd cs-curriculum-bot
```
# 2. Create Virtual Environment

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# 3. Install Dependencies
```
pip install -r requirements.txt
```

# 4. Configure Secrets
Create a folder .streamlit and a file secrets.toml inside it:

Ini, TOML

    .streamlit/secrets.toml
GOOGLE_API_KEY = "AIzaSyD-YourActualGoogleKeyHere"

# 5. Run the App
```
streamlit run app.py
```

## 🧠 How it Works

* Ingestion: The app reads curriculum_data.txt and splits it into small text chunks.

* Embedding: It converts these chunks into numerical vectors using all-MiniLM-L6-v2.

* Retrieval: When a user asks a question, the system finds the top 3 most relevant text chunks.

* Generation: It sends the User Question + Relevant Chunks + Chat History to Gemini 2.0 Flash Lite.

* Response: The AI generates a factual answer based only on the provided context.

## 📝 License
This project is for educational purposes as part of the BS Computer Science undergraduate project.