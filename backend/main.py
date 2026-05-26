from fastapi            import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat           import router as chat_router
from api.jobs           import router as jobs_router
import ee
from config             import settings

app = FastAPI(
    title      ="Satellite Chatbot API",
    description="GEE powered satellite analysis chatbot",
    version    ="1.0.0"
)

# CORS — frontend ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins    =["*"],  
    allow_credentials=True,
    allow_methods    =["*"],
    allow_headers    =["*"],
)

# Routers
app.include_router(chat_router)
app.include_router(jobs_router)

# GEE startup mein authenticate karo
@app.on_event("startup")
async def startup():
    print("Initializing GEE...")
    ee.Authenticate()
    ee.Initialize(project=settings.gee_project)
    print("GEE ready!")

@app.get("/")
async def root():
    return {"status": "ok", "message": "Satellite Chatbot API running!"}

