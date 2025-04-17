import requests
from src.marketplaces.base import MarketplaceInterface
from src.config import Settings, Marketplace
from src.models.product import Product


class FacebookAPI(MarketplaceInterface):
    BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(self):
        creds = Settings.MARKETPLACE_CREDS[Marketplace.FACEBOOK]
        self.access_token = creds["access_token"]
        self.catalog_id = creds["catalog_id"]

    def authenticate(self) -> bool:
        """Check if the access token is available."""
        return bool(self.access_token)

    def get_products(self) -> list[Product]:
        """Fetch products from the Facebook catalog."""
        url = f"{self.BASE_URL}/{self.catalog_id}/products"
        params = {"access_token": self.access_token}
        response = requests.get(url, params=params)
        response.raise_for_status()

        products = []
        for item in response.json().get("data", []):
            products.append(Product(
                id=item["id"],
                title=item.get("name", ""),
                price=0.0,  # Meta API doesn't return price directly here
                inventory=0,
                marketplace=Marketplace.FACEBOOK.value
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
