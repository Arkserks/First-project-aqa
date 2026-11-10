from src.main.api.fixtures.user_fixture import create_credit_user_request
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.create_deposit_request import CreateDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.models.make_transfer_request import MakeTransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.responce_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created(),
        ).post()
        return response

    def create_deposit(self, create_deposit_request: CreateDepositRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(create_deposit_request)
        return response

    def create_invalid_deposit(self, create_deposit_request: CreateDepositRequest, create_user_request: CreateUserRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_DEPOSIT,
            ResponseSpecs.request_bad(),
        ).post(create_deposit_request)
        return response

    def get_credit_access(self, get_credit_request: GetCreditRequest, create_credit_user_request: CreateCreditUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
            Endpoint.GET_CREDIT,
            ResponseSpecs.request_created(),
        ).post(get_credit_request)
        return response

    def get_credit_invalid(self, get_credit_request: GetCreditRequest, create_credit_user_request: CreateCreditUserRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
            Endpoint.GET_CREDIT,
            ResponseSpecs.request_bad(),
        ).post(get_credit_request)
        return response

    def make_transfer_valid(self, make_transfer_request: MakeTransferRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.MAKE_TRANSFER,
            ResponseSpecs.request_ok(),
        ).post(make_transfer_request)
        return response

    def make_transfer_invalid(self, make_transfer_request: MakeTransferRequest, create_user_request: CreateUserRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.MAKE_TRANSFER,
            ResponseSpecs.request_bad(),
        ).post(make_transfer_request)
        return response

    def credit_repay_valid(self, credit_repay_request: CreditRepayRequest, create_credit_user_request: CreateCreditUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay_request)
        return response

    def credit_repay_invalid(self, credit_repay_request: CreditRepayRequest, create_credit_user_request: CreateCreditUserRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_bad_bussiness()
        ).post(credit_repay_request)
        return response

