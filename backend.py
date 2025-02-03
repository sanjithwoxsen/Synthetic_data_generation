import os
from dotenv import load_dotenv
import ollama
from PyPDF2 import PdfReader
from google import generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import pandas as pd
from streamlit import progress

# Load Environment and Set API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Specify model
MODEL_NAME = "llama3.1"


# PDF Processing Class
class Database:
    def __init__(self, pdf_docs):
        self.pdf_docs = pdf_docs

    def _pdf_to_text(self):
        # Efficiently extract text from all pages in all PDF files
        self.text = "".join(
            page.extract_text()
            for pdf in self.pdf_docs
            for page in PdfReader(pdf).pages
        )

    def _text_to_chunks(self):
        # Split text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.chunks = text_splitter.split_text(self.text)

    def _vectorstore(self):
        # Save vectorized chunks for later retrieval
        vectorstore = FAISS.from_texts(self.chunks, embeddings)
        vectorstore.save_local("faiss_index")
        print("Vector embeddings saved")

    def store(self):
        self._pdf_to_text()
        self._text_to_chunks()
        self._vectorstore()


# Context Retrieval Class
class Context:
    def __init__(self, topic):
        self.topic = topic

    def redefine(self):
        prompt_redefine = f"""
        You are an assistant creating queries for vector database retrieval based on topics. Given the Topic: '{self.topic}',
        return only the clarified query.
        """
        redefined_response = ollama.generate(model=MODEL_NAME, prompt=prompt_redefine)
        self.clarified_query = redefined_response["response"]
        return self.clarified_query

    def retrieve_faiss(self, query):
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(query)
        pdf_docs = [doc.page_content for doc in docs]

        os.makedirs('log', exist_ok=True)
        with open("log/Retrieval_log.txt", "w") as file:
            file.write(f"Clarified Query: {query}\n")
            for i, pdf_doc in enumerate(pdf_docs, start=1):
                file.write(f"Document {i}: {pdf_doc}\n")
        return docs


# Question Generation Class
class QuestionGeneration:
    def __init__(self, context, num_questions, question_type, conditions):
        self.context = context
        self.num_questions = num_questions
        self.question_type = question_type
        self.conditions = conditions

    def generate(self):
        prompt = f"""
        Generate {self.num_questions} questions based on the context provided.

        Context: {self.context}
        Total Questions: {self.num_questions}
        Question Type: {self.question_type}
        Conditions: {self.conditions}

        Provide the questions without any numbering or introduction.
        """
        response = ollama.generate(model=MODEL_NAME, prompt=prompt)
        if MODEL_NAME == "llama3.2":
            questions = response["response"].split('\n\n')
        elif MODEL_NAME == "llama3.1":
            questions = response["response"].split('\n')

        print("Question generation successful")
        return len(questions), questions


# Answer Generation Class
class AnswerGeneration:
    def __init__(self, context, questions, question_type, conditions,percentage_text=None,progress_bar=None):
        self.context = context
        self.questions = questions
        self.question_type = question_type
        self.conditions = conditions
        self.progress_bar = progress_bar
        self.percentage_text = percentage_text

    def generate(self):
        answers = []
        for i, question in enumerate(self.questions):
            prompt = f"""
            Answer the question: {question} using the following context: {self.context}

            Answer Type: {self.question_type}
            Conditions: {self.conditions}

            Directly provide the answer, without any formatting or symbols.
            """
            response = ollama.generate(model=MODEL_NAME, prompt=prompt)
            answer = response["response"].replace('\n', ' ').replace('**', ' ')
            print(f"Q{i}: Answer generation successful")
            answers.append(answer)
            if self.progress_bar:
                progress =(i+1) /  len(self.questions)
                self.progress_bar.progress(progress)
                self.percentage_text.text(f"Progress: {int(progress * 100)}%")
        return answers


# Function to Convert Q&A to CSV
def create_csv(questions, answers, topic):
    os.makedirs('csv', exist_ok=True)  # Efficient folder creation

    # Create DataFrame and Save as CSV
    df = pd.DataFrame({'Question': questions, 'Answer': answers})
    file_path = f"csv/Synthetic_Dataset_{topic}.csv"
    df.to_csv(file_path, index=False)

    print(df.head())
    return file_path,df
