import os
import uvicorn
from mcp.server.fastmcp import FastMCP

print("BOOT: app.py starting")
print("BOOT: PORT =", os.environ.get("PORT"))

PORT = int(os.environ.get("PORT", "8080"))

# Give FastMCP the Cloud Run port (may or may not be honored by your version,
# but leaving it doesn't hurt).
os.environ["FASTMCP_PORT"] = str(PORT)
os.environ["FASTMCP_HOST"] = "0.0.0.0"

mcp = FastMCP("ga4-mcp-remote")


@mcp.tool()
def ping() -> str:
    """Health check tool to confirm the MCP server is reachable."""
    return "pong"


class ForwardedHostOverrideMiddleware:
    """
    Cloud Run adds X-Forwarded-Host/Forwarded headers. Some frameworks validate
    those and will return 'Invalid Host header'. This middleware forces a safe
    host value for BOTH Host and X-Forwarded-Host and removes Forwarded.
    """
    def __init__(self, app, host: str = "localhost"):
        self.app = app
        self.host = host.encode("latin-1")

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http":
            new_headers = []
            for k, v in scope.get("headers", []):
                lk = k.lower()
                if lk == b"host":
                    new_headers.append((b"host", self.host))
                elif lk == b"x-forwarded-host":
                    new_headers.append((b"x-forwarded-host", self.host))
                elif lk == b"forwarded":
                    # Drop it entirely to avoid host validation off Forwarded:
                    continue
                else:
                    new_headers.append((k, v))
            scope["headers"] = new_headers

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

    # Override Host + X-Forwarded-Host (and strip Forwarded) to prevent 421
    asgi_app = ForwardedHostOverrideMiddleware(asgi_app, host="localhost")

    uvicorn.run(
        asgi_app,
        host="0.0.0.0",
        port=PORT,
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
