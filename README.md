# Mew starter railway

Three services in one GitHub repository. Each service builds from its own Dockerfile and can deploy independently.

| Service | Build directory | What it does |
| --- | --- | --- |
| `frontend` | `frontend/` | Caddy serves the greeting page and forwards `/api/*` to FastAPI. |
| `backend` | `backend/` | FastAPI validates names and returns greetings at `/api/greet`. |
| `mcp` | `mcp/` | An MCP server exposes a `greet` tool over Streamable HTTP at `/mcp`. The tool calls FastAPI. |

The browser sends greeting requests to the frontend domain. Caddy and the MCP server reach FastAPI over the private network. Each service has its own `/health` endpoint.

## Run locally

From the repository root, run:

```sh
docker compose up --build
```

- Submit a name at [localhost:3000](http://localhost:3000).
- Try the API at [localhost:8000/docs](http://localhost:8000/docs).
- Connect an MCP client using Streamable HTTP to `http://localhost:8001/mcp` and call `greet` with `{"name":"Ada"}`. The tool should return `Hello, Ada!`.

## Deploy on Railway from GitHub

1. Commit and push the changes to `main`. Open your Railway project and keep all three services in the same environment. For an existing deployment, reuse the current service as `frontend` to keep its public domain. For a new project, create an empty project and add three empty services.
2. Name the services `frontend`, `backend`, and `mcp`. In each service’s **Settings**, set the **Root Directory** from the table, then connect the same GitHub repository and branch under **Source**. Railway detects the Dockerfile in each root directory. If you previously set a custom build or start command on the existing service, clear it so the Dockerfile controls the startup. [Railway monorepo guide](https://docs.railway.com/deployments/monorepo)
3. Add these variables in each service’s **Variables** tab. Set the backend port explicitly so both clients can reference it.

   | Service | Root Directory | Variables |
   | --- | --- | --- |
   | `frontend` | `/frontend` | `BACKEND_URL=http://${{backend.RAILWAY_PRIVATE_DOMAIN}}:${{backend.PORT}}` |
   | `backend` | `/backend` | `PORT=8000` |
   | `mcp` | `/mcp` | `PORT=8001` and `BACKEND_URL=http://${{backend.RAILWAY_PRIVATE_DOMAIN}}:${{backend.PORT}}` |

   If your Railway environment uses legacy IPv6-only private networking, set `HOST=::` on `backend` and `mcp`. [Railway private networking](https://docs.railway.com/networking/private-networking/how-it-works#internal-dns)
4. Set **Healthcheck Path** to `/health` on each service and deploy the staged changes. To limit future rebuilds to the service that changed, set its **Watch Paths** to `/frontend/**`, `/backend/**`, or `/mcp/**`, respectively. [Railway health checks](https://docs.railway.com/deployments/healthchecks)
5. If the frontend has no public domain, open its **Settings → Networking → Public Networking** and click **Generate Domain**. Open the domain and submit the greeting form. FastAPI stays on the private network. [Railway public networking](https://docs.railway.com/networking/public-networking)

An MCP client in the same Railway environment can use `http://mcp.railway.internal:8001/mcp`. For an external client testing this demo, generate a public domain on the `mcp` service and use `https://<mcp-domain>/mcp`. The demo greeting tool needs no credentials. Add authentication before exposing tools that access private data or perform actions.
