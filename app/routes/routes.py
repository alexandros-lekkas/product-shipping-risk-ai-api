from app.utils.api import check_api_key
from app.models.product_advice import ProductAdviceRequest
from app.services.get_advice import get_advice

from fastapi import APIRouter, Depends

router = APIRouter()

@router.post('/advice/product')
def advice(request: ProductAdviceRequest, api_key: str = Depends(check_api_key)):
    return get_advice(request.user_input, request.item_data)

@router.get('/compare/models')
def compare_models():
    return compare_models()