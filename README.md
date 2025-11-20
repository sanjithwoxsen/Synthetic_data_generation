# Synthetic Data Generator

A powerful AI-driven application that generates synthetic question-answer datasets from PDF documents using advanced language models and vector embeddings.

## 🌟 Features

- **PDF Document Processing**: Upload multiple PDF files and extract content automatically
- **Intelligent Context Retrieval**: Uses FAISS vector store for efficient similarity search
- **AI-Powered Question Generation**: Generates relevant questions based on document context
- **Automated Answer Generation**: Creates accurate answers using Ollama's LLaMA models
- **Customizable Output**: Configure number of questions and answer types (one-word, short, or long)
- **Custom Conditions**: Add specific rules and conditions for LLM generation
- **Interactive Web Interface**: Built with Streamlit for easy interaction
- **CSV Export**: Download generated datasets as CSV files
- **Progress Tracking**: Real-time progress bar for answer generation

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.9 or higher
- [Ollama](https://ollama.ai/) with LLaMA 3.1 model
- Google Gemini API key

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sanjithwoxsen/Synthetic_data_generation.git
cd Synthetic_data_generation
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama and Download LLaMA Model

Follow the [Ollama installation guide](https://ollama.ai/) for your operating system, then pull the required model:

```bash
ollama pull llama3.1
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

To get a Google Gemini API key, visit [Google AI Studio](https://makersuite.google.com/app/apikey).

## 💻 Usage

### Running Locally

Start the Streamlit application:

```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`.

### Using the Application

1. **Upload PDF Files**: Drag and drop or select one or more PDF files
2. **Enter Topic Name**: Specify the topic for question generation
3. **Configure Settings**:
   - Number of Questions (5-100)
   - Answer Type (One-word, Short, or Long)
   - Custom Conditions (optional)
4. **Generate**: Click the "Generate" button to create your synthetic dataset
5. **Download**: Preview and download the generated CSV file

## 🐳 Docker Deployment

### Build the Docker Image

```bash
docker build -t synthetic-data-generator .
```

### Run the Docker Container

```bash
docker run -p 8501:8501 --env-file .env synthetic-data-generator
```

Access the application at `http://localhost:8501`.

## 📁 Project Structure

```
Synthetic_data_generation/
├── main.py              # Streamlit frontend application
├── backend.py           # Core logic for data processing and generation
├── frontend.py          # Alternative frontend implementation
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── logo.jpeg           # Application logo
├── .env                # Environment variables (not in repo)
├── csv/                # Generated CSV files storage
├── faiss_index/        # FAISS vector store
└── log/                # Retrieval logs
```

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)**: Web interface framework
- **[Ollama](https://ollama.ai/)**: Local LLM inference with LLaMA 3.1
- **[Google Generative AI](https://ai.google.dev/)**: Text embeddings (text-embedding-004)
- **[LangChain](https://www.langchain.com/)**: Text splitting and vector store management
- **[FAISS](https://github.com/facebookresearch/faiss)**: Efficient similarity search
- **[PyPDF2](https://pypdf2.readthedocs.io/)**: PDF text extraction
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation and CSV generation

## 🔧 Configuration

### Model Selection

You can change the LLM model in `backend.py`:

```python
MODEL_NAME = "llama3.1"  # or "llama3.2"
```

### Text Chunking Parameters

Adjust chunk size and overlap in the `Database` class:

```python
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
```

## 📝 Output Format

The generated CSV file contains two columns:

- **Question**: The generated question
- **Answer**: The corresponding answer

Example:
```csv
Question,Answer
"What is machine learning?","Machine learning is a subset of artificial intelligence..."
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is available for educational and research purposes.

## 👤 Author

**Sanjith**
- GitHub: [@sanjithwoxsen](https://github.com/sanjithwoxsen)

## 🙏 Acknowledgments

- Ollama team for the LLaMA models
- Google AI for Generative AI APIs
- LangChain community for the excellent tooling

## ⚠️ Notes

- Ensure Ollama is running before starting the application
- Large PDF files may take longer to process
- The quality of generated questions depends on the input document quality
- An active internet connection is required for Google embeddings API

---

For issues, questions, or suggestions, please open an issue on GitHub.
