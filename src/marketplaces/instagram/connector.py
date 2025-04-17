import requests
from src.marketplaces.base import MarketplaceInterface
from src.config import Settings, Marketplace
from src.models.product import Product


class InstagramAPI(MarketplaceInterface):
    BASE_URL = "https://graph.instagram.com/v18.0"

    def __init__(self):
        creds = Settings.MARKETPLACE_CREDS[Marketplace.INSTAGRAM]
        self.access_token = creds["access_token"]
        self.business_id = creds["business_id"]

    def authenticate(self) -> bool:
        """Check if the access token is available."""
        return bool(self.access_token)

    def get_products(self) -> list[Product]:
        """Fetch products from the Instagram catalog."""
        url = f"{self.BASE_URL}/{self.business_id}/products"
        params = {"access_token": self.access_token}
        response = requests.get(url, params=params)
        response.raise_for_status()

        products = []
        for item in response.json().get("data", []):
            products.append(Product(
                id=item["id"],
                title=item.get("name", ""),
                price=0.0,  # Placeholder for price
                inventory=0,
                marketplace=Marketplace.INSTAGRAM.value
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
