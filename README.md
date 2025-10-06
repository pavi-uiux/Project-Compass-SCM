# 🌍 Project Compass - International Shipment Tracking

This project helps track international shipments across their complete lifecycle — from origin to final delivery — using **FastAPI**, **MongoDB**, and **Streamlit**.

---

## 🚀 Features
- Create new shipment records  
- Update shipment stages dynamically  
- Track real-time shipment history  
- MongoDB used for digital thread storage  
- Simple Streamlit frontend for easy access  

---

Create and activate virtual environment

python -m venv venv
venv\Scripts\activate


Install required libraries

pip install -r requirements.txt


Run the FastAPI server

uvicorn main:app --reload

Run the frontend

streamlit run app.py