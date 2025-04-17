import typer
from src.config import Marketplace
from src.sync_service import SyncService

app = typer.Typer()
sync = SyncService()

@app.command()
def list_marketplaces():
    """List all available marketplaces."""
    for mp in Marketplace:
        typer.echo(f"- {mp.value}")

@app.command()
def fetch_products(marketplace: str):
    """Fetch products from a specific marketplace."""
    try:
        mp = Marketplace(marketplace.lower())
        products = sync.marketplace_apis[mp].get_products()
        for p in products:
            typer.echo(f"[{p.marketplace}] {p.id} - {p.title} (${p.price})")
    except Exception as e:
        typer.echo(f"Error fetching products: {e}")

@app.command()
def update_inventory(marketplace: str, product_id: str, qty: int):
    """Update inventory for a specific product in a marketplace."""
    try:
        mp = Marketplace(marketplace.lower())
        result = sync.marketplace_apis[mp].update_inventory(product_id, qty)
        if result:
            typer.echo("Inventory updated successfully.")
        else:
            typer.echo("Failed to update inventory.")
    except Exception as e:
        typer.echo(f"Error: {e}")

@app.command()
def get_orders(marketplace: str):
    """Get orders from a specific marketplace."""
    try:
        mp = Marketplace(marketplace.lower())
        orders = sync.marketplace_apis[mp].get_orders()
        for o in orders:
            typer.echo(f"Order ID: {o.order_id} | Status: {o.status}")
    except Exception as e:
        typer.echo(f"Error getting orders: {e}")

if __name__ == "__main__":
    app()