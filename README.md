# Mew starter railway

A small frontend and FastAPI backend served by one Railway service. The form calls the API on the same domain and displays the greeting returned by the server. The app needs no database or secrets.

## Run locally

Use Python 3.11 or newer.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --reload --port 3000
```

Open [localhost:3000](http://localhost:3000) and submit a name. FastAPI’s interactive API docs are at [localhost:3000/docs](http://localhost:3000/docs).

| Route | Response |
| --- | --- |
| `GET /` | Frontend |
| `GET /api/greet?name=Ada` | `{"message":"Hello, Ada!"}` |
| `GET /health` | `{"status":"ok"}` |
| `GET /docs` | Interactive API documentation |

## Deploy from GitHub

1. Create an empty GitHub repository. From this folder, push the app to it. Replace `YOUR_USERNAME` and `YOUR_REPO` with your repository details.

   ```sh
   git init -b main
   git add .
   git commit -m "Add Railway starter app"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. Open [Railway’s GitHub deployment page](https://railway.com/new/github), connect your GitHub account if prompted, select the repository, and choose **Deploy Now**. Railway detects the root [Dockerfile](Dockerfile), and the server uses Railway’s `PORT`. Keep the service root at the repository root. [Railway quick start](https://docs.railway.com/quick-start#deploying-your-project---from-github)
3. In the service settings, go to **Networking → Public Networking → Generate Domain**. Open the generated URL and submit the form. [Railway public networking](https://docs.railway.com/networking/public-networking)
4. To have Railway check readiness on future deployments, set the service’s **Healthcheck Path** to `/health`. [Railway health checks](https://docs.railway.com/deployments/healthchecks)
