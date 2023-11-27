from logging import config as logging_config

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.v1 import lasso
from app.settings.logger import LOGGING
from app.settings.settings import settings

app = FastAPI(
    title=settings.project.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.get("/")
async def root():
    return {"message": "good"}


@app.on_event("startup")
async def startup():
    if settings.project.log_file:
        logging_config.dictConfig(LOGGING)


app.include_router(lasso.router, prefix="/api/v1/lasso", tags=["film"])
