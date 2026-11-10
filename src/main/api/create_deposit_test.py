import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_deposit_request import CreateDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestDeposit:
    def test_create_deposit_valid(self,api_manager: ApiManager,create_user_request: CreateUserRequest, create_deposit_request: CreateDepositRequest, db_session: Session):
        response = api_manager.user_steps.create_deposit(create_deposit_request, create_user_request)

        assert response.id == create_deposit_request.account_id
        assert response.balance == create_deposit_request.amount

        account_from_db = Account.get_account_by_id(db_session, create_deposit_request.account_id)
        assert account_from_db.balance == create_deposit_request.amount, "Баланс на счете отличается от суммы депозита"

    @pytest.mark.parametrize(
        "invalid_amount",
        [
            999,
            9001
        ],
        indirect=True,
    )
    def test_create_deposit_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, invalid_deposit_request: CreateDepositRequest, db_session: Session):
        response = api_manager.user_steps.create_invalid_deposit(invalid_deposit_request, create_user_request)

        assert "Amount must be between 1000 and 9000" in response.text

        account_from_db = Account.get_account_by_id(db_session, invalid_deposit_request.account_id)
        assert account_from_db.balance == 0, "Баланс на счете не нулевой, невалидные значения суммы пополнения прошли"