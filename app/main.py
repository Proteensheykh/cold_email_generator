import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("✉️ Cold Mail Generator")
    url_input = st.text_input("Enter URL here:", value="https://jobs.nike.com/job/R-37526")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader("https://jobs.nike.com/job/R-37526")
            data = clean_text(loader.load().pop().page_content)

            jobs = llm.extract_jobs(data)
            portfolio.load_portfolio()
            for job in jobs:
                skills = job["skills"]
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)


