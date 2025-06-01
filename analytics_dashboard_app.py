import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta, date

# --- Firebase Setup ---
API_KEY = "AIzaSyBaMcUWcLWfyYwIYXRmaeZhBKZCK-rJHSo"
PROJECT_ID = "returnssaas"
COLLECTION = "return_requests"
BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/{COLLECTION}?key={API_KEY}"

st.set_page_config(page_title="📊 Return Analytics Dashboard", layout="wide")
st.title("📈 Seller Analytics Dashboard")

# --- Fetch Data ---
def fetch_data():
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        st.error("Failed to fetch data from Firestore")
        return pd.DataFrame()

    docs = response.json().get("documents", [])
    records = []

    for doc in docs:
        fields = doc.get("fields", {})
        records.append({
            "store": fields.get("store_name", {}).get("stringValue", ""),
            "status": fields.get("status", {}).get("stringValue", "Pending"),
            "reason": fields.get("return_reason", {}).get("stringValue", "Other"),
            "timestamp": fields.get("timestamp", {}).get("timestampValue", "")[:10]
        })

    return pd.DataFrame(records)

# --- Load Data ---
df = fetch_data()

if df.empty:
    st.warning("No return data available.")
else:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    stores = sorted(df["store"].dropna().unique())
    selected_store = st.selectbox("Select your store:", ["Select a store"] + list(stores))

    if selected_store == "Select a store":
        st.info("Please choose a store to view your analytics.")
    else:
        df_store = df[df["store"] == selected_store]

        # --- Date Filter ---
        st.markdown("### 📅 Choose a Day")
        selected_date = st.date_input(
            "📅 Select a return date to view analytics:",
            value=date.today()
        )

        df_filtered = df_store[df_store["timestamp"].dt.date == selected_date]

        st.markdown("### 📊 Key Stats")
        col1, col2, col3, col4 = st.columns(4)
        if not df_filtered.empty and "status" in df_filtered.columns:
            col1.metric("Total Returns", len(df_filtered))
            col2.metric("Approved", (df_filtered["status"] == "Approved").sum())
            col3.metric("Rejected", (df_filtered["status"] == "Rejected").sum())
            col4.metric("Pending", (df_filtered["status"] == "Pending").sum())
        else:
            col1.metric("Total Returns", 0)
            col2.metric("Approved", 0)
            col3.metric("Rejected", 0)
            col4.metric("Pending", 0)

        # --- CSV Download ---
        if not df_filtered.empty:
            csv = df_filtered.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"returns_{selected_store}_{selected_date}.csv",
                mime="text/csv"
            )

        st.divider()

        # --- Charts
        if not df_filtered.empty:
            status_fig = px.pie(df_filtered, names="status", title="Return Status Breakdown", hole=0.4)
            st.plotly_chart(status_fig, use_container_width=True)

            reason_counts = df_filtered["reason"].value_counts().reset_index()
            reason_counts.columns = ["Reason", "Count"]
            reason_fig = px.bar(reason_counts, x="Reason", y="Count", color="Reason", title="Top Return Reasons")
            st.plotly_chart(reason_fig, use_container_width=True)

            trend_data = df_filtered.groupby(df_filtered["timestamp"].dt.date).size().reset_index(name="Returns")
            trend_data.columns = ["Date", "Returns"]
            time_fig = px.line(trend_data, x="Date", y="Returns", markers=True, title="Returns Over Time")
            st.plotly_chart(time_fig, use_container_width=True)
        else:
            st.info("No return data found for the selected date.")

st.markdown("---")
st.caption("Returns SaaS • CSV Export + Analytics • Single-Date UX • v2.8 🚀")
