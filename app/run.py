import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",  # noqa: S104
        port=8000,
        reload=True,
        reload_excludes=[".venv", "versions/*.*"],
    )
