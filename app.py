import os
from mcp.server.fastmcp import FastMCP

print("BOOT: app.py starting")
print("BOOT: PORT=", os.environ.get("PORT"))

# Force FastMCP to bind where Cloud Run expects
os.environ["FASTMCP_HOST"] = "0.0.0.0"
os.environ["FASTMCP_PORT"] = os.environ.get("PORT", "8080")

mcp = FastMCP("ga4-mcp-remote")

@mcp.tool()
def ping() -> str:
    return "pong"

if __name__ == "__main__":
    # IMPORTANT: no host= or port= kwargs for your FastMCP version
    mcp.run(transport="streamable-http")





