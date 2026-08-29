from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.middleware import APILoggingMiddleware
from app.db.init_db import run_init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any, None]:
    # --- Startup ---
    print("Running async database init...")
    await run_init_db()
    print("Application pre-startup setup complete.")

    yield  # No shutdown code needed below this!


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=settings.TAGS_METADATA,
    docs_url=f"{settings.API_V1_STR}/docs",
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Register your custom API Automated Logging Middleware
app.add_middleware(APILoggingMiddleware)


@app.get("/", include_in_schema=False)
async def homepage(request: Request) -> HTMLResponse:
    # print(request.base_url)
    html_content: str = f"""
    <html>
        <head>
            <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
            <title>{settings.PROJECT_NAME}</title>
        </head>
        <body>
            <h1>{settings.PROJECT_NAME}</h1>
            <p>This is the app homepage! Please go on below mentioned link for available APIs.</p>
            <a href="{settings.API_V1_STR}/docs">Swagger Documentation.</a>
        </body>
    </html>
    """

    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


app.include_router(api_router, prefix=settings.API_V1_STR)
