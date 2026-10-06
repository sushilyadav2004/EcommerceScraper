from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from app.database.connection import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(500), nullable=False)

    brand = Column(String(200), nullable=True)

    price = Column(Float, nullable=True)

    rating = Column(Float, nullable=True)

    reviews = Column(Integer, nullable=True)

    scraped_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )