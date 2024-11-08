import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests
from urllib.parse import quote

st.title("AI AGENT FOR WEB INFORMATION RETRIEVAL")

uploaded_file = st.file_uploader("Upload CSV File", type="csv")
sheet_id = st.text_input("Enter Google Sheet ID")

data = None

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:", data.head())
elif sheet_id:
    credentials = service_account.Credentials.from_service_account_file("google_sheets_key.json")
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range="Sheet1").execute()
    values = result.get("values", [])
    data = pd.DataFrame(values[1:], columns=values[0])
    st.write("Data from Google Sheet:", data.head())

prompt_template = st.text_input("Enter your search prompt (e.g., 'Get me the email address of {company}')")
if data is not None and prompt_template:
    entity_column = st.selectbox("Select column with entities", data.columns)

SERPAPI_KEY = st.secrets["api_keys"]["SERPAPI_KEY"]
GROQ_API_KEY = st.secrets["api_keys"]["GROQ_API_KEY"]
SCRAPERAPI_KEY = st.secrets["api_keys"]["SCRAPERAPI_KEY"]

#st.write("SERPAPI Key: ", SERPAPI_KEY)
#st.write("GROQ API Key: ", GROQ_API_KEY)
#st.write("ScraperAPI Key: ", SCRAPERAPI_KEY)

def serpapi_search(query):
    encoded_query = quote(query)
    url = f"https://serpapi.com/search.json?q={encoded_query}&api_key={SERPAPI_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"Other error occurred: {err}")
    return None

def scraperapi_search(query):
    encoded_query = quote(query)
    url = f"http://api.scraperapi.com?api_key={SCRAPERAPI_KEY}&url=https://www.google.com/search?q={encoded_query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"Other error occurred: {err}")
    return None

def extract_info_with_groq(search_text, prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    full_prompt = f"{prompt}\n\n{search_text}"
    data = {"prompt": full_prompt}
    try:
        response = requests.post("https://api.groq.com/v1/parse", headers=headers, json=data)
        response.raise_for_status()
        return response.json().get("parsed_result", "No result found")
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"Other error occurred: {err}")
    return "Error processing the result"

results = []
if st.button("Run Search and Extract Information"):
    if data is not None and prompt_template:
        for entity in data[entity_column]:
            query = prompt_template.format(company=entity)
            search_result = serpapi_search(query)
            if search_result and 'organic_results' in search_result:
                snippet = search_result['organic_results'][0]['snippet']
                extracted_info = extract_info_with_groq(snippet, prompt_template)
                results.append({"Entity": entity, "Extracted Info": extracted_info})

        result_df = pd.DataFrame(results)
        st.write(result_df)

        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(label="Download Results as CSV", data=csv, file_name="results.csv", mime="text/csv")
    else:
        st.error("Please provide a valid prompt and select a column.")
