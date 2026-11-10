from typing import Annotated

from src.main.api.geneartors.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel

from pydantic import Field


class MakeTransferRequest(BaseModel):
    from_account_id: int = Field(alias="fromAccountId")
    to_account_id: int = Field(alias="toAccountId")
    amount: Annotated[float, CreationRule(regex=r'^([5-9]\d{2}|[1-8]\d{3})$')]