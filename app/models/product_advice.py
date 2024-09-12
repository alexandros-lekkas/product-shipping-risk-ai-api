from pydantic import BaseModel

class ProductAdviceRequest(BaseModel):
    user_input: str
    item_data: dict