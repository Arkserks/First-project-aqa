from typing import Annotated

from pydantic import Field

from src.main.api.geneartors.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel


class CreateDepositRequest(BaseModel):
    account_id: int = Field(alias="accountId")
    amount: Annotated[float, CreationRule(regex=r'^[1-8]\d{3}$')]

