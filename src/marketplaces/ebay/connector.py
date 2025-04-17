import requests
from src.marketplaces.base import MarketplaceInterface
from src.config import Settings, Marketplace
from src.models.product import Product


class eBayAPI(MarketplaceInterface):
    BASE_URL = "https://api.ebay.com"

    def __init__(self):
        creds = Settings.MARKETPLACE_CREDS[Marketplace.EBAY]
        self.access_token = creds["access_token"]

    def authenticate(self) -> bool:
        """Check if the access token is available."""
        return bool(self.access_token)

    def get_products(self) -> list[Product]:
        """Fetch products from the eBay store."""
        url = f"{self.BASE_URL}/sell/inventory/v1/inventory_item"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        products = []
        for item in response.json().get("inventoryItems", []):
            products.append(Product(
                id=item["sku"],
                title=item.get("product", {}).get("title", ""),
                price=item.get("price", {}).get("value", 0.0),
                inventory=item.get("availability", {}).get("shipToLocationAvailability", {}).get("quantity", 0),
                marketplace=Marketplace.EBAY.value
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