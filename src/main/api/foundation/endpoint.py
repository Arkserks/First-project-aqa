from dataclasses import dataclass
from enum import Enum

from src.main.api.models.base_model import BaseModel
from typing import Optional, Type

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_deposit_request import CreateDepositRequest
from src.main.api.models.create_deposit_response import CreateDepositResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.models.get_credit_response import GetCreditResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.make_transfer_request import MakeTransferRequest
from src.main.api.models.maker_transfer_response import MakeTransferResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
        url="/admin/create",
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model=None,
        url="/admin/users",
        response_model=None
    )

    LOGIN_USER = EndpointConfiguration(
        request_model=LoginUserRequest,
        url="/auth/token/login",
        response_model=LoginUserResponse,
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model=None,
        url="/account/create",
        response_model=CreateAccountResponse
    )

    CREATE_DEPOSIT = EndpointConfiguration(
        request_model=CreateDepositRequest,
        url="/account/deposit",
        response_model=CreateDepositResponse
    )

    GET_CREDIT = EndpointConfiguration(
        request_model=GetCreditRequest,
        url="/credit/request",
        response_model=GetCreditResponse
    )

    MAKE_TRANSFER = EndpointConfiguration(
        request_model=MakeTransferRequest,
        url= "/account/transfer",
        response_model=MakeTransferResponse
    )


    CREDIT_REPAY = EndpointConfiguration(
        request_model=CreditRepayRequest,
        url="/credit/repay",
        response_model=CreditRepayResponse
    )

