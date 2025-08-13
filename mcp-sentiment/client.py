# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: mcp
#     language: python
#     name: python3
# ---

# %%
import gradio as gr

# %%
from mcp.client.stdio import StdioServerParameters
from smolagents import ToolCollection, CodeAgent
from smolagents import CodeAgent, InferenceClientModel
from smolagents.mcp_client import MCPClient
# from gen_ai_hub.proxy.langchain import ChatOpenAI
from dotenv import load_dotenv

import getpass
import os
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

# %%
load_dotenv()

# %%
try:
    # if not os.environ.get("OPENAI_API_KEY"):
    #     os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")


    # model = init_chat_model("gpt-4.1-nano", model_provider="openai")
    mcp_client = MCPClient(
        # {"url": "https://abidlabs-mcp-tools.hf.space/gradio_api/mcp/sse"}
        # {"host": "127.0.0.1", "port": 7860}
        {"url": "http://127.0.0.1:7860/gradio_api/mcp/sse"}, #   "/Users/I570121/.pyenv/versions/mcp/lib/python3.10/site-packages/mcp/client/sse.py", line 66
    )
    tools = mcp_client.get_tools()
    print(f"Tools: {[*tools]}")
    # Create a language model
    # model = ChatOpenAI(temperature=0.0, proxy_model_name="gpt-4.1-nano")

    model = InferenceClientModel()
    agent = CodeAgent(tools=[*tools], model=model)

    demo = gr.ChatInterface(
        fn=lambda message, history: str(agent.run(message)),
        type="messages",
        examples=["Prime factorization of 68"],
        title="Agent with MCP Tools",
        description="This is a simple agent that uses MCP tools to answer questions.",
    )

    demo.launch()
finally:
    mcp_client.close()


# # 
# You have exceeded your monthly included credits for Inference Providers. Subscribe to PRO to get 20x more monthly included credits.
# ^CKeyboard interruption in main thread... closing server.