import streamlit as st
import pandas as pd
import openai
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# Hardcoded API Keys
SERPAPI_API_KEY = "db8323c9ce4fd8b234548b4bd7c6f2c0d5011f56fc2d44fa00af57064123eaa8"
OPENAI_API_KEY = "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"

# Correct the file path
GOOGLE_APPLICATION_CREDENTIALS = r"C:\Users\patha\ai_agent_project\google_service_account.json"  # Using raw string literal for the path
openai.api_key = OPENAI_API_KEY

# Google Sheets Helper Function
def connect_google_sheet(sheet_id, range_name):
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_APPLICATION_CREDENTIALS, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get("values", [])
    return pd.DataFrame(values[1:], columns=values[0]) if values else pd.DataFrame()

# Perform Web Search using SerpAPI
def perform_search(query):
    url = "https://serpapi.com/search"
    params = {"q": query, "api_key": SERPAPI_API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("organic_results", [])

# Extract Information using OpenAI GPT
import openai

# Extract Information using OpenAI GPT
import openai

# Extract Information using OpenAI GPT (updated for new API)
def extract_info_with_llm(prompt, search_results):
    formatted_results = "\n".join([res["snippet"] for res in search_results[:3]])  # Use top 3 results
    full_prompt = f"{prompt}\n\n{formatted_results}"
    
    # Correct API call using openai.ChatCompletion.create
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or the model you are using
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=150
    )
    
    return response['choices'][0]['message']['content'].strip()



# Streamlit Dashboard
st.title("AI Agent Project")

# Step 1: File Upload or Google Sheet
st.header("1. Upload Data or Connect to Google Sheets")

data_source = st.radio("Choose Data Source", ["Upload CSV", "Google Sheets"])
if data_source == "Upload CSV":
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of Uploaded Data", df.head())
else:
    sheet_id = st.text_input("Enter Google Sheet ID")
    range_name = st.text_input("Enter Range Name (e.g., Sheet1!A1:C10)")
    if st.button("Load Google Sheet"):
        if sheet_id and range_name:
            df = connect_google_sheet(sheet_id, range_name)
            st.write("Preview of Google Sheet Data", df.head())

# Step 2: Query and Process
if 'df' in locals():
    st.header("2. Define Query for Information Retrieval")
    main_column = st.selectbox("Select the main column", options=df.columns)
    query_template = st.text_input(
        "Enter your query template (use {entity} as a placeholder)", "Get me the email address of {entity}."
    )
    if st.button("Start Search"):
        results = []
        for entity in df[main_column]:
            # Convert entity to string before replacing in the query template
            search_query = query_template.replace("{entity}", str(entity))
            st.write(f"Searching for: {search_query}")
            search_results = perform_search(search_query)
            if search_results:
                processed_result = extract_info_with_llm(query_template, search_results)
                results.append({"Entity": entity, "Result": processed_result})
            else:
                results.append({"Entity": entity, "Result": "No results found"})
        
        # Display Results
        result_df = pd.DataFrame(results)
        st.write("Search Results", result_df)
        st.download_button(
            label="Download Results as CSV", data=result_df.to_csv(index=False), file_name="results.csv"
        )
