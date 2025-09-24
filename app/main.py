from fastapi import FastAPI
from .auth import routes as auth_routes
from .addresses import routes as address_routes # Import the new address router

app = FastAPI(
    title="Public Records Notification API",
    description="API for monitoring public records and notifying users.",
    version="1.0.0"
)

# Include the routers
app.include_router(auth_routes.router)
app.include_router(address_routes.router) # Include the new address router

@app.get("/", tags=["Root"])
async def read_root():
    """A simple health check endpoint."""
    return {"status": "API is running"}

