from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routers.products import router as product_router


app = FastAPI(
    title="E-commerce Product Scraper API",
    description="API for scraping and storing e-commerce product information",
    version="1.0.0"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# API routes
app.include_router(product_router)


# Frontend
@app.get("/")
def home():

    return FileResponse(
        "app/templates/index.html"
    )