from fastapi import APIRouter
from app.routers.category import router as category_router
from app.routers.supplier import router as supplier_router
from app.routers.product import router as product_router
from app.routers.customer import router as customer_router
from app.routers.user import router as user_router
from app.routers.sale import router as sale_router
from app.routers.payment import router as payment_router
from app.routers.receipt import router as receipt_router
from app.routers.sale_item import router as SaleItem_router

api_router = APIRouter()

# Registering all individual endpoints
api_router.include_router(category_router)
api_router.include_router(supplier_router)
api_router.include_router(product_router)
api_router.include_router(customer_router)
api_router.include_router(user_router)
api_router.include_router(sale_router)
api_router.include_router(payment_router)
api_router.include_router(receipt_router)
api_router.include_router(SaleItem_router)


