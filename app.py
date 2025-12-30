import asyncio
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ga4-mcp-remote")

@mcp.tool()
def ping() -> str:
    """Health check tool to confirm the MCP server is reachable."""
    return "pong"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    asyncio.run(
        mcp.run_async(
            transport="streamable-http",
            host="0.0.0.0",
            port=port,
        )
    )
