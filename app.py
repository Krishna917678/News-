import streamlit as st
from Backend.Api import fetch_news
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

st.title("News+ — Your AI-Powered News Reader")

query = st.text_input("Search news for:", value="technology")
num_articles = st.slider("Number of articles to fetch:", min_value=1, max_value=10, value=5)

if st.button("Fetch News"):
    articles = fetch_news(query=query, page_size=num_articles)
    if articles:
        for i, article in enumerate(articles, 1):
            st.subheader(f"{i}. {article['title']}")
            st.write(article["description"])
            st.write(f"[Read more]({article['url']})")
            st.write("---")
    else:
        st.error("No articles found or an error occurred.")

# Optional: Add OpenAI GPT summary of first article (example)
if st.button("Summarize First Article with GPT"):
    if not OPENAI_API_KEY:
        st.error("OpenAI API key missing in .env")
    elif articles:
        first_article = articles[0]
        prompt = f"Summarize this news article:\nTitle: {first_article['title']}\nContent: {first_article['content']}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        summary = response.choices[0].text.strip()
        st.markdown(f"**Summary:** {summary}")
    else:
        st.warning("Fetch news articles first.")
