import os
import tempfile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Case, Transaction
from app.schemas.transaction import TransactionResponse
from app.services.transaction_service import process_transaction_csv


router = APIRouter(
    prefix="/cases",
    tags=["Transactions"]
)


@router.post(
    "/{case_id}/transactions/upload",
    response_model=list[TransactionResponse],
    status_code=status.HTTP_201_CREATED
)
async def upload_transactions(
    case_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if db.query(Case).filter(Case.id == case_id).first() is None:
        raise HTTPException(status_code=404, detail="Case not found")

    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temporary_file:
            temporary_file.write(await file.read())
            temporary_path = temporary_file.name

        dataframe = process_transaction_csv(temporary_path)
        transactions = [
            Transaction(
                case_id=case_id,
                transaction_id=row.transaction_id,
                sender=row.sender,
                receiver=row.receiver,
                amount=float(row.amount),
                timestamp=row.timestamp.to_pydatetime()
            )
            for row in dataframe.itertuples(index=False)
        ]
        db.add_all(transactions)
        db.commit()
        for transaction in transactions:
            db.refresh(transaction)
        return transactions
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    finally:
        if temporary_path:
            os.remove(temporary_path)


@router.get(
    "/{case_id}/transactions",
    response_model=list[TransactionResponse]
)
def get_transactions(
    case_id: int,
    db: Session = Depends(get_db)
):

    case = db.query(Case).filter(
        Case.id == case_id
    ).first()

    if not case:
        return []

    transactions = db.query(Transaction).filter(
        Transaction.case_id == case_id
    ).all()

    return transactions