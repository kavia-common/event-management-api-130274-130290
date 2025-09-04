from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.events import router as events_router
from .routers.attendees import router as attendees_router


def get_app() -> FastAPI:
    """
    Factory to create and configure the FastAPI application.
    """
    app = FastAPI(
        title="Event Management API",
        description=(
            "A FastAPI backend to manage events and attendees. "
            "Provides CRUD operations for events and attendees and supports "
            "linking attendees to events."
        ),
        version="1.0.0",
        openapi_tags=[
            {"name": "Health", "description": "Service health and metadata."},
            {"name": "Events", "description": "Operations related to events."},
            {"name": "Attendees", "description": "Operations related to attendees."},
            {
                "name": "Event Attendees",
                "description": "Manage attendees associated with a specific event.",
            },
        ],
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health endpoint
    @app.get("/", tags=["Health"], summary="Health Check")
    # PUBLIC_INTERFACE
    def health_check():
        """Simple health check endpoint."""
        return {"message": "Healthy"}

    # Include routers
    app.include_router(events_router)
    app.include_router(attendees_router)

    return app


# For ASGI servers (uvicorn) to discover the app as "app"
app = get_app()
