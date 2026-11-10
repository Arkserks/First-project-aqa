import random

import pytest

from src.main.api.geneartors.model_generator import RandomModelGenerator
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.create_deposit_request import CreateDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.models.make_transfer_request import MakeTransferRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_user2_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_credit_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateCreditUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_deposit_request(api_manager, create_user_request):
    account = api_manager.user_steps.create_account(create_user_request)
    amount = RandomModelGenerator.generate_field(CreateDepositRequest, "amount")
    return CreateDepositRequest(account_id=account.id, amount=amount)


@pytest.fixture
def invalid_amount(request):
    """Сумма приходит из parametrize(indirect=True)."""
    return request.param


@pytest.fixture
def invalid_deposit_request(api_manager, create_user_request, invalid_amount):
    account = api_manager.user_steps.create_account(create_user_request)
    return CreateDepositRequest(account_id=account.id, amount=invalid_amount)


@pytest.fixture
def get_credit_valid(api_manager, create_credit_user_request):
    account = api_manager.user_steps.create_account(create_credit_user_request)
    amount = RandomModelGenerator.generate_field(GetCreditRequest, "amount")
    return GetCreditRequest(account_id=account.id, amount=amount, term_months=random.choice([12, 24]))


@pytest.fixture
def get_credit_invalid(api_manager, create_credit_user_request, invalid_amount):
    account = api_manager.user_steps.create_account(create_credit_user_request)
    return GetCreditRequest(account_id=account.id, amount=invalid_amount, term_months=random.choice([12, 24]))


@pytest.fixture
def make_transfer_request_valid(api_manager, create_user_request, create_user2_request, create_deposit_request):
    account2 = api_manager.user_steps.create_account(create_user2_request)
    amount = RandomModelGenerator.generate_field(MakeTransferRequest, "amount")
    deposit_amount = max(1000, amount)
    deposit_request = CreateDepositRequest(account_id=create_deposit_request.account_id, amount=deposit_amount)
    account1 = api_manager.user_steps.create_deposit(deposit_request, create_user_request)
    return MakeTransferRequest(from_account_id=account1.id, to_account_id=account2.id, amount=amount)


@pytest.fixture
def make_transfer_request_invalid(api_manager, create_user_request, create_user2_request, create_deposit_request,
                                  invalid_amount):
    account2 = api_manager.user_steps.create_account(create_user2_request)
    deposit_request = CreateDepositRequest(account_id=create_deposit_request.account_id, amount=1000)
    account1 = api_manager.user_steps.create_deposit(deposit_request, create_user_request)
    return MakeTransferRequest(from_account_id=account1.id, to_account_id=account2.id, amount=invalid_amount)


@pytest.fixture
def credit_repay_request_valid(api_manager, create_credit_user_request, get_credit_valid):
    get_credit = api_manager.user_steps.get_credit_access(get_credit_valid, create_credit_user_request)
    return CreditRepayRequest(credit_id=get_credit.credit_id, account_id=get_credit.id, amount=get_credit.amount)

@pytest.fixture
def credit_repay_request_invalid(api_manager, create_credit_user_request, get_credit_valid):
    get_credit = api_manager.user_steps.get_credit_access(get_credit_valid, create_credit_user_request)
    amount = get_credit.amount - 1
    return CreditRepayRequest(credit_id=get_credit.credit_id, account_id=get_credit.id, amount=amount)
