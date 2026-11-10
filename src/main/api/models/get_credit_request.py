from typing import Annotated

from src.main.api.geneartors.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel

from pydantic import Field


class GetCreditRequest(BaseModel):
    account_id: int = Field(alias="accountId")
    amount: Annotated[float, CreationRule(regex=r'^([5-9]\d{3}|1[0-4]\d{3})$')]
    term_months: int = Field(alias="termMonths")
