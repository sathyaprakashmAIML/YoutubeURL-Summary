import streamlit as st
import validators
from langchain.chains.summarize import load_summarize_chain
from langchain_groq import ChatGroq
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
from langchain_core.prompts import PromptTemplate
from pytube import YouTube
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

st.set_page_config(page_icon="🤖",page_title="Bot For Summarization")
st.title("🤖 Bot For Summarization")

api_key=st.sidebar.text_input("Groq API KEY",type="password")
st.subheader("Enter your URL")
url=st.text_input("URL",label_visibility="collapsed")

template='''
Provide me the summary of the content ,
content:{text}
'''
template2='''
give me the final summary of the contents with the title for the content,
content:{text}
'''
prompt=PromptTemplate(
    input_variables=["text"],
    template=template
)
prompt2=PromptTemplate(input_variables=['text'],
                       template=template2)
llm=ChatGroq(api_key=api_key,model="gemma2-9b-it")
if st.button("Summarize the URL"):
    if not api_key.strip() or not url.strip():
        st.error("Please enter the API KEY and URL")
    elif not validators.url(url):
        st.error("Please enter a valid URL")
    else:
        with st.spinner("Summarizing..."):
            if "youtube.com" in url:
                    loader=YoutubeLoader.from_youtube_url(url)
            else:
                loader=UnstructuredURLLoader(urls=[url],ssl_verify=False,headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
            documents=loader.load()
            summarize_chain=load_summarize_chain(llm,chain_type="map_reduce",map_prompt=prompt,combine_prompt=prompt2)
            response=summarize_chain.run(documents)
            st.success(response)
                
        
                
                
        
            
               
