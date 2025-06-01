import streamlit as st
import requests
from datetime import datetime
from utils.evaluator import evaluate_return_request
import base64

# 🔐 Firebase Setup
API_KEY = "API KEY"
PROJECT_ID = "returnssaas"
BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"
REQUESTS_COLLECTION = "return_requests"
RULES_COLLECTION = "return_policies"

st.set_page_config(page_title="ReturnPal - Submit a Return", layout="centered")
st.title("📦 Submit Your Return Request")
st.markdown("Please fill out the details below to request a return.")

# --- Fetch available store names ---
def get_store_names():
    url = f"{BASE_URL}/{RULES_COLLECTION}?key={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            docs = response.json().get("documents", [])
            return [doc["name"].split("/")[-1].replace("_", " ").title() for doc in docs]
        else:
            return []
    except:
        return []

store_options = get_store_names()

# --- Return Form ---
with st.form("return_form"):
    store_name = st.selectbox("Select Store", options=["Select a store"] + store_options)
    order_id = st.text_input("Order ID", placeholder="e.g. #123456")
    customer_name = st.text_input("Your Name")
    return_reason = st.selectbox("Reason for Return", ["Damaged", "Wrong Item", "Too Late", "Other"])
    comments = st.text_area("Additional Comments (optional)")
    is_used = st.checkbox("Was the item used?", value=False)
    product_tags = st.text_input("Product Tags (comma-separated)", placeholder="e.g. sale, tshirt")
    uploaded_image = st.file_uploader("Upload a photo (optional)", type=["jpg", "jpeg", "png"])
    submit = st.form_submit_button("Submit Return Request")

if submit:
    if not store_name or store_name == "Select a store" or not order_id or not customer_name:
        st.warning("Please fill out all required fields.")
    else:
        submitted_date = datetime.now()
        doc_id = store_name.lower().replace(" ", "_")

        # 💡 Auto-evaluate the return
        status = evaluate_return_request(
            store_name=doc_id,
            submitted_date=submitted_date,
            reason=return_reason,
            is_used=is_used,
            product_tags=product_tags
        )

        # 🔄 Optional image encode
        image_data = None
        if uploaded_image:
            image_bytes = uploaded_image.read()
            image_data = base64.b64encode(image_bytes).decode("utf-8")

        # 🔥 Prepare return request data
        return_data = {
            "fields": {
                "store_name": {"stringValue": store_name},
                "order_id": {"stringValue": order_id},
                "customer_name": {"stringValue": customer_name},
                "return_reason": {"stringValue": return_reason},
                "comments": {"stringValue": comments},
                "is_used": {"booleanValue": is_used},
                "product_tags": {"stringValue": product_tags},
                "timestamp": {"timestampValue": submitted_date.isoformat() + "Z"},
                "status": {"stringValue": status},
                "return_reference": {"stringValue": f"RET-{order_id.upper()}"}
            }
        }

        if image_data:
            return_data["fields"]["return_image"] = {"stringValue": image_data}

        # 🔄 Send to Firestore
        request_url = f"{BASE_URL}/{REQUESTS_COLLECTION}?key={API_KEY}"
        response = requests.post(request_url, json=return_data)

        if response.status_code == 200:
            st.success(f"✅ Return submitted! Status: {status}")
        else:
            st.error(f"❌ Failed to submit. Error {response.status_code}")
            st.text(response.text)

st.markdown("---")
st.caption("ReturnPal • Smart Auto-Evaluator + Image Upload Enabled ✨")
