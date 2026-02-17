from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/miles/openapi.json",
    openapi_tags=settings.TAGS_METADATA,
    docs_url=f"{settings.API_V1_STR}/miles/docs",
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


@app.get(f"{settings.API_V1_STR}/miles/", tags=["Homepage"], include_in_schema=False)
async def homepage(request: Request) -> HTMLResponse:
    print(request.base_url)
    html_content = """
    <html>
        <head>
            <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
            <title>Miles App</title>
        </head>
        <body>
            <h1>Miles App</h1>
            <p>This is the app homepage! Please go on below mentioned link for available APIs.</p>
            <a href="/api/v1/miles/docs">Swagger Documentation.</a>
        </body>
    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)


app.include_router(api_router, prefix=settings.API_V1_STR)
