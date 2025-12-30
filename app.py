import os
import asyncio
from mcp.server.fastmcp import FastMCP

print("BOOT: app.py starting")
print("BOOT: PORT=", os.environ.get("PORT"))

mcp = FastMCP("ga4-mcp-remote")


@mcp.tool()
def ping() -> str:
    """Health check tool to confirm the MCP server is reachable."""
    return "pong"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    # Use the method your FastMCP version actually supports:
    asyncio.run(
        mcp.run_sse_async(
            host="0.0.0.0",
            port=port,
        )
    )


