import requests
from src.marketplaces.base import MarketplaceInterface
from src.config import Settings, Marketplace
from src.models.product import Product


class ShopifyAPI(MarketplaceInterface):
    BASE_URL = "https://<your-shop-name>.myshopify.com/admin/api/2023-01"

    def __init__(self):
        creds = Settings.MARKETPLACE_CREDS[Marketplace.SHOPIFY]
        self.access_token = creds["access_token"]

    def authenticate(self) -> bool:
        """Check if the access token is available."""
        return bool(self.access_token)

    def get_products(self) -> list[Product]:
        """Fetch products from the Shopify store."""
        url = f"{self.BASE_URL}/products.json"
        headers = {"X-Shopify-Access-Token": self.access_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        products = []
        for item in response.json().get("products", []):
            products.append(Product(
                id=item["id"],
                title=item.get("title", ""),
                price=item.get("variants", [{}])[0].get("price", 0.0),
                inventory=item.get("variants", [{}])[0].get("inventory_quantity", 0),
                marketplace=Marketplace.SHOPIFY.value
            ))
        return products

    def update_inventory(self, product_id: str, quantity: int) -> bool:
        """Stub for updating inventory."""
        return True

    def get_orders(self, since=None) -> list:
        """Stub for fetching orders."""
        return []

    def update_order_status(self, order_id: str, status: str) -> bool:
        """Stub for updating order status."""
        return True