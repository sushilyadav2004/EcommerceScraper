from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.product import Product
from app.schemas.product import (
    ProductUpdate,
    ProductScrapeRequest,
    ProductResponse
)
from app.scraper.product_scraper import scrape_product


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# ==========================================
# POST - Scrape Product & Save
# ==========================================

@router.post(
    "/scrape",
    response_model=ProductResponse
)
def scrape_and_save_product(
    request: ProductScrapeRequest,
    db: Session = Depends(get_db)
):
    try:

        # Scrape website
        product_data = scrape_product(
            str(request.url)
        )

        if not product_data["name"]:
            raise HTTPException(
                status_code=404,
                detail="Product information not found"
            )

        # Create database object
        product = Product(
            name=product_data["name"],
            brand=product_data["brand"],
            price=product_data["price"],
            rating=product_data["rating"],
            reviews=product_data["reviews"],
            scraped_at=product_data["scraped_at"]
        )

        # Save
        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Scraping failed: {str(e)}"
        )


# ==========================================
# GET - All Products
# ==========================================

@router.get(
    "",
    response_model=list[ProductResponse]
)
def get_products(
    db: Session = Depends(get_db)
):
    products = (
        db.query(Product)
        .order_by(Product.id.desc())
        .all()
    )

    return products


# ==========================================
# GET BY ID - Single Product
# ==========================================

@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# ==========================================
# DELETE - Product
# ==========================================

@router.delete(
    "/{product_id}"
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully",
        "id": product_id
    }
@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    request: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = request.name
    product.brand = request.brand
    product.price = request.price
    product.rating = request.rating
    product.reviews = request.reviews

    db.commit()
    db.refresh(product)

    return product