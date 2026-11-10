import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrud as Credit
from src.main.api.db.crud.transaction_crud import TransactionCrud as Transaction
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.get_credit_request import GetCreditRequest


@pytest.mark.api
class TestGetCredit:
    def test_get_credit_access(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, get_credit_valid: GetCreditRequest, db_session: Session):
        response = api_manager.user_steps.get_credit_access(get_credit_valid, create_credit_user_request)

        assert response.id == get_credit_valid.account_id
        assert response.amount == get_credit_valid.amount
        assert response.term_months == get_credit_valid.term_months

        credit_from_db = Credit.get_credit_by_id(db_session,response.credit_id)
        assert credit_from_db.balance == -get_credit_valid.amount, "Баланс на счете отличается от суммы запрошенного кредита"

    @pytest.mark.parametrize(
        "invalid_amount",
        [
            4999,
            15001
        ],
        indirect=True,
    )
    def test_get_credit_failure(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, get_credit_invalid: GetCreditRequest, invalid_amount, db_session: Session):
        response = api_manager.user_steps.get_credit_invalid(get_credit_invalid, create_credit_user_request)

        assert "Amount must be between 5000 and 15000" in response.text

        transaction_from_db = Transaction.get_transaction_by_amount(db_session, invalid_amount)
        assert transaction_from_db is None, "Транзакция на получение кредита создана, ошибка"