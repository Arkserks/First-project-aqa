from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction


class TransactionCrud:
    @staticmethod
    def get_transaction_by_amount(db: Session, amount: float) -> Transaction | None:
        return db.query(Transaction).filter_by(amount=amount).first()

