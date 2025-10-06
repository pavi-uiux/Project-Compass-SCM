from config import db
from datetime import datetime
import uuid

shipments = db.shipments

def serialize_doc(doc):
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    # Convert timestamps in history
    if "history" in doc:
        for h in doc["history"]:
            if isinstance(h.get("timestamp"), datetime):
                h["timestamp"] = h["timestamp"].isoformat()
    return doc


def create_shipment(data):
    shipment = {
        "shipment_id": str(uuid.uuid4())[:8].upper(),
        "tracking_number": f"TRK-{uuid.uuid4().hex[:6].upper()}",
        "clientName": data["client_name"],
        "origin": data["origin"],
        "destination": data["destination"],
        "cargoDetails": data.get("cargoDetails", "General Cargo"),
        "status": "IN_TRANSIT_TO_PORT",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "history": [
            {"stage": "IN_TRANSIT_TO_PORT", "timestamp": datetime.utcnow()}
        ]
    }
    shipments.insert_one(shipment)
    return serialize_doc(shipment)


def get_all_shipments():
    return [serialize_doc(s) for s in shipments.find()]


def get_shipment_by_id(shipment_id):
    doc = shipments.find_one({"shipment_id": shipment_id})
    return serialize_doc(doc)


def update_status(shipment_id, new_stage):
    shipment = shipments.find_one({"shipment_id": shipment_id})
    if not shipment:
        return None

    history_entry = {"stage": new_stage, "timestamp": datetime.utcnow()}
    shipments.update_one(
        {"shipment_id": shipment_id},
        {
            "$set": {"status": new_stage, "updated_at": datetime.utcnow()},
            "$push": {"history": history_entry}
        }
    )
    return get_shipment_by_id(shipment_id)
