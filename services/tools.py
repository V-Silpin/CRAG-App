from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_CSE_ID"] = os.getenv("GOOGLE_CSE_ID")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def gen_tool():
    search = GoogleSearchAPIWrapper(k=1)    
    def top5_results(query):
        return search.results(query, 5)
    web_search_tool = Tool(
        name="google_search_snippets",
        description="Search Google for recent results.",
        func=top5_results,
    )
    return web_search_tool