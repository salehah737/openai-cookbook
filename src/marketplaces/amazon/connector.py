import requests
from src.marketplaces.base import MarketplaceInterface
from src.config import Settings, Marketplace
from src.models.product import Product


class AmazonAPI(MarketplaceInterface):
    BASE_URL = "https://sellingpartnerapi-na.amazon.com"

    def __init__(self):
        creds = Settings.MARKETPLACE_CREDS[Marketplace.AMAZON]
        self.access_key = creds["access_key"]
        self.secret_key = creds["secret_key"]
        self.region = creds["region"]

    def authenticate(self) -> bool:
        """Stub for authentication."""
        # Implement AWS Signature V4 authentication if needed
        return True

    def get_products(self) -> list[Product]:
        """Fetch products from the Amazon store."""
        url = f"{self.BASE_URL}/catalog/v0/items"
        headers = {
            "x-amz-access-token": self.access_key,
            "x-amz-secret-key": self.secret_key
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        products = []
        for item in response.json().get("Items", []):
            products.append(Product(
                id=item["Identifiers"]["MarketplaceASIN"]["ASIN"],
                title=item.get("AttributeSets", [{}])[0].get("Title", ""),
                price=0.0,  # Placeholder for price
                inventory=0,  # Placeholder for inventory
                marketplace=Marketplace.AMAZON.value
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