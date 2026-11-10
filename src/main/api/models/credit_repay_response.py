from src.main.api.models.base_model import BaseModel

from pydantic import Field


class CreditRepayResponse(BaseModel):
    credit_id: int = Field(alias="creditId")
    amount_deposited: float = Field(alias="amountDeposited")
