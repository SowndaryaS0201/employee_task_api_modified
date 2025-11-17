from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import employees, tasks, auth
import traceback
from fastapi.responses import JSONResponse
from fastapi.requests import Request

# Create DB tables
Base.metadata.create_all(bind=engine)

# Create app
app = FastAPI(
    title="Employee & Task API (JWT, enhanced)",
    version="1.0"
)

# ---------------------------------------------------------
# ✅ CORS MIDDLEWARE (Fixes OPTIONS 405 Error)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "*"   # <-- enable full access for development
    ],
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],  # allow Authorization, Content-Type, etc.
)

# ---------------------------------------------------------
# Middleware to catch unhandled errors (development)
# ---------------------------------------------------------
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        tb = traceback.format_exc()
        print("UNHANDLED EXCEPTION:\n", tb)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------
app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(tasks.router)


# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------
@app.get("/")
def read_root():
    return {"message": "Employee & Task API - visit /docs"}
