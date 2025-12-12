from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.api.video_routes import router as video_router

app = FastAPI(title="Contentizer API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust if frontend runs on different port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
app.include_router(video_router, prefix="/api/video")

@app.get("/health")
async def health_check():
    return {"status": "ok"}