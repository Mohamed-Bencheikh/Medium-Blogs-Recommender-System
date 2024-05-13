## imports
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import google.generativeai as genai
import textwrap
from dotenv import load_dotenv
import os

## load environment variables
load_dotenv()
embedding_model = SentenceTransformer("all-mpnet-base-v2")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("articles")
genai.configure(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))
## PROMPT
def make_prompt(query, relevant_passage):
  escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = textwrap.dedent(f"""You are a helpful Recommender System  that recommend Medium articles from the list of articles proposed in the context below. \
  Be sure to suggest the most relevant one based on the QUERY, including all relevant background information. \
  Your response should look like this:\
  I recommend this article:\
  TITLE: the title of the article\
  URL: the url of the article\
  Reason: your reasoning for the recommendation\
  If the passage is irrelevant to the answer, you may ignore it.
  QUESTION: '{query}'
  PASSAGE: '{relevant_passage}'
    ANSWER:
  """)
  return prompt

## RELEVANT PASSAGE
def get_relevant_passage(query, top_k=5):
  results = []
  q_emb = embedding_model.encode(query)
  res = index.query(vector=q_emb.tolist(), top_k=top_k, include_metadata=True).to_dict()
  ## get the titles and the urls
  for r in res['matches']:
    title = r['metadata']['title']
    url = r['metadata']['url']
    results.append({'title': title, 'url': url})
  return results

## GET RESPONSE
def get_response(query):
  context = get_relevant_passage(query)
  passage = ""
  for i, res in enumerate(context):
    passage += f"result {i+1}:\n"
    passage += f"Title: {res['title']}\n"
    passage += f"Url: {res['url']}\n"
  prompt = make_prompt(query, passage)
  q_a_model = genai.GenerativeModel('gemini-1.5-pro-latest')
  response = q_a_model.generate_content(prompt)
  return response

# result = get_relevant_passage("What is the best way to learn Python?", top_k=3)
# print(result)

