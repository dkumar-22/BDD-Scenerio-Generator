import os
import re
import json
import numpy as np
import argparse
from typing import List, Dict, Any, Optional, Tuple

# Required libraries (install with pip)
# pip install pypdf langchain langchain-community langchain-google-genai faiss-cpu python-dotenv

from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from dotenv import load_dotenv

# Load environment variables (API keys)
load_dotenv()

class SmartRAGAgent:
    """Smart RAG Agent for Software Design Documents
    
    This agent uses vector embeddings to provide intelligent question answering
    and BDD scenario generation based on a software design document PDF.
    """
    
    def __init__(self, pdf_path: str, model_name: str = "gemini-1.5-flash"):
        """Initialize the Smart RAG Agent
        
        Args:
            pdf_path: Path to the software design document PDF
            model_name: Google Generative AI model to use (default: gemini-1.5-flash)
        """
        self.pdf_path = pdf_path
        self.model_name = model_name
        self.llm = None
        self.embeddings = None
        self.vectorstore = None
        self.qa_chain = None
        self.bdd_chain = None
        self.document_text = ""
        
        # Validate API key
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in environment. Please set it.")
            
        print(f"Initializing Smart RAG Agent with {pdf_path}")
        
    def setup(self):
        """Set up the RAG agent components"""
        # Extract text from PDF
        self._extract_pdf_text()
        
        # Initialize embedding model
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(model=f"models/{self.model_name}", 
                                          temperature=0.2,
                                          top_p=0.95,
                                          convert_system_message_to_human=True)
        
        # Create vector database
        self._create_vector_db()
        
        # Set up QA and BDD chains
        self._setup_chains()
        
        print("Smart RAG Agent setup complete!")
    
    def _extract_pdf_text(self):
        """Extract text from the PDF document"""
        print(f"Extracting text from {self.pdf_path}...")
        
        try:
            pdf_reader = PdfReader(self.pdf_path)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            self.document_text = text
            print(f"Extracted {len(text)} characters from PDF")
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def _create_vector_db(self):
        """Create vector database from document chunks"""
        print("Creating vector database...")
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(self.document_text)
        print(f"Split document into {len(chunks)} chunks")
        
        # Create vector store
        try:
            self.vectorstore = FAISS.from_texts(chunks, self.embeddings)
            print("Vector database created successfully")
        except Exception as e:
            raise Exception(f"Error creating vector database: {str(e)}")
    
    def _setup_chains(self):
        """Set up the QA and BDD scenario generation chains"""
        print("Setting up QA and BDD generation chains...")
        
        # QA Chain setup
        qa_prompt_template = """You are an expert in software design documents, acting as a smart agent to provide accurate information.
        Answer the user's question based on the retrieved context from the software design document.
        If you don't know the answer based on the context, say so clearly without making up information.
        
        Context from the design document:
        {context}
        
        Question: {question}
        
        Answer:"""
        
        qa_prompt = PromptTemplate(
            template=qa_prompt_template,
            input_variables=["context", "question"]
        )
        
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        
        self.qa_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | qa_prompt
            | self.llm
        )
        
        # BDD Chain setup
        bdd_prompt_template = """You are an expert in behavior-driven development (BDD) and software design documents.
        Generate detailed BDD scenarios in Gherkin syntax based on the context from a software design document.
        Focus on creating scenarios that validate the core functionality described in the document.
        
        Context from the design document:
        {context}
        
        Feature or component to create BDD scenarios for: {feature}
        
        Generate 3-5 BDD scenarios in proper Gherkin format (Feature, Scenario, Given, When, Then) that test the functionality of this component or feature:"""
        
        bdd_prompt = PromptTemplate(
            template=bdd_prompt_template,
            input_variables=["context", "feature"]
        )
        
        self.bdd_chain = (
            {"context": retriever, "feature": RunnablePassthrough()}
            | bdd_prompt
            | self.llm
        )
        
        print("Chains set up successfully")
    
    def answer_question(self, question: str) -> str:
        """Answer a question about the software design document
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the question based on the document context
        """
        if not self.qa_chain:
            raise ValueError("Agent not set up. Call setup() first.")
        
        print(f"Answering question: {question}")
        response = self.qa_chain.invoke(question)
        
        # Extract content from LangChain response
        if hasattr(response, 'content'):
            return response.content
        return str(response)
    
    def generate_bdd_scenarios(self, feature: str) -> str:
        """Generate BDD scenarios for a feature or component
        
        Args:
            feature: The feature or component to generate scenarios for
            
        Returns:
            BDD scenarios in Gherkin format
        """
        if not self.bdd_chain:
            raise ValueError("Agent not set up. Call setup() first.")
        
        print(f"Generating BDD scenarios for: {feature}")
        response = self.bdd_chain.invoke(feature)
        
        # Extract content from LangChain response
        if hasattr(response, 'content'):
            return response.content
        return str(response)

    def save_vector_db(self, path: str = "vectorstore.faiss"):
        """Save the vector database for future use
        
        Args:
            path: Directory path to save the database
        """
        if not self.vectorstore:
            raise ValueError("Vector database not created. Call setup() first.")
        
        # Save the vector store
        self.vectorstore.save_local(path)
        print(f"Vector database saved to {path}")
    
    @classmethod
    def load_from_saved(cls, pdf_path: str, vector_db_path: str, model_name: str = "gemini-1.5-flash"):
        """Load a RAG agent from a saved vector database
        
        Args:
            pdf_path: Path to the original PDF (for reference)
            vector_db_path: Path to the saved vector database
            model_name: Google Generative AI model to use
            
        Returns:
            Initialized SmartRAGAgent
        """
        agent = cls(pdf_path, model_name)
        
        # Extract text (needed for reference)
        agent._extract_pdf_text()
        
        # Initialize embedding model
        agent.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Initialize LLM
        agent.llm = ChatGoogleGenerativeAI(model=f"models/{model_name}", 
                                          temperature=0.2,
                                          top_p=0.95,
                                          convert_system_message_to_human=True)
        
        # Load the vector database
        agent.vectorstore = FAISS.load_local(vector_db_path, agent.embeddings)
        print(f"Loaded vector database from {vector_db_path}")
        
        # Set up the chains
        agent._setup_chains()
        
        return agent

