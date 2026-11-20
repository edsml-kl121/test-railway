from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="Mew starter railway")


@app.head("/health", include_in_schema=False)
@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.head("/api/greet", include_in_schema=False, response_model=None)
@app.get("/api/greet", response_model=dict[str, str])
async def greet(response: Response, name: str = "") -> dict[str, str] | JSONResponse:
    name = name.strip()
    if not 1 <= len(name) <= 60:
        return JSONResponse(
            status_code=400,
            content={"error": "Enter a name between 1 and 60 characters."},
            headers={"Cache-Control": "no-store"},
        )

    response.headers["Cache-Control"] = "no-store"
    return {"message": f"Hello, {name}!"}
