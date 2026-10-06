from datetime import datetime

from pydantic import BaseModel, HttpUrl


class ProductScrapeRequest(BaseModel):
    url: HttpUrl


class ProductUpdate(BaseModel):
    name: str
    brand: str | None = None
    price: float | None = None
    rating: float | None = None
    reviews: int | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    brand: str | None = None
    price: float | None = None
    rating: float | None = None
    reviews: int | None = None
    scraped_at: datetime

    model_config = {
        "from_attributes": True
    }