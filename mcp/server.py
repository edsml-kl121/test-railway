import os

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse

backend_url = os.environ.get("BACKEND_URL", "http://backend:8000").rstrip("/")
hosts = [
    host
    for host in (
        "localhost",
        "127.0.0.1",
        "[::1]",
        os.environ.get("RAILWAY_PRIVATE_DOMAIN"),
        os.environ.get("RAILWAY_PUBLIC_DOMAIN"),
    )
    if host
]
authorities = [authority for host in hosts for authority in (host, f"{host}:*")]

mcp = FastMCP(
    "Mew starter railway",
    stateless_http=True,
    json_response=True,
    transport_security=TransportSecuritySettings(
        allowed_hosts=authorities,
        allowed_origins=[
            f"{scheme}://{authority}"
            for scheme in ("http", "https")
            for authority in authorities
        ],
    ),
)


@mcp.tool()
async def greet(name: str) -> str:
    """Return a personalized greeting from the FastAPI backend."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{backend_url}/api/greet", params={"name": name})
            if response.status_code == 400:
                raise ValueError(response.json()["error"])
            response.raise_for_status()
    except httpx.HTTPError as error:
        raise RuntimeError("Could not get a greeting from the backend.") from error

    return response.json()["message"]


@mcp.custom_route("/health", methods=["GET"])
async def health(_request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})


app = mcp.streamable_http_app()
