import os
import requests
from typing import List
from .VectorStore import VectorStore
from sentence_transformers import SentenceTransformer
from argomcp.utils.logTitle import logTitle
import asyncio



class EmbeddingRetriever:
    def __init__(self, embedding_model: str):
        self.vector_store = VectorStore()
        self.model = SentenceTransformer(embedding_model)


    async def embed_document(self, document: str) -> List[float]:
        logTitle("EMBEDDING DOCUMENT")
        embedding =await self._embed(document)
        self.vector_store.add_embedding(embedding, document)
        return embedding

    async def embed_query(self, query: str) -> List[float]:
        logTitle("EMBEDDING QUERY")
        return await self._embed(query)

    async def _embed(self, text: str) -> List[float]:
        embedding = self.model.encode(text).tolist()
        # print(embedding)
        return embedding


    async def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        query_embedding = await self.embed_query(query)
        return self.vector_store.search(query_embedding, top_k)
    
    
