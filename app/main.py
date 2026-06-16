from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import connect_db, close_db
from app.routers import products, projects, developers, upload, auth, users, crm, posts, amenities

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    await connect_db()
    yield
    # Shutdown actions
    await close_db()

app = FastAPI(
    title="Anh Duong Property Real Estate API",
    description="Backend API for realty listings, developers, and projects backed by MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS to allow access from local frontend and Vercel deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://cms.anhduong-property.online",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(products.router)
app.include_router(projects.router)
app.include_router(developers.router)
app.include_router(upload.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(crm.router)
app.include_router(posts.router)
app.include_router(amenities.router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "status": "online",
        "service": "Anh Duong Property API Service",
        "version": "1.0.0",
        "docs_url": "/docs"
    }
