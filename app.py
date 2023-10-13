import streamlit as st
import PyPDF2
pip install gensim
from gensim.summarization import summarize
from langdetect import detect

st.title("Text Summarizer App")

# User input: Text or PDF
input_option = st.radio("Choose input type:", ("Text", "PDF"))

if input_option == "Text":
    # User inputs text
    text = st.text_area("Enter text for summarization:", max_chars=1000)
    if st.button("Summarize"):
        if text:
            try:
                # Detect language of the input
                lang = detect(text)
                if lang != 'en':
                    st.warning("Input text is not in English.")
                else:
                    # Summarize the text
                    summary = summarize(text)
                    st.subheader("Summary:")
                    st.write(summary)
            except Exception as e:
                st.error("Error processing the input text. Please check the format.")
        else:
            st.warning("Please enter some text for summarization")
else:
    # User inputs a PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_text = ""

        # Limit to the first 2 pages
        max_pages = 2
        for page_num in range(min(max_pages, pdf_reader.numPages)):
            page = pdf_reader.getPage(page_num)
            pdf_text += page.extractText()

        st.write("PDF Text:")
        st.write(pdf_text)

        if st.button("Summarize PDF"):
            if pdf_text:
                try:
                    # Detect language of the PDF text
                    lang = detect(pdf_text)
                    if lang != 'en':
                        st.warning("PDF content is not in English.")
                    else:
                        # Summarize the PDF text
                        summary = summarize(pdf_text)
                        st.subheader("Summary:")
                        st.write(summary)
                except Exception as e:
                    st.error("Error processing the PDF text. Please check the format.")
            else:
                st.warning("The PDF appears to be empty or cannot be extracted.")
