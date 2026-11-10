import pytest
from sqlalchemy.orm import Session

from src.main.api.db.crud.credit_crud import CreditCrud as Credit

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_valid(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                                credit_repay_request_valid: CreditRepayRequest, db_session: Session):
        response = api_manager.user_steps.credit_repay_valid(credit_repay_request_valid, create_credit_user_request)

        assert response.credit_id == credit_repay_request_valid.credit_id
        assert response.amount_deposited == credit_repay_request_valid.amount

        credit_from_db = Credit.get_credit_by_id(db_session, credit_repay_request_valid.credit_id)
        assert credit_from_db.balance == 0, "Кредит погашен, но сумма кредита не обнулилась, ошибка"

    def test_credit_repay_invalid(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                                  credit_repay_request_invalid: CreditRepayRequest, db_session: Session):
        """
        Проверяем, что при нехватке средств мы не можем погасить кредит.
        """
        response = api_manager.user_steps.credit_repay_invalid(credit_repay_request_invalid, create_credit_user_request)

        assert f"The amount is not enough. Credit balance:" in response.text

        credit_from_db = Credit.get_credit_by_id(db_session, credit_repay_request_invalid.credit_id)
        assert credit_from_db.balance != 0, "Кредит  НЕ погашен, но сумма кредита обнулилась, ошибка"