import openai
from openai import OpenAI
import dotenv
import os
from argomcp.utils.logTitle import logTitle
import asyncio  # 需要导入asyncio模块


dotenv.load_dotenv()

class ChatDoubao():
    def __init__(self, model_name: str, tools = [], system_prompt: str = "", context: str = ""):
        api_key=os.getenv("ARK_API_KEY")
        base_url=os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
        self.model = model_name
        self.tools = tools
        self.system_prompt = system_prompt
        self.context = context
        self.llm = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.message = []

    async def chat(self, prompt = None):
        logTitle(f"Chat")
        if(prompt):
            self.message.append({"role": "user", "content": prompt})
        
        # print("\n\n", self.message)
        stream = self.llm.chat.completions.create(
            model=self.model,
            messages=self.message,
            tools=self.getToolsDefinition(),
            stream=True
        )
        
        content = ""
        toolCalls = []
        
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                contentChunk = chunk.choices[0].delta.content if chunk.choices[0].delta.content else ""
                content += contentChunk
            if delta.tool_calls:
                for toolCallChunk in delta.tool_calls:
                    if len(toolCalls) <= toolCallChunk.index:
                        toolCalls.append({"id": "", "function": {"name": "", "arguments": ""}})
                    currentCall = toolCalls[toolCallChunk.index]
                    # print(f'\n\n\ntoolCallChunk: {toolCallChunk}, currentCall: {currentCall}')
                    # print(toolCallChunk.function.name,  toolCallChunk.function.arguments, toolCallChunk.id)
                    if (toolCallChunk.id):
                        currentCall["id"] += toolCallChunk.id
                    if (toolCallChunk.function.name):
                        currentCall["function"]["name"] += toolCallChunk.function.name
                    if (toolCallChunk.function.arguments):
                        currentCall["function"]["arguments"] += toolCallChunk.function.arguments
                
        self.message.append({
            "role": "assistant", 
            "content": content, 
            "tool_calls": [{"id": call["id"], "type": "function", "function": call["function"]} for call in toolCalls] if toolCalls else None
        })
        
        # print("\n\n\n", self.message)
        return {
            "content": content,
            "toolCalls": toolCalls
        }

    def appendToolResult(self, toolCallId: str, toolOutput: str):
        # for msg in self.message:
        #     if msg.get("role") == "tool" and msg.get("tool_call_id") == toolCallId:
        #         return  # 已存在，不再添加
        self.message.append({
            "role": "tool",
            "content": toolOutput,
            "tool_call_id": toolCallId
        })
                
    def getToolsDefinition(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": tool['name'],
                    "description": tool['description'],
                    "parameters": tool['inputSchema']
                }
            } for tool in self.tools
        ]
        
# if __name__ == '__main__':
#     # 异步主函数
#     async def main():
#         prompt = "你是谁"
#         llm = ChatDoubao("doubao-1-5-lite-32k-250115")
#         # 异步调用需要加await
#         res = await llm.chat(prompt=prompt)
#         print(res)
    
#     # 运行异步主函数
#     asyncio.run(main())