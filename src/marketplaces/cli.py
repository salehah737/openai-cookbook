import logging
from enum import Enum
from typing import Optional

import typer
from typer import progressbar

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = typer.Typer()

class Marketplace(str, Enum):
    AMAZON = "amazon"
    EBAY = "ebay"
    SHOPIFY = "shopify"

class SyncService:
    def __init__(self):
        # Initialize marketplace APIs
        self.marketplace_apis = {
            Marketplace.AMAZON: AmazonAPI(),
            Marketplace.EBAY: EbayAPI(),
            Marketplace.SHOPIFY: ShopifyAPI()
        }

class MarketplaceService:
    def __init__(self, sync_service: SyncService):
        self.sync_service = sync_service

    def list_marketplaces(self) -> list[str]:
        """List all available marketplaces."""
        return [mp.value for mp in Marketplace]

    def fetch_products(self, marketplace: str) -> list:
        """Fetch products from a specific marketplace."""
        mp = self._validate_marketplace(marketplace)
        return self.sync_service.marketplace_apis[mp].get_products()

    def update_inventory(self, marketplace: str, product_id: str, qty: int) -> bool:
        """Update inventory for a specific product."""
        mp = self._validate_marketplace(marketplace)
        if qty < 0:
            raise ValueError("Quantity must be non-negative")
        return self.sync_service.marketplace_apis[mp].update_inventory(product_id, qty)

    def get_orders(self, marketplace: str) -> list:
        """Get orders from a specific marketplace."""
        mp = self._validate_marketplace(marketplace)
        return self.sync_service.marketplace_apis[mp].get_orders()

    def _validate_marketplace(self, marketplace: str) -> Marketplace:
        """Validate marketplace input."""
        try:
            return Marketplace(marketplace.lower())
        except ValueError:
            raise ValueError(f"Invalid marketplace. Available options: {self.list_marketplaces()}")

# Initialize services
sync = SyncService()
service = MarketplaceService(sync)

@app.command()
def list_marketplaces():
    """
    List all available marketplaces.
    
    Usage:
        python cli.py list-marketplaces
    """
    try:
        marketplaces = service.list_marketplaces()
        typer.echo("Available marketplaces:")
        for mp in marketplaces:
            typer.echo(f"- {mp.capitalize()}")
    except Exception as e:
        logger.error(f"Error listing marketplaces: {e}", exc_info=True)
        typer.echo(f"Error: {e}", err=True)

@app.command()
def fetch_products(
    marketplace: str,
    limit: Optional[int] = typer.Option(None, help="Limit number of products to fetch")
):
    """
    Fetch products from a specific marketplace.
    
    Usage:
        python cli.py fetch-products --marketplace amazon
        python cli.py fetch-products --marketplace ebay --limit 10
    """
    try:
        products = service.fetch_products(marketplace)
        if limit:
            products = products[:limit]
        
        typer.echo(f"Products from {marketplace.capitalize()}:")
        with progressbar(products, label="Processing products") as bar:
            for p in bar:
                typer.echo(f"[{p.marketplace}] {p.id} - {p.title} (${p.price})")
    except ValueError as e:
        typer.echo(f"Validation error: {e}", err=True)
    except Exception as e:
        logger.error(f"Error fetching products: {e}", exc_info=True)
        typer.echo(f"Error: {e}", err=True)

@app.command()
def update_inventory(
    marketplace: str,
    product_id: str = typer.Argument(..., help="ID of the product to update"),
    qty: int = typer.Argument(..., help="New inventory quantity"),
):
    """
    Update inventory for a specific product in a marketplace.
    
    Usage:
        python cli.py update-inventory amazon ABC123 50
    """
    try:
        success = service.update_inventory(marketplace, product_id, qty)
        if success:
            typer.echo("✅ Inventory updated successfully")
        else:
            typer.echo("❌ Failed to update inventory", err=True)
    except ValueError as e:
        typer.echo(f"Validation error: {e}", err=True)
    except Exception as e:
        logger.error(f"Error updating inventory: {e}", exc_info=True)
        typer.echo(f"Error: {e}", err=True)

@app.command()
def get_orders(
    marketplace: str,
    status: Optional[str] = typer.Option(None, help="Filter orders by status"),
):
    """
    Get orders from a specific marketplace.
    
    Usage:
        python cli.py get-orders --marketplace shopify
        python cli.py get-orders --marketplace amazon --status shipped
    """
    try:
        orders = service.get_orders(marketplace)
        if status:
            orders = [o for o in orders if o.status.lower() == status.lower()]
        
        typer.echo(f"Orders from {marketplace.capitalize()}:")
        for order in orders:
            typer.echo(f"Order #{order.id} - Status: {order.status}")
    except ValueError as e:
        typer.echo(f"Validation error: {e}", err=True)
    except Exception as e:
        logger.error(f"Error fetching orders: {e}", exc_info=True)
        typer.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    app()
