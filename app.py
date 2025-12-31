import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.middleware.trustedhost import TrustedHostMiddleware

# ---- BOOT LOGS ----
print("BOOT: app.py starting")
print("BOOT: PORT =", os.environ.get("PORT"))

# ---- CONFIG ----
PORT = int(os.environ.get("PORT", "8080"))

# Ensure FastMCP knows the correct bind target
os.environ["FASTMCP_HOST"] = "0.0.0.0"
os.environ["FASTMCP_PORT"] = str(PORT)

# ---- MCP SERVER ----
mcp = FastMCP("ga4-mcp-remote")


@mcp.tool()
def ping() -> str:
    """Health check tool to confirm the MCP server is reachable."""
    return "pong"


# ---- ENTRYPOINT ----
if __name__ == "__main__":
    # Obtain the ASGI app exposed by FastMCP
    if hasattr(mcp, "streamable_http_app"):
        asgi_app = mcp.streamable_http_app()
    elif hasattr(mcp, "app"):
        asgi_app = mcp.app
    else:
        raise RuntimeError(
            "FastMCP does not expose an ASGI app via streamable_http_app() or app"
        )

    # Allow Cloud Run / Google Frontend Host headers
    asgi_app = TrustedHostMiddleware(asgi_app, allowed_hosts=["*"])

    # Start the server explicitly on Cloud Run's required interface
    uvicorn.run(
        asgi_app,
        host="0.0.0.0",
        port=PORT,
        log_level="info",
    )






