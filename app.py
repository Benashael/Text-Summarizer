import streamlit as st
from txtai.pipeline import Summary
import PyPDF2
import requests
from bs4 import BeautifulSoup

st.set_page_config(
    page_title="Text Summarizer App",
    page_icon="✍️",  # You can replace "✍️" with the URL to your custom icon image
    layout="wide",
)

# Sidebar Navigation
page = st.sidebar.radio("Select a page:", ("Summarize Text", "Summarize Document", "Summarize URL"))

# Initialize txtai components
summary_model = Summary()

if page == "Summarize Text":
    st.header("Summarize Text")
    text = st.text_area("Enter text for summarization:", max_chars=10000)
    if st.button("Summarize"):
        if text:
            try:
                if len(text.split()) > 8000:
                    st.error("Error: Input text exceeds the word limit.")
                else:
                    # Summarize the input text
                    summary = summary_model(text, 5)  # Generate a summary with 5 sentences
                    st.subheader("Summary:")
                    st.write(summary)
            except Exception as e:
                st.error("Error processing the input text. Please check the format.")
        else:
            st.warning("Warning: Please enter some text for summarization")

elif page == "Summarize Document":
    st.header("Summarize Document")
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file:
        # Use PyPDF2 to extract text from the PDF
        pdf_text = ""
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            pdf_text += page.extractText()

        st.write("PDF Text:")
        st.write(pdf_text)

        if st.button("Summarize PDF"):
            if pdf_text:
                try:
                    if len(pdf_text.split()) > 10000:
                        st.error("Error: PDF content exceeds the word limit.")
                    else:
                        # Summarize the PDF content
                        summary = summary_model(pdf_text, 5)  # Generate a summary with 5 sentences
                        st.subheader("Summary:")
                        st.write(summary)
                except Exception as e:
                    st.error("Error processing the PDF text. Please check the format.")
            else:
                st.warning("Warning: The PDF appears to be empty or cannot be extracted.")

elif page == "Summarize URL":
    st.header("Summarize URL")
    url = st.text_input("Enter a URL for summarization:")

    if st.button("Summarize URL"):
        if url:
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    st.error("Error: Invalid URL or could not access the content.")
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = ' '.join(soup.stripped_strings)
                    if len(text.split()) > 20000:
                        st.error("Error: URL content exceeds the word limit.")
                    else:
                        # Summarize the URL content
                        summary = summary_model(text, 5)  # Generate a summary with 5 sentences
                        st.subheader("Summary:")
                        st.write(summary)
            except Exception as e:
                st.error("Error processing the URL content. Please check the URL or its format.")
        else:
            st.warning("Warning: Please enter a URL for summarization")
