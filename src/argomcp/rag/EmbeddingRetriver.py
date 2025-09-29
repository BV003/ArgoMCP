import requests
import os
import dotenv
import json
from VectorStore import VectorStore

dotenv.load_dotenv()

class EmbeddingRetriever:
    def __init__(self, model):
        self.embeddingModel = model
        self.vectorStore = VectorStore()
        self.key = os.getenv("SILICON_KEY")
        
    async def embedDocument(self, text):
        doc_emb = await self.embed(text)
        self.vectorStore.addEmbedding(doc_emb, text)
        return doc_emb

    async def embedQuery(self, text):
        return await self.embed(text)
    
    async def embed(self, text):
        url = "https://api.siliconflow.cn/v1/embeddings"

        payload = {
            "model": self.embeddingModel,
            "input": text,
            "encoding_format": "float"
        }
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        
        data = response.json()
        return data["data"][0]['embedding']
    
    async def retrive(self, query: str, topk: int = 3):
        query_emb = await self.embedQuery(query)
        return self.vectorStore.search(query_emb, topk)
    
    
async def main():
    model = "BAAI/bge-large-zh-v1.5"
    embed = EmbeddingRetriever(model=model)
    res = await embed.embed("你好")
    # print(res)
    
if __name__ == '__main__':
    import asyncio
    print(asyncio.run(main()))
