import requests
from src.marketplaces.base import MarketplaceInterface
from src.config import Settings, Marketplace
from src.models.product import Product


class TikTokAPI(MarketplaceInterface):
    BASE_URL = "https://business-api.tiktokglobalshop.com"

    def __init__(self):
        creds = Settings.MARKETPLACE_CREDS[Marketplace.TIKTOK]
        self.app_key = creds["app_key"]
        self.app_secret = creds["app_secret"]
        self.access_token = creds["access_token"]
        self.shop_id = creds["shop_id"]

    def authenticate(self) -> bool:
        """Check if the access token is available."""
        return bool(self.access_token)

    def get_products(self) -> list[Product]:
        """Fetch products from the TikTok shop."""
        url = f"{self.BASE_URL}/product/list"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"shop_id": self.shop_id}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        products = []
        for item in response.json().get("data", {}).get("products", []):
            products.append(Product(
                id=item["id"],
                title=item.get("name", ""),
                price=item.get("price", 0.0),
                inventory=item.get("inventory", 0),
                marketplace=Marketplace.TIKTOK.value
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
