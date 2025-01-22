from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_mongodb.retrievers.hybrid_search import MongoDBAtlasHybridSearchRetriever
from pymongo import MongoClient
import os
from dotenv import load_dotenv

class Components():
    def __init__(self):
        load_dotenv()
        self.__groq_api_key = os.getenv('GROQ_API_KEY')
        self.__google_api_key = os.getenv("GEMINI_API_KEY")
        self.__atlas_key = os.getenv("ATLAS_CONNECTION_STRING")
        self.__db_name = os.getenv("DB_NAME")
        self.__collection_name = os.getenv("COLLECTION_NAME")
        self.__vector_name = os.getenv("VECTOR_INDEX")
        self.__keyword_name = os.getenv("KEYWORD_INDEX")
    def gen_retrieve(self):
        embeddings = GoogleGenerativeAIEmbeddings(google_api_key=self.__google_api_key, model="models/embedding-001")
        client = MongoClient(self.__atlas_key)
        collection = client[self.__db_name][self.__collection_name]
        vector_store = MongoDBAtlasVectorSearch(
            collection=collection,
            embedding=embeddings,
            index_name=self.__vector_name,
            relevance_score_fn="cosine",
        )
        retriever = MongoDBAtlasHybridSearchRetriever(
            vectorstore = vector_store,
            search_index_name = self.__keyword_name,
            top_k = 5,
            fulltext_penalty = 50,
            vector_penalty = 50
        )
        return retriever
    def gen_llm(self):
        llm = ChatGroq(groq_api_key=self.__groq_api_key, model_name="Llama3-8b-8192")
        return llm