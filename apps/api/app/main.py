from fastapi import FastAPI

app = FastAPI(
    title="Atman API",
    description="Backend API for the Atman personal AI mentor.",
    version="0.1.0",
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "atman-api"}
