%%writefile app.py
import streamlit as st
from langchain.docstore.document import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.utilities import ApifyWrapper
import os

os.environ["OPENAI_API_KEY"] = "-------YOUR API KEY-------"
os.environ["APIFY_API_TOKEN"] = "-----YOUR APIFY KEY-------"

apify = ApifyWrapper()
# Call the Actor to obtain text from the crawled webpages
loader = apify.call_actor(
    actor_id="apify/website-content-crawler",
    run_input={
        "startUrls": [
           {"url": "https://campusrecreation.illinoisstate.edu"}
        ]
    },
    dataset_mapping_function=lambda item: Document(
        page_content=item["text"] or "", metadata={"source": item["url"]}
    ),
)

index = VectorstoreIndexCreator().from_loaders([loader])
def main():

    # Set the app title
    st.title('ChatBot for ISU Recreation Center')

    st.write('Any Queries? I can assist you')


    user_input = st.text_input("User Input:")
    if st.button("Submit"):
      response = index.query(user_input)
      st.write("Chatbot Response:", response)

if __name__ == "__main__":
      main()
