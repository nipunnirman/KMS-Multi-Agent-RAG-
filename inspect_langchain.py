
import langchain.agents
import inspect

print(f"langchain version: {langchain.__version__}")
if hasattr(langchain.agents, 'create_agent'):
    print("create_agent exists")
else:
    print("create_agent DOES NOT EXIST")

if hasattr(langchain.agents, 'create_openai_tools_agent'):
    print("create_openai_tools_agent exists")
else:
    print("create_openai_tools_agent DOES NOT EXIST")

if hasattr(langchain.agents, 'create_tool_calling_agent'):
    print("create_tool_calling_agent exists")
else:
    print("create_tool_calling_agent DOES NOT EXIST")
