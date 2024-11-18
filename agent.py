# Import required libraries
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor
from langchain import hub
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate
from langchain_community.tools import TavilySearchResults
import os

api_key = os.getenv("TAVILY_API_KEY")
if not api_key:
    raise ValueError("TAVILY_API_KEY is not set.")

def create_groq_agent():
    # Initialize the language model
    tool = TavilySearchResults(api_key=api_key,search_depth="advanced", include_answer=True,
    include_raw_content=True,max_results=10)

    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

    # Define the list of tools
    tools = [tool]

    # Define the prompt template
    llm_prompt_template = """
    You are an intelligent assistant designed to answer questions accurately and helpfully by leveraging available tools. Your primary role is to understand the user's question, find relevant information using the tools, and respond with a single, precise word without explanation.

    Instructions:
    - For every question, determine if a tool is necessary to obtain the information.
    - If a tool is needed, fetch the information using the tool and respond with a single, precise word.
    - If the answer is straightforward and does not require tool usage, respond with a single word directly.

    Example interactions:
    User: "What is the contact email for XYZ University?"
    Assistant: (Uses the tool to search for information, then responds with "contact@example.com")

    User: "Is the sky blue?"
    Assistant: "Yes"

    Make your answers precise and clear with a single word only without any explanation.
    """

    # Load the prompt template
    prompt = hub.pull("hwchase17/openai-functions-agent")

    for message in prompt.messages:
        if isinstance(message, SystemMessagePromptTemplate):
            message.prompt = PromptTemplate(input_variables=[], template= llm_prompt_template)
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

# Define the function to invoke the agent
def invoke_agent(input_text):
    # Create the agent executor
    agent_executor = create_groq_agent()
    result = agent_executor.invoke({"input": input_text})
    return result['output']