# Interactive CLI
def main():
    parser = argparse.ArgumentParser(description="Smart RAG Agent for Software Design Documents")
    parser.add_argument("--pdf", required=True, help="Path to the software design document PDF")
    parser.add_argument("--model", default="gemini-1.5-flash", help="Google Generative AI model to use")
    parser.add_argument("--save_db", action="store_true", help="Save the vector database for future use")
    parser.add_argument("--load_db", help="Load a previously saved vector database")
    
    args = parser.parse_args()
    
    try:
        # Create or load agent
        if args.load_db:
            agent = SmartRAGAgent.load_from_saved(args.pdf, args.load_db, args.model)
        else:
            agent = SmartRAGAgent(args.pdf, args.model)
            agent.setup()
            
            # Save vector DB if requested
            if args.save_db:
                agent.save_vector_db()
        
        # Interactive loop
        print("\n=== Smart RAG Agent Interactive Mode ===")
        print("Type 'exit' to quit")
        print("Start a query with 'bdd:' to generate BDD scenarios")
        print("====================================\n")
        
        while True:
            user_input = input("Enter your query: ")
            
            if user_input.lower() == 'exit':
                break
                
            if user_input.lower().startswith('bdd:'):
                feature = user_input[4:].strip()
                response = agent.generate_bdd_scenarios(feature)
                print("\n=== BDD Scenarios ===")
                print(response)
                print("===================\n")
            else:
                response = agent.answer_question(user_input)
                print("\n=== Answer ===")
                print(response)
                print("==============\n")
                
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    main()