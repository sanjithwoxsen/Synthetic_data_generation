import streamlit as st
from backend import Database, Context, QuestionGeneration, AnswerGeneration, create_csv


# Layout for logo and header
col1, col2 = st.columns([1, 3])
with col1:
    st.image("logo.jpeg", width=150)
with col2:
    st.markdown(
        "<h1 style='text-align: left; margin-top: -10px;'>Synthetic Data Generator</h1>",
        unsafe_allow_html=True
    )
    st.markdown("<h2 style='text-align: center;'>Your Reliable Synthetic Dataset Generation</h2>", unsafe_allow_html=True)

# File Upload Section
file = st.file_uploader("Choose PDF Files", accept_multiple_files=True, type="pdf")
topic = st.text_input("Topic Name", placeholder="Enter the topic name")
num_questions = st.number_input("Number of Questions", min_value=5, max_value=100, value=8)
answer_type = st.radio("Answer Type", options=["One-word", "Short", "Long"], index=1, horizontal=True)
custom_conditions = st.text_area("Custom Conditions", placeholder="Enter any custom rules for the LLM...")

# Generate Button with Input Validation
if st.button("Generate") and file and topic:
    # Process PDF Files and Store Chunks in Vector Store
    with st.spinner("Storing in Database..."):
        db = Database(file)
        db.store()

    # Retrieve Context Based on Topic
    with st.spinner("Retriving Contexts..."):
        context_obj = Context(topic)
        clarified_query = context_obj.redefine()
        context_content = context_obj.retrieve_faiss(clarified_query)

    with st.spinner("Generating Questions..."):
        # Generate Questions
        question_gen = QuestionGeneration(context=context_content, num_questions=num_questions,
                                          question_type=answer_type, conditions=custom_conditions)
        total_questions, questions = question_gen.generate()

    #Display Total questions generated
    st.write(f"Total {total_questions} Questions Generated")

    with st.spinner(f"Generating Answer"):
        # CSS to enlarge the progress bar
        st.markdown("""
                    <style>
                    .stProgress > div > div > div > div {
                        background-color: red; /* Change the color to red */
                        height: 25px; /* Increase this value to make it larger */
                    }
                    </style>
                    """, unsafe_allow_html=True)

        progress_bar = st.progress(0)
        percentage_text = st.empty()

        # Generate Answers
        answer_gen = AnswerGeneration(context_content, questions, answer_type, custom_conditions,
                                      percentage_text=percentage_text, progress_bar=progress_bar)
        answers = answer_gen.generate()

    st.success("Answers Generated")


    # Save Questions and Answers to CSV and Provide Download Option
    csv_file_path,df = create_csv(questions, answers, topic)
    st.write("Preview of Data")
    st.dataframe(df)


    # CSV Download Button
    with open(csv_file_path, 'rb') as file:
        st.write("Click the below button to download your CSV file.")
        st.download_button(label="Download as CSV", data=file, file_name=f"{topic}_questions_answers.csv", mime="text/csv")

