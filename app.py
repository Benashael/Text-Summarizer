import streamlit as st
import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from langdetect import detect
import requests
from bs4 import BeautifulSoup

# Introduction Page
st.title("Welcome to the Text Summarizer App")
st.write("This app is designed to help you summarize text, documents (PDF), or web content from URLs. It offers three main features, each explained below:")

# Feature 1: Summarize Text
st.header("Feature 1: Summarize Text")
st.write("You can use this feature to generate summaries from a piece of text. Follow these steps:")
st.write("1. Enter or paste the text you want to summarize into the 'Enter text for summarization' field.")
st.write("2. Click the 'Summarize' button to receive a summary of the input text.")
st.write("3. The summary will be displayed below the input field.")
st.write("Please note that there is a limit of 1000 words for text input.")

# Feature 2: Summarize Document
st.header("Feature 2: Summarize Document")
st.write("This feature allows you to summarize the content of a PDF document. Here's how you can use it:")
st.write("1. Click on the 'Summarize Document' option in the sidebar.")
st.write("2. Use the 'Upload a PDF file' button to upload the PDF document you want to summarize.")
st.write("3. Click 'Summarize PDF' to receive a summary of the document's content.")
st.write("4. The summary will be displayed below the uploaded document.")
st.write("Keep in mind that document summarization is limited to the first 2 pages of the PDF.")

# Feature 3: Summarize URL
st.header("Feature 3: Summarize URL")
st.write("With this feature, you can generate summaries from web content. Here's how to use it:")
st.write("1. Select 'Summarize URL' in the sidebar.")
st.write("2. Enter the URL of a web page you want to summarize in the 'Enter a URL for summarization' field.")
st.write("3. Click 'Summarize URL' to get a summary of the web content.")
st.write("4. The summary will be displayed below the URL input.")
st.write("Please note that web content summarization is limited to 1000 words, and you should enter a valid URL.")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ("Introduction", "Summarize Text", "Summarize Document", "Summarize URL"))

if page == "Introduction":
    pass
elif page == "Summarize Text":
    st.header("Summarize Text")
    text = st.text_area("Enter text for summarization:", max_chars=1000)
    if st.button("Summarize"):
        if text:
            try:
                if len(text.split()) > 1000:
                    st.error("Error: Input text exceeds the 1000 word limit.")
                else:
                    # Detect language of the input
                    lang = detect(text)
                    if lang != 'en':
                        st.warning("Warning: Input text is not in English.")
                    else:
                        # Initialize the parser with your text
                        parser = PlaintextParser.from_string(text, Tokenizer("english"))
                        summarizer = LsaSummarizer()
                        summary = summarizer(parser.document, 5)  # 5 sentences in the summary
                        summary_text = " ".join([str(sentence) for sentence in summary])
                        st.subheader("Summary:")
                        st.write(summary_text)
            except Exception as e:
                st.error("Error processing the input text. Please check the format.")
        else:
            st.warning("Warning: Please enter some text for summarization")

elif page == "Summarize Document":
    st.header("Summarize Document")
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
                    if len(pdf_text.split()) > 1000:
                        st.error("Error: PDF content exceeds the 1000 word limit.")
                    else:
                        # Detect language of the PDF text
                        lang = detect(pdf_text)
                        if lang != 'en':
                            st.warning("Warning: PDF content is not in English.")
                        else:
                            # Initialize the parser with PDF text
                            parser = PlaintextParser.from_string(pdf_text, Tokenizer("english"))
                            summarizer = LsaSummarizer()
                            summary = summarizer(parser.document, 5)  # 5 sentences in the summary
                            summary_text = " ".join(map(str, summary))
                            st.subheader("Summary:")
                            st.write(summary_text)
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
                    text = soup.get_text()
                    text = ' '.join(text.split())
                    if len(text.split()) > 1000:
                        st.error("Error: URL content exceeds the 1000 word limit.")
                    else:
                        # Detect language of the URL text
                        lang = detect(text)
                        if lang != 'en':
                            st.warning("Warning: URL content is not in English.")
                        else:
                            # Initialize the parser with URL text
                            parser = PlaintextParser.from_string(text, Tokenizer("english"))
                            summarizer = LsaSummarizer()
                            summary = summarizer(parser.document, 5)  # 5 sentences in the summary
                            summary_text = " ".join(map(str, summary))
                            st.subheader("Summary:")
                            st.write(summary_text)
            except Exception as e:
                st.error("Error processing the URL content. Please check the URL or its format.")
        else:
            st.warning("Warning: Please enter a URL for summarization")
