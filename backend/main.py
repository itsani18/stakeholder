from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from routes.upload_routes import router as upload_router
from routes.analysis import router as analysis_router
from routes.report import router as report_router


app = FastAPI(
    title="AI Stakeholder Feedback Analyzer"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/generated",
    StaticFiles(directory="generated"),
    name="generated"
)

app.include_router(upload_router)
app.include_router(analysis_router)
app.include_router(report_router)


@app.get("/")
async def home():

    return {
        "message": "Backend is running"
    }