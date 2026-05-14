# uidai-risk-score-assignment
This assignment built with Python FastAPI, Kafka, and SQLite. It demonstrates how to handle asynchronous risk score requests, process them via Kafka, and return results through a callback API.
 Technologies Used
•	Python
•	FastAPI
•	Kafka
•	SQLite
•	SQLAlchemy
•	Docker
•	HTML
**Features**
Part 1 – Ingestion API
•	POST endpoint to initiate risk score request
•	JWT bearer token validation
•	Scope validation (write:risk_test)
•	Aadhaar number masking
•	Save transaction with PENDING status
•	Publish event to Kafka
Part 2 – Background Worker
•	Kafka consumer to process events
•	Generate random risk score
•	Send callback response
•	Retry mechanism for failed callbacks
•	Idempotency handling to avoid duplicate processing
Part 3 – Audit API
•	GET endpoint to fetch transaction status
•	Prevent IDOR with partner ownership validation
•	Optimized database queries
 **Project Structure**
Code
uidai-assignment/
│
├── app/                # Backend FastAPI application
├── frontend/           # Simple HTML frontend
├── docker-compose.yml  # Docker setup
├── README.md           # Documentation
**How to Run**
1.	Start Docker
docker-compose up -d
2.	Run FastAPI
uvicorn app.main:app --reload
3.	Start Kafka Consumer
python -m app.kafka_consumer
4.	Open Frontend
frontend/index.html
 **Swagger API Docs**
http://127.0.0.1:8000/docs
 **Security Highlights**
•	JWT token validation
•	Scope validation
•	Aadhaar number masking
•	IDOR prevention
