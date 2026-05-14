from sqlalchemy import Column, String, Integer, Boolean
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    partner_id = Column(String, index=True)
    aadhaar_masked = Column(String)
    device_data = Column(String)
    callback_url = Column(String)
    risk_score = Column(Integer, nullable=True)
    status = Column(String)
    processed = Column(Boolean, default=False)