from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from app.database import SessionLocal, engine, Base
from app.models import Transaction
from app.schemas import RiskRequest
from app.auth import verify_token
from app.utils import mask_aadhaar
from app.kafka_producer import publish_event
from fastapi.middleware.cors import CORSMiddleware

# database tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database session function
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



# INITIATE API


@app.post("/api/v1/risk-score/initiate")
def initiate_risk_score(
    request: RiskRequest,
    db: Session = Depends(get_db),
    token=Depends(verify_token)
):

    # Generate transaction id
    transaction_id = str(uuid4())

    # Mask Aadhaar
    masked_aadhaar = mask_aadhaar(
        request.aadhaar_number
    )

    # Save to database
    transaction = Transaction(
        transaction_id=transaction_id,
        partner_id=request.partner_id,
        aadhaar_masked=masked_aadhaar,
        device_data=request.device_data,
        callback_url=request.callback_url,
        status="PENDING"
    )

    db.add(transaction)
    db.commit()

    # Publish Kafka event
    event = {
        "transaction_id": transaction_id
    }

    publish_event(event)

    # Return response
    return {
        "message": "Request Accepted",
        "transaction_id": transaction_id
    }


 
# AUDIT API

@app.get("/api/v1/risk-score/audit/{transaction_id}")
def audit_transaction(
    transaction_id: str,
    db: Session = Depends(get_db),
    token=Depends(verify_token)
):

    # Get logged-in partner id
    partner_id = token["sub"]

    # IDOR prevention
    transaction = db.query(Transaction).filter(
        Transaction.transaction_id == transaction_id,
        Transaction.partner_id == partner_id
    ).first()

    if not transaction:
        return {
            "message": "Transaction Not Found"
        }

    return {
        "transaction_id": transaction.transaction_id,
        "status": transaction.status,
        "risk_score": transaction.risk_score
    }


 
# CALLBACK API
 

@app.post("/callback")
def callback_api(data: dict):

    print("Callback Received")

    print(data)

    return {
        "message": "Callback Success"
    }