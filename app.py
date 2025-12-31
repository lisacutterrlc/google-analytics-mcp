import os
import uvicorn
from mcp.server.fastmcp import FastMCP

print("BOOT: app.py starting")
print("BOOT: PORT =", os.environ.get("PORT"))

PORT = int(os.environ.get("PORT", "8080"))

# Ensure FastMCP sees Cloud Run's port
os.environ["FASTMCP_PORT"] = str(PORT)
os.environ["FASTMCP_HOST"] = "0.0.0.0"

mcp = FastMCP("ga4-mcp-remote")


@mcp.tool()
def ping() -> str:
    """Health check tool to confirm the MCP server is reachable."""
    return "pong"


class HostOverrideMiddleware:
    """
    Forces a stable Host header to avoid 'Invalid Host header' rejections
    from inner frameworks/middleware that only allow localhost by default.
    """
    def __init__(self, app, host: str = "localhost"):
        self.app = app
        self.host = host.encode("latin-1")

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http":
            headers = []
            for k, v in scope.get("headers", []):
                # Replace host header with localhost
                if k.lower() == b"host":
                    headers.append((b"host", self.host))
                else:
                    headers.append((k, v))
            scope["headers"] = headers
        await self.app(scope, receive, send)


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

    # Override Host header to prevent 421 Invalid Host header
    asgi_app = HostOverrideMiddleware(asgi_app, host="localhost")

    uvicorn.run(
        asgi_app,
        host="0.0.0.0",
        port=PORT,
        log_level="info",
    )
