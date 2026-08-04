from auditoria.mcp.tools import get_mcp_tools

tools = get_mcp_tools()
print(f'MCP tools: {len(tools)}')
for tool in tools:
    name = tool.get('name', 'unknown')
    description = tool.get('description', '')[:50]
    print(f'  - {name}: {description}...')
