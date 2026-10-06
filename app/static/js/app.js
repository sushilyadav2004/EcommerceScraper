async function scrapeProduct() {

    const url = document.getElementById("productUrl").value;
    const message = document.getElementById("message");
    const result = document.getElementById("productResult");

    if (!url) {
        message.innerText = "Please enter product URL.";
        return;
    }

    message.innerText = "Scraping product...";

    try {

        const response = await fetch("/products/scrape", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Scraping failed");
        }

        message.innerText = "Product scraped successfully!";

        result.innerHTML = `
            <div class="product-info">

                <div class="info-box">
                    <strong>Name</strong>
                    ${data.name}
                </div>

                <div class="info-box">
                    <strong>Brand</strong>
                    ${data.brand ?? "N/A"}
                </div>

                <div class="info-box">
                    <strong>Price</strong>
                    $${data.price ?? "N/A"}
                </div>

                <div class="info-box">
                    <strong>Rating</strong>
                    ${data.rating ?? "N/A"}
                </div>

                <div class="info-box">
                    <strong>Reviews</strong>
                    ${data.reviews ?? "N/A"}
                </div>

                <div class="info-box">
                    <strong>Scraped At</strong>
                    ${data.scraped_at}
                </div>

            </div>
        `;

        loadProducts();

    } catch (error) {

        message.innerText = "Error: " + error.message;

    }
}


async function loadProducts() {

    const container = document.getElementById("productsTable");

    try {

        const response = await fetch("/products");

        const products = await response.json();

        if (products.length === 0) {
            container.innerHTML = "No products found.";
            return;
        }

        let html = `
            <table>

                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Brand</th>
                        <th>Price</th>
                        <th>Rating</th>
                        <th>Reviews</th>
                        <th>Scraped At</th>
                    </tr>
                </thead>

                <tbody>
        `;

        products.forEach(product => {

            html += `
                <tr>

                    <td>${product.id}</td>

                    <td>${product.name}</td>

                    <td>${product.brand ?? "N/A"}</td>

                    <td>$${product.price ?? "N/A"}</td>

                    <td>${product.rating ?? "N/A"}</td>

                    <td>${product.reviews ?? "N/A"}</td>

                    <td>${product.scraped_at}</td>

                </tr>
            `;

        });

        html += `
                </tbody>
            </table>
        `;

        container.innerHTML = html;

    } catch (error) {

        container.innerText =
            "Failed to load products: " + error.message;

    }
}


// Load products when page opens
document.addEventListener(
    "DOMContentLoaded",
    loadProducts
);