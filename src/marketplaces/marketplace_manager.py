
# Import marketplace connectors
from src.marketplaces.facebook.connector import FacebookAPI
from src.marketplaces.instagram.connector import InstagramAPI
from src.marketplaces.tiktok.connector import TikTokAPI
from src.marketplaces.amazon.connector import AmazonAPI
from src.marketplaces.ebay.connector import eBayAPI
from src.marketplaces.shopify.connector import ShopifyAPI
from src.marketplaces.walmart.connector import WalmartAPI

# Inside the MarketplaceManager class
class MarketplaceManager:
    def __init__(self):
        self.marketplace_apis = {
            Marketplace.AMAZON: AmazonAPI(),
            Marketplace.EBAY: eBayAPI(),
            Marketplace.SHOPIFY: ShopifyAPI(),
            Marketplace.WALMART: WalmartAPI(),
            Marketplace.FACEBOOK: FacebookAPI(),
            Marketplace.INSTAGRAM: InstagramAPI(),
            Marketplace.TIKTOK: TikTokAPI()
        }
