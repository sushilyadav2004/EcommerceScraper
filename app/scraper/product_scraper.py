import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime

from app.core.logger import logger


def scrape_product(url: str):

    logger.info(f"Scraping started: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # --------------------------------
    # Product Name
    # --------------------------------

    name_element = soup.select_one("#productTitle")

    name = (
        name_element.get_text(" ", strip=True)
        if name_element
        else None
    )

    # --------------------------------
    # Brand
    # --------------------------------

    brand_element = soup.select_one("#bylineInfo")

    brand = (
        brand_element.get_text(" ", strip=True)
        if brand_element
        else None
    )

    # --------------------------------
    # Price
    # --------------------------------

    price = None

    price_container = soup.select_one(
        "#corePrice_feature_div"
    )

    if price_container:

        price_text = price_container.get_text(
            " ",
            strip=True
        )

        # Example:
        # $129 99
        # $129.99

        price_match = re.search(
            r"\$(\d[\d,]*)\s*(?:\.|\s)?(\d{2})",
            price_text
        )

        if price_match:

            dollars = price_match.group(1)
            cents = price_match.group(2)

            price = float(
                f"{dollars.replace(',', '')}.{cents}"
            )

    # --------------------------------
    # Rating + Reviews
    # --------------------------------

    rating = None
    reviews = None

    histogram = soup.select_one(
        "#histogramTable"
    )

    if histogram:

        rating_text = histogram.get_text(
            " ",
            strip=True
        )

        # Example:
        # 4.6 out of 5 · 214 global ratings

        rating_match = re.search(
            r"(\d+(?:\.\d+)?)\s+out of 5",
            rating_text
        )

        review_match = re.search(
            r"([\d,]+)\s+global ratings",
            rating_text
        )

        if rating_match:

            rating = float(
                rating_match.group(1)
            )

        if review_match:

            reviews = int(
                review_match.group(1)
                .replace(",", "")
            )

    # --------------------------------
    # Fallback: Search complete page
    # --------------------------------

    if rating is None or reviews is None:

        page_text = soup.get_text(
            " ",
            strip=True
        )

        rating_match = re.search(
            r"(\d+(?:\.\d+)?)\s+out of 5\s*[·|]\s*([\d,]+)\s+global ratings",
            page_text
        )

        if rating_match:

            rating = float(
                rating_match.group(1)
            )

            reviews = int(
                rating_match.group(2)
                .replace(",", "")
            )

    # --------------------------------
    # Scraped Time
    # --------------------------------

    scraped_at = datetime.now()

    logger.info(
        f"Scraping completed: {name}"
    )

    return {
        "name": name,
        "brand": brand,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "scraped_at": scraped_at
    }