import streamlit as st
import os

# 1. Text Splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 2. Vector Store
from langchain_community.vectorstores import FAISS

# 3. Embeddings (Free local model)
from langchain_huggingface import HuggingFaceEmbeddings

# 4. Google Gemini
from langchain_google_genai import ChatGoogleGenerativeAI

# --- CONFIGURATION ---
# We rely on st.secrets for keys

# --- HELPER FUNCTIONS ---
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(text)

def get_vectorstore(text_chunks):
    # Uses local CPU to convert text to numbers (Free)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)

def get_contextual_response(question, vectorstore, chat_history):
    # 1. Search for relevant text in the curriculum
    docs = vectorstore.similarity_search(question, k=3)
    context_text = "\n\n".join([doc.page_content for doc in docs])
    
    # 2. Format the Chat History
    history_text = ""
    for msg in chat_history[-4:]: 
        role = "User" if msg["role"] == "user" else "AI"
        history_text += f"{role}: {msg['content']}\n"
    
    # 3. Create the Contextual Prompt
    prompt = f"""
    You are a helpful academic advisor for the Computer Science department.
    
    INSTRUCTIONS:
    1. Answer the user's question based on the Curriculum Context below.
    2. If the answer is not in the context, say you don't know.
    3. Keep answers concise and helpful.
    
    --- CHAT HISTORY ---
    {history_text}
    
    --- CURRICULUM CONTEXT ---
    {context_text}
    
    --- USER QUESTION ---
    {question}
    
    ANSWER:
    """
    
    # 4. Call Gemini 1.5 Flash
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.3,
        google_api_key=st.secrets["GOOGLE_API_KEY"]
    )
    
    # Generate response
    response = llm.invoke(prompt)
    return response.content

def initialize_vectorstore():
    """
    Auto-loads the 'curriculum_data.txt' file.
    """
    if "vectorstore" not in st.session_state or st.session_state.vectorstore is None:
        try:
            with st.spinner("Loading Curriculum Brain..."):
                with open("curriculum_data.txt", "r", encoding="utf-8") as f:
                    raw_text = f.read()
                
                chunks = get_text_chunks(raw_text)
                st.session_state.vectorstore = get_vectorstore(chunks)
                st.success("System Ready!")
        except FileNotFoundError:
            st.error("CRITICAL ERROR: 'curriculum_data.txt' not found.")
            st.stop()

# --- MAIN APP ---
def main():
    st.set_page_config(page_title="CS Assistant", page_icon="🎓")
    st.title("🎓 CS Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    initialize_vectorstore()

    # Display History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input Area
    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_contextual_response(prompt, st.session_state.vectorstore, st.session_state.messages)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == '__main__':
    main()