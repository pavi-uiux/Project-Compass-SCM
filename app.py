import streamlit as st
import requests
import pandas as pd

# -------------------------
# CONFIG
# -------------------------
BASE_URL = "http://localhost:8000/shipments"

st.set_page_config(page_title="Project Compass - Shipment Tracker", layout="wide")

st.title("🌍 Project Compass - International Shipment Tracking")
st.write("Track and update global shipments in real time.")

# -------------------------
# NAVIGATION MENU
# -------------------------
menu = ["Create Shipment", "View All Shipments", "Update Shipment Status"]
choice = st.sidebar.selectbox("Navigation", menu)

# -------------------------
# 1️⃣ CREATE SHIPMENT
# -------------------------
if choice == "Create Shipment":
    st.header("🚢 Create a New Shipment")

    # Initialize session state if not already
    if "client" not in st.session_state:
        st.session_state.client = ""
    if "origin" not in st.session_state:
        st.session_state.origin = ""
    if "destination" not in st.session_state:
        st.session_state.destination = ""

    # Text input widgets
    client = st.text_input("Client Name", value=st.session_state.client, key="client_input")
    origin = st.text_input("Origin", value=st.session_state.origin, key="origin_input")
    destination = st.text_input("Destination", value=st.session_state.destination, key="destination_input")

    if st.button("Create Shipment"):
        if client and origin and destination:
            payload = {
                "client_name": client,
                "origin": origin,
                "destination": destination
            }
            try:
                res = requests.post(f"{BASE_URL}/create", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.success("Shipment created successfully!")
                    st.json(data)

                    # Reset session state values to clear the form
                    st.session_state.client = ""
                    st.session_state.origin = ""
                    st.session_state.destination = ""
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
        else:
            st.warning("Please fill in all fields.")

# -------------------------
# 2️⃣ VIEW ALL SHIPMENTS
# -------------------------
elif choice == "View All Shipments":
    st.header("📦 View All Shipments")

    try:
        res = requests.get(BASE_URL)
        if res.status_code == 200:
            shipments = res.json()
            if shipments:
                df = pd.DataFrame(shipments)
                st.dataframe(df)

                shipment_id = st.text_input("Enter Shipment ID to view details")
                if st.button("View Details"):
                    if shipment_id:
                        r = requests.get(f"{BASE_URL}/{shipment_id}")
                        if r.status_code == 200:
                            st.subheader("Shipment Details:")
                            st.json(r.json())
                        else:
                            st.error("Shipment not found.")
            else:
                st.info("No shipments found.")
        else:
            st.error("Error fetching shipments.")
    except Exception as e:
        st.error(f"Backend connection failed: {e}")

# -------------------------
# 3️⃣ UPDATE SHIPMENT STATUS
# -------------------------
elif choice == "Update Shipment Status":
    st.header("🔄 Update Shipment Status")
    shipment_id = st.text_input("Enter Shipment ID")

    stage = st.selectbox(
        "Select the next stage",
        ["IN_TRANSIT_TO_PORT", "AWAITING_CUSTOMS", "CLEARED_CUSTOMS", "DELIVERED"]
    )

    if st.button("Update Status"):
        if shipment_id:
            endpoint = None
            if stage == "AWAITING_CUSTOMS":
                endpoint = f"{BASE_URL}/{shipment_id}/arrive"
            elif stage == "CLEARED_CUSTOMS":
                endpoint = f"{BASE_URL}/{shipment_id}/clear_customs"
            elif stage == "DELIVERED":
                endpoint = f"{BASE_URL}/{shipment_id}/deliver"
            elif stage == "IN_TRANSIT_TO_PORT":
                st.info("Shipment is already in transit after creation.")
                endpoint = None

            if endpoint:
                try:
                    res = requests.put(endpoint)
                    if res.status_code == 200:
                        st.success("Shipment status updated successfully!")
                        st.json(res.json())
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Failed to connect: {e}")
        else:
            st.warning("Please enter a valid Shipment ID.")
