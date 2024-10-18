import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.runnables.base import RunnableSequence
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import requests

# Load environment variables from .env file
load_dotenv()

# Streamlit UI
st.title("Domain Specific QA System")

# Sidebar for user to enter their OpenAI API key
st.sidebar.header("API Key Configuration")
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

# Function to fetch domain-specific content (medical, legal, finance)
def fetch_content(query, domain="medical"):
    if domain == "medical":
        url = f"https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/?term={query}&retmode=text"
    elif domain == "legal":
        url = f"https://api.openlegaldata.io/legal/?query={query}"
    elif domain == "finance":
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&keywords={query}&apikey=T7057FKJ25MO5JPY"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"

# Function to generate the answer using OpenAI LLM
def get_answer(query, domain="medical"):
    context = fetch_content(query, domain=domain)

    # Limit the context length to avoid exceeding token limits
    max_context_length = 2000  # Set a reasonable limit
    if len(context) > max_context_length:
        context = context[:max_context_length]  # Truncate the context

    # Use gpt-4o model
    llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=openai_api_key)
    prompt_template = PromptTemplate(
        input_variables=["context", "query"],
        template=( 
            "You are an expert in {context}. Based on the following context, provide an accurate response to the query:\n\n"
            "Context: {context}\n"
            "Query: {query}\n\n"
            "Answer:"
        ),
    )
    
    # Create a sequence using RunnableSequence
    llm_chain = RunnableSequence(prompt_template | llm)
    response = llm_chain.invoke({"context": context, "query": query})
    
    # Extract the answer from the response object
    answer = response.content
    
    return answer

# Function to fine-tune the prompt based on the user query
def fine_tune_prompt(query, context, domain="medical"):
    return (
        f"You are an expert in the {domain} domain. Using the following information, provide a clear and accurate answer to the question:\n\n"
        f"Context: {context}\n\n"
        f"Question: {query}\n\n"
        "Answer:"
    )

# Main function to run the QA system
def run_qa_system(query, domain="medical"):
    answer = get_answer(query, domain)
    return answer

# User input for the query
query = st.text_input("Enter your question:")
domain = st.selectbox("Select the domain:", ["medical", "legal", "finance"])

if st.button("Get Answer"):
    if query:  # Check if query is provided
        if openai_api_key:  # Check if API key is provided
            answer = run_qa_system(query, domain)
            st.write(f"**Answer:** {answer}")
        else:
            st.warning("Please enter your OpenAI API key.")
    else:
        st.warning("Please enter a question.")
