import streamlit as st
import requests

# 🔐 Firebase Setup
API_KEY = "AIzaSyBaMcUWcLWfyYwIYXRmaeZhBKZCK-rJHSo"
PROJECT_ID = "returnssaas"
BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

# UI Setup
st.set_page_config(page_title="Return Policy Setup", layout="centered")
st.title("🛍️ Return Policy Setup for Sellers")
st.markdown("Configure your store's return rules below. These will be used for auto-approving future returns.")

# Input Form
store_name = st.text_input("🏪 Store Name", placeholder="e.g. LuxeWear")
return_days = st.number_input("📆 Return Window (in days)", min_value=1, max_value=60, value=14)
non_returnable = st.text_input("🚫 Non-returnable tags (comma separated)", placeholder="e.g. used, sale")
accept_used = st.checkbox("♻️ Allow return of used items?", value=False)
auto_approve_reasons = st.text_input("⚙️ Auto-approve reasons (comma separated)", placeholder="e.g. damaged, wrong item")

# Save Button
if st.button("💾 Save Return Policy"):
    if not store_name.strip():
        st.warning("⚠️ Please enter a store name.")
    else:
        doc_id = store_name.strip().lower().replace(" ", "_")
        doc_url = f"{BASE_URL}/return_policies/{doc_id}?key={API_KEY}"

        # Firestore Data Format
        data = {
            "fields": {
                "store_name": {"stringValue": store_name},
                "return_days": {"integerValue": int(return_days)},
                "non_returnable_tags": {"stringValue": non_returnable},
                "accept_used": {"booleanValue": accept_used},
                "auto_approve_reasons": {"stringValue": auto_approve_reasons}
            }
        }

        # Firestore API Request
        headers = {"Content-Type": "application/json"}
        response = requests.patch(doc_url, json=data, headers=headers)

        if response.status_code == 200:
            st.success("✅ Return policy saved successfully!")
            st.markdown(f"""
**🏬 Store:** {store_name}  
**⏳ Return Window:** {return_days} days  
**🚫 Non-returnable Tags:** {non_returnable or '_None_'}  
**♻️ Accept Used Items?** {"Yes" if accept_used else "No"}  
**⚙️ Auto-Approve Reasons:** {auto_approve_reasons or '_None_'}
""")
        else:
            st.error(f"❌ Failed to save. Error {response.status_code}")
            st.text(response.text)

st.markdown("---")
st.caption("Returns SaaS • Seller Return Rules • Smart Logic Enabled ✨")
