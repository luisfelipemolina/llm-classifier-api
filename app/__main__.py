import uvicorn

from app import config

def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "app.definition:app_definition",
        workers=config.WORKERS, 
        host=config.HOST,  
        port=config.PORT,
        reload=config.RELOAD, 
        log_level=config.LOG_LEVEL,
        factory=True,  
    )


if __name__ == "__main__":
    main()
