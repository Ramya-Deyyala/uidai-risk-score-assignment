from kafka import KafkaConsumer
import json
import random
import requests
import time

from app.database import SessionLocal
from app.models import Transaction


# Kafka Consumer
consumer = KafkaConsumer(
    "Risk_Evaluation_Requested",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(
        x.decode('utf-8')
    ),
    auto_offset_reset='earliest',
    group_id='risk-group'
)

# Database session
db = SessionLocal()

print("Kafka Consumer Started...")


# Listen continuously
for message in consumer:

    data = message.value

    print("Received Event:", data)

    # Find transaction
    transaction = db.query(Transaction).filter(
        Transaction.transaction_id == data["transaction_id"]
    ).first()

    # Idempotency check
    if transaction.processed:

        print("Already Processed")

        continue

    # Generate random score
    score = random.randint(1, 100)

    callback_payload = {
        "transaction_id": transaction.transaction_id,
        "risk_score": score
    }

    success = False

    # Retry logic
    for i in range(3):

        try:

            response = requests.post(
                transaction.callback_url,
                json=callback_payload
            )

            print("Retry:", i + 1)

            if response.status_code == 200:

                success = True

                break

        except Exception as e:

            print("Error:", e)

        time.sleep(5)

    # Update DB only once
    if success:

        transaction.risk_score = score

        transaction.status = "COMPLETED"

        transaction.processed = True

        db.commit()

        print("Transaction Completed")