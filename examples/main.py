from argomcp.mcp.MCPClient import MCPClient
from argomcp.agent.Agent import Agent
import os
from argomcp.utils.logTitle import logTitle
from argomcp.rag.EmbeddingRetriver import EmbeddingRetriever
import asyncio




emb_model = os.getenv("EMBEDDING_MODEL")
current_dir = os.getcwd()
fetchMCP = MCPClient("fetch", command="uvx", args=['mcp-server-fetch'])
fileMCP = MCPClient("file", command="npx", args=['-y', '@modelcontextprotocol/server-filesystem', current_dir])

print(f'current_dir is {current_dir}')
TASK = f"""
        告诉我 Chelsey Dietrich 的信息,先从我给你的文件中中找到相关信息,信息在 knowledge 目录下,总结后创作一个关于她的故事
        把故事和她的基本信息保存到{current_dir}/output/antonette.md,输出一个漂亮md文件
        """
async def main():
    # 简化流程，不再使用多层异常处理
    context = await retriveContext()
    logTitle("init Agent")
    agent = Agent("doubao-1-5-lite-32k-250115", [fileMCP], context=context)
    await agent.init()
    logTitle("init Agent finish")
    response = await agent.invoke(TASK)
    agent.log_context.save_to_file()
    return response


async def retriveContext():
    # RAG
    embeddingRetriever = EmbeddingRetriever(embedding_model = emb_model)
    knowledgeDir = os.path.join(current_dir, 'knowledge');
    for file in os.listdir(knowledgeDir):
        with open(os.path.join(knowledgeDir, file), 'r', encoding='utf-8') as f:
            text = f.read()
            await embeddingRetriever.embed_document(text)
            
    context = await embeddingRetriever.retrieve(TASK, 3)
    logTitle(context)
    return context


if __name__ == "__main__":
    # 简单地运行主函数
    result = asyncio.run(main())
    print(result) 
    
    