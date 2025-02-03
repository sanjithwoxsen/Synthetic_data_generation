import streamlit as st
import PyPDF2
import pandas as pd
import os

# Function to extract text from the uploaded PDF
def extract_pdf_content(file):
    reader = PyPDF2.PdfReader(file)
    content = ""
    for page_num in range(len(reader.pages)):
        content += reader.pages[page_num].extract_text()
    return content

# Function to generate questions and answers using dummy data
def generate_qa(content, topic, num_questions, answer_type, custom_conditions):
    questions = []
    answers = []
    for i in range(1, num_questions + 1):
        questions.append(f"Sample question {i} about {topic}")
        answers.append(f"Sample {answer_type.lower()} answer for question {i}")
    return questions, answers

# Function to convert questions and answers into a CSV format and save to server
def save_to_csv(questions, answers):
    df = pd.DataFrame({'Questions': questions, 'Answers': answers})
    # Specify a directory to save the CSV file
    directory = "saved_files"
    os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist
    file_path = os.path.join(directory, 'questions_answers.csv')  # Full path to save
    df.to_csv(file_path, index=False)
    return file_path

# Streamlit app structure
def app():
    # Logo and Title beside each other with slight upward adjustment
    col1, col2 = st.columns([1, 3])  # Adjust column width ratio

    with col1:
        st.image("C://Users//hafee//Downloads//Logo.jpeg", width=150)  # Update with your local logo path

    with col2:
        st.markdown(
            "<h1 style='text-align: left; margin-top: -10px;'>Synthetic Data Generator</h1>",
            unsafe_allow_html=True
        )

    # Slogan below the title
    st.markdown("<h2 style='text-align: center;'>Your Reliable Synthetic Dataset Generation</h2>", unsafe_allow_html=True)

    # File Upload for PDF
    file = st.file_uploader("Drag your Content or Document (.pdf only)", type=['pdf'])

    # Topic input
    topic = st.text_input("Topic Name", placeholder="Enter the topic name")

    # Number of questions input
    num_questions = st.number_input("Number of Questions", min_value=1, max_value=100, value=5, step=1)

    # Answer type selection (horizontal)
    answer_type = st.radio("Answer Type", options=["One-word", "Short", "Long"], index=1, horizontal=True)

    # Custom conditions input
    custom_conditions = st.text_area("Custom Conditions", placeholder="Enter any custom rules for the LLM...")

    # Generate button
    generate_button = st.button("Generate")

    if generate_button and file and topic:
        # Extract content from the uploaded PDF
        content = extract_pdf_content(file)

        # Generate questions and answers
        questions, answers = generate_qa(content, topic, num_questions, answer_type, custom_conditions)

        # Display the generated questions and answers
        st.subheader("Generated Questions and Answers")
        for i, (q, a) in enumerate(zip(questions, answers), start=1):
            st.write(f"*Q{i}:* {q}")
            st.write(f"*A{i}:* {a}")
            st.write("---")

        # Save to CSV and provide a download link
        csv_file_path = save_to_csv(questions, answers)

        # Provide a message to indicate where the file is saved
        st.success(f"The CSV file has been saved to the server at: {csv_file_path}")

        # Provide a download link for the CSV file
        with open(csv_file_path, 'rb') as f:
            st.download_button(
                label="Download as CSV",
                data=f,
                file_name="questions_answers.csv",
                mime="text/csv"
            )

        # Add a message below the download button
        st.write("Click the button above to download your CSV file.")

# Run the Streamlit app
if _name_ == "_main_":
    app()