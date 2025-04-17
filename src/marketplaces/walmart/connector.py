import requests
from src.marketplaces.base import MarketplaceInterface
from src.config import Settings, Marketplace
from src.models.product import Product


class WalmartAPI(MarketplaceInterface):
    BASE_URL = "https://marketplace.walmartapis.com/v3"

    def __init__(self):
        creds = Settings.MARKETPLACE_CREDS[Marketplace.WALMART]
        self.client_id = creds["client_id"]
        self.client_secret = creds["client_secret"]

    def authenticate(self) -> bool:
        """Stub for authentication."""
        # Implement OAuth or token-based authentication if needed
        return True

    def get_products(self) -> list[Product]:
        """Fetch products from the Walmart store."""
        url = f"{self.BASE_URL}/items"
        headers = {
            "WM_SVC.NAME": "Walmart Marketplace",
            "WM_QOS.CORRELATION_ID": "123456abcdef",
            "Authorization": f"Basic {self.client_id}:{self.client_secret}"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        products = []
        for item in response.json().get("ItemResponse", []):
            products.append(Product(
                id=item["sku"],
                title=item.get("productName", ""),
                price=item.get("price", {}).get("amount", 0.0),
                inventory=item.get("inventory", {}).get("quantity", 0),
                marketplace=Marketplace.WALMART.value
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