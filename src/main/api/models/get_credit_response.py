from src.main.api.models.base_model import BaseModel

from pydantic import Field


class GetCreditResponse(BaseModel):
    id: int
    amount: float
    term_months: int = Field(alias="termMonths")
    balance: float
    credit_id: int = Field(alias="creditId")
