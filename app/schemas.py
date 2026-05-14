from pydantic import BaseModel

class RiskRequest(BaseModel):
    partner_id: str
    aadhaar_number: str
    device_data: str
    callback_url: str