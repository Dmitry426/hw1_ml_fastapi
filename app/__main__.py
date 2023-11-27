import uvicorn

from app import app
from app.settings.settings import settings

uvicorn.run(app, host=settings.api.host, port=int(settings.api.port))
