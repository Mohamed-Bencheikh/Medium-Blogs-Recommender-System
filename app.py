import streamlit as st
from recommend import get_relevant_passage, get_response
import warnings
warnings.filterwarnings("ignore")
def get_search_results(query):
    # Implement the get_relevant_blogs function as before
    with st.spinner("Searching..."):
        rec_articles = get_relevant_passage(query)
        for i, article in enumerate(rec_articles):
            st.write("------------------------------------")
            st.write(f"**Title:** {article['title']}")
            # make a clickable link with text link and url article['url']
            st.write(f"**URL:** [open link]({article['url']})")

def get_chat_response(query):
    st.chat_message(name='human', value=query)
    with st.chat_message(name='bot'):
        with st.spinner("Thinking..."):
            response = get_response(query).text
            st.markdown(response, unsafe_allow_html=True)

st.set_page_config(page_title="Blog Recommendation App")

st.title("Blog Recommendation App")
cols = st.columns([.7, 3])
with cols[0]:
    search_or_chat = st.selectbox("Select an option:", ["Search", "Chat"], label_visibility="collapsed")

if search_or_chat == "Search":
    with cols[1]:
        user_query = st.text_input("Chat", placeholder="Search by keywords or sentence", label_visibility="collapsed")
    if st.button("Search"):
        get_search_results(user_query)

elif search_or_chat == "Chat":
    with cols[1]:
        user_query = st.text_input("Describe", placeholder="Describe what you're looking for", label_visibility="collapsed")
    if st.button("Ask"):
        get_chat_response(user_query)
