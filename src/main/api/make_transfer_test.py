import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.make_transfer_request import MakeTransferRequest


@pytest.mark.api
class TestTransfer:
    def test_add_transfer_valid(self, api_manager: ApiManager, make_transfer_request_valid: MakeTransferRequest,
                                create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.user_steps.make_transfer_valid(make_transfer_request_valid, create_user_request)

        assert response.from_account_id == make_transfer_request_valid.from_account_id
        assert response.to_account_id == make_transfer_request_valid.to_account_id

        to_account_from_db = Account.get_account_by_id(db_session, make_transfer_request_valid.to_account_id)
        assert to_account_from_db.balance == make_transfer_request_valid.amount, ("Сумма на балансе получателя"
                                                                                  "отличается от суммы перевода, ошибка")

    @pytest.mark.parametrize(
        "invalid_amount",
        [
            499,
            10001
        ],
        indirect=True
    )
    def test_add_transfer_invalid(self, api_manager: ApiManager, make_transfer_request_invalid: MakeTransferRequest,
                                  create_user_request: CreateUserRequest, invalid_amount, db_session: Session):
        response = api_manager.user_steps.make_transfer_invalid(make_transfer_request_invalid, create_user_request)

        assert '{"error":"Amount must be between 500 and 10000"}' in response.text

        to_account_from_db = Account.get_account_by_id(db_session, make_transfer_request_invalid.to_account_id)
        assert to_account_from_db.balance == 0, "Баланс аккаунта адресата пополнен несмотря невалидный amount"