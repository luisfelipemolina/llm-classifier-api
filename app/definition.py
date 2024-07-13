from fastapi import FastAPI

from app.application_gpt import router

def app_definition() -> FastAPI:
            app = FastAPI(
            title="data-api-cnae-classifier",
            description="API para classificação de produtos diretos e indiretos baseados no CNAE da empresa",
            version="0.1.0"
    )
            app.include_router(router)

            return app

