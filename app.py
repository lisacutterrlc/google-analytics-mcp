import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

print("BOOT: app.py starting")
print("BOOT: PORT =", os.environ.get("PORT"))

PORT = int(os.environ.get("PORT", "8080"))

# Cloud Run bind target
os.environ["FASTMCP_PORT"] = str(PORT)
os.environ["FASTMCP_HOST"] = "0.0.0.0"

mcp = FastMCP(
    "ga4-mcp-remote",
    transport_security=TransportSecuritySettings(
        # This is what is currently causing your 421 "Invalid Host header"
        # Disable it for now so Cloud Run host headers are accepted.
        enable_dns_rebinding_protection=False
    ),
)


@mcp.tool()
def ping() -> str:
    """Health check tool to confirm the MCP server is reachable."""
    return "pong"


if __name__ == "__main__":
    # Get the ASGI app for Streamable HTTP
    if hasattr(mcp, "streamable_http_app"):
        asgi_app = mcp.streamable_http_app()
    elif hasattr(mcp, "app"):
        asgi_app = mcp.app
    else:
        raise RuntimeError(
            "FastMCP does not expose an ASGI app via streamable_http_app() or app"
        )

    uvicorn.run(
        asgi_app,
        host="0.0.0.0",
        port=PORT,
        log_level="info",
    )
