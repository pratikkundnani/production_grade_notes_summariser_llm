from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
import streamlit as st
import os 
from dotenv import load_dotenv


os.environ["LANGCHAIN_TRACING_V2"]=os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

promt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a document summariser. Please summarise the document keeping the summary short and to the point"),
        ("user", "Question:{question}")
    ]
)

st.title("Notes Summariser App using Ollama") 
input_text=st.text_input("Paste the content to summarise")

llm=Ollama(model='llama3')
output_parser=StrOutputParser()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
    chunk_overlap=200,
    length_function=len)
def summarize_text(input_text):
    segments = text_splitter.split_text(input_text)
    summaries = []
    for segment in segments:
        response = promt | llm | output_parser
        summary = response.invoke({'question': segment})
        summaries.append(summary)
    return " ".join(summaries)

if input_text: 
    st.write(summarize_text(input_text))
