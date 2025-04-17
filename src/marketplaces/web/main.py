from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.sync_service import SyncService
from src.config import Marketplace

app = FastAPI()
templates = Jinja2Templates(directory="web/templates")
sync = SyncService()

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

    @app.get("/products/{marketplace}", response_class=HTMLResponse)
    async def show_products(request: Request, marketplace: str):
    
    mp = Marketplace(marketplace)
    products = sync.marketplace_apis[mp].get_products()
    return templates.TemplateResponse("products.html", {"request": request, "products": products, "marketplace": marketplace.capitalize()})
    from fastapi import Depends, HTTPException, Cookie
    from src.services.auth_service import get_current_user
    from src.models.user import Role, User

    def require_role(required: Role):
        def wrapper(user: User = Depends(get_current_user)):
                if not user or user.role != required:
                            raise HTTPException(status_code=403, detail="Forbidden")
                                    return user
                                        return wrapper
                from fastapi.responses import RedirectResponse
                from fastapi import Request, Form
                from fastapi.templating import Jinja2Templates

                templates = Jinja2Templates(directory="templates")

                @app.get("/admin/users")
                async def admin_users(request: Request, user: User = Depends(require_role(Role.ADMIN))):
                    users = list(users_db.values())
                        return templates.TemplateResponse("admin_users.html", {"request": request, "users": users, "user": user})

                        @app.post("/admin/update-role")
                        async def update_role(username: str = Form(...), role: str = Form(...), user: User = Depends(require_role(Role.ADMIN))):
                            if username in users_db:
                                    users_db[username].role = Role(role)
                                        return RedirectResponse("/admin/users", status_code=302)
                            