from fastapi import FastAPI, HTTPException
from models import create_shipment, get_all_shipments, get_shipment_by_id, update_status
from kafka_utils import send_to_kafka
from config import (
    KAFKA_TOPIC_IN_TRANSIT,
    KAFKA_TOPIC_ARRIVAL,
    KAFKA_TOPIC_CUSTOMS,
    KAFKA_TOPIC_DELIVERED
)

app = FastAPI(title="Project Compass Backend")

@app.get("/shipments")
def list_shipments():
    return get_all_shipments()

@app.get("/shipments/{shipment_id}")
def get_shipment(shipment_id: str):
    shipment = get_shipment_by_id(shipment_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment

@app.post("/shipments/create")
def create_new_shipment(data: dict):
    shipment = create_shipment(data)
    send_to_kafka(KAFKA_TOPIC_IN_TRANSIT, shipment)
    return shipment

@app.put("/shipments/{shipment_id}/arrive")
def mark_arrival(shipment_id: str):
    updated = update_status(shipment_id, "AWAITING_CUSTOMS")
    if not updated:
        raise HTTPException(status_code=404, detail="Shipment not found")
    send_to_kafka(KAFKA_TOPIC_ARRIVAL, updated)
    return updated

@app.put("/shipments/{shipment_id}/clear_customs")
def mark_customs_cleared(shipment_id: str):
    updated = update_status(shipment_id, "CLEARED_CUSTOMS")
    if not updated:
        raise HTTPException(status_code=404, detail="Shipment not found")
    send_to_kafka(KAFKA_TOPIC_CUSTOMS, updated)
    return updated

@app.put("/shipments/{shipment_id}/deliver")
def mark_delivered(shipment_id: str):
    updated = update_status(shipment_id, "DELIVERED")
    if not updated:
        raise HTTPException(status_code=404, detail="Shipment not found")
    send_to_kafka(KAFKA_TOPIC_DELIVERED, updated)
    return updated
