from langchain.agents import AgentExecutor
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.tools import ShellTool

from tests.agent.glm3_agent import create_structured_glm3_chat_agent

if __name__ == "__main__":
    tools = [ShellTool()]

    llm = ChatZhipuAI()
    # Construct the Tools agent
    agent = create_structured_glm3_chat_agent(llm, tools)

    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    out = agent_executor.invoke({"input": "查看本地目录"})
    print(out)