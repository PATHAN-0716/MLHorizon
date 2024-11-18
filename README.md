# AI Agent for Automated Information Retrieval

## Project Description

This project aims to create an AI agent that reads through datasets (CSV files or Google Sheets) to automatically retrieve specific information for each entity within a chosen column. Users can define search queries with a customizable template, allowing the agent to perform a web search for each entity. Using a language model (LLM), the AI will parse the search results to format and structure extracted information based on the query context. Users can view, download, or update the structured results back into the Google Sheet directly from the dashboard.

## Features

- **Data Upload**: Upload a CSV or connect to Google Sheets for data input.
- **Custom Query Template**: Users can define a query with placeholders for each entity.
- **Automated Web Search**: The AI performs a web search for each entry and retrieves specific information.
- **Structured Output**: The extracted information is formatted into a structured dataset.
- **Download and Update**: Results can be downloaded as a CSV or updated directly into the connected Google Sheets.

## Tools and Libraries

- **Dashboard**: Streamlit for the user interface
- **Data Handling**: pandas for CSVs and Google Sheets API for sheet interaction
- **Search API**: Tavily for web search
- **LLM API**: Groq API to handle and parse search results
- **Agents**: LangChain for orchestrating search and LLM processing




1. **Run the Streamlit application**:
    ```bash
    streamlit run app.py
    ```


2. **Upload Data**:
   - You can either upload a CSV file or enter the Google Sheets ID to load data.
   - For CSV files, use the "Upload Data" sidebar to select and upload your file.
   - For Google Sheets, enter the Google Sheets ID in the sidebar and connect.

3. **Select a Column and Enter Query Template**:
   - Choose the main column that contains the entities you want to search.
   - Enter a query template using `{entity_name}` as a placeholder for the main column values. This placeholder will be replaced with each entity in the column when generating search queries.


4. **Run Agent Query**:
   - Click the **Run Agent Query** button to start the search and extraction process.
   - The system will use the LangChain agent to query **Tavily** and **Groq API** with each generated query.
   - The results will be displayed on the dashboard for review.




5. **Download Results or Update Google Sheets**:
   - Download results as a CSV by clicking **Download Results as CSV**.
   - If connected to Google Sheets, it will automatically update the sheet with the retrieved data.




## API Keys and Environment Variables

1. **Tavily API Key**: Used for search query execution. Add it to an environment variable named `TAVILY_API_KEY`.
2. **Groq API Key**: Used for processing natural language queries. Add it to an environment variable named `GROQ_API_KEY`.
3. **Google Sheets API Credentials**: Ensure the `credentials.json` file is placed in the project directory.

To set environment variables, you can use a `.env` file or export the keys directly in your shell:

```plaintext
# .env file
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
```
Project Demonstration
link-https://drive.google.com/file/d/1QrjxuA2GlsVfTs0QXA5rGHkD0fEzqo8O/view?usp=sharing
