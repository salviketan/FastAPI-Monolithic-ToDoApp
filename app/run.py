import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=80,
        reload=True,
        reload_excludes=[".venv", "versions/*.*"],
    )
