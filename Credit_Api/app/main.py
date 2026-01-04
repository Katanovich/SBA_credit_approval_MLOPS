from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app import __version__

app = FastAPI(
    title="SBA Loan API",
    version=__version__,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check — ОБЯЗАТЕЛЬНО для AWS
@app.get("/health")
def health():
    return {"status": "ok"}

# API routes
app.include_router(api_router)
