# Domain Specific Q&A System

This Domain-Specific QA System is a Streamlit-based application that leverages advanced NLP techniques and the GPT-4o model to provide accurate answers to user queries across medical, legal, and financial domains.

Check out the app here: 

## Features
- **Domain-Specific Querying**: Supports queries in medical, legal, and financial domains.
- **GPT-4o Integration**: Utilizes OpenAI's powerful GPT-4o model for generating human-like responses.
- **Dynamic Content Retrieval**: Fetches up-to-date information from domain-specific APIs.
- **User-Friendly Interface**: Built with Streamlit for an intuitive and interactive user experience.

## NLP Techniques Demonstrated
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Fine-Tuning Strategies
- Prompt Engineering
- Domain-Specific Applications

## Tech Stack
- **Python**: Primary programming language
- **Streamlit**: Web application framework
- **Langchain**: For building and fine-tuning language models
- **OpenAI API**: For accessing the GPT-4o model
- **FAISS**: For efficient similarity search and clustering
- **Requests**: For API interactions

## Setup and Installation
1. Install required dependencies:
```bash
pip install -r requirement.txt
```

2. Set up your OpenAI API key in a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

## How It Works
1. User inputs a question and selects a domain (medical, legal, or finance).
2. The system fetches relevant content from domain-specific APIs.
3. The GPT-4o model processes the query and context to generate an answer.
4. The answer is displayed to the user through the Streamlit interface.
