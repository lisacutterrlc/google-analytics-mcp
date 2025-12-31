import os
import asyncio
from mcp.server.fastmcp import FastMCP

print("BOOT: app.py starting")
print("BOOT: PORT=", os.environ.get("PORT"))

# Make FastMCP bind to Cloud Run's required port
os.environ["FASTMCP_PORT"] = os.environ.get("PORT", "8080")
# Host default is already 0.0.0.0 in this SDK, but you can force it too:
os.environ["FASTMCP_HOST"] = "0.0.0.0"

mcp = FastMCP("ga4-mcp-remote")

@mcp.tool()
def ping() -> str:
    return "pong"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
    )





