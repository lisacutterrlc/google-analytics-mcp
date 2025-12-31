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
    import uvicorn

    port = int(os.environ.get("PORT", "8080"))

    # Try to get the ASGI app FastMCP exposes for Streamable HTTP
    asgi_app = None
    if hasattr(mcp, "streamable_http_app"):
        asgi_app = mcp.streamable_http_app()  # common pattern
    elif hasattr(mcp, "app"):
        asgi_app = mcp.app  # fallback some versions expose

    if asgi_app is None:
        raise RuntimeError("Could not find an ASGI app on FastMCP instance (expected streamable_http_app() or app).")

    uvicorn.run(asgi_app, host="0.0.0.0", port=port)





