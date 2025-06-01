
# 🛍️ ReturnPal – Full-Stack Returns Management Platform (Ongoing)

ReturnPal is an ongoing consumer and B2B returns management system built to simplify the product return process for customers while enabling partnered brands to automate and monitor their return workflows. It consists of two main modules:

- **ReturnPal App (B2C)**: For customers to submit product return requests and track status.
- **Returns SaaS Dashboard (B2B)**: For brands to manage, approve, and analyze returns.

---

## 🚀 Features

### 🧾 ReturnPal App (Customer-facing)
- Submit product return requests with image uploads
- Real-time return tracking via **FedEx API**
- Secure login with **Firebase Authentication**
- View status updates and refund progress

### 🧑‍💼 Returns SaaS Dashboard (Brand-facing)
- Role-based seller login
- Visual analytics dashboard for return trends (via **Streamlit**)
- Auto-approval rules using JSON-configurable return conditions
- View item inspection reports and SLA compliance

---

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Firebase Admin SDK
- **Frontend**: Streamlit (for seller dashboard), HTML/React UI (planned for B2C)
- **Database**: Firebase Firestore
- **Authentication**: Firebase Auth, JWT
- **Logistics**: FedEx API
- **Testing**: Postman, unit tests
- **Hosting**: Firebase / Heroku (dev)

---

## 📂 Project Structure

```
Returnpal/
├── firebase_auth.py
├── firebase_key.json              # 🔒 EXCLUDED FROM GIT
├── analytics_dashboard_app.py
├── return_rules_app.py
├── returnpal_app.py
├── pages/
│   ├── login_app.py
│   ├── seller_dashboard_app.py
├── utils/
│   └── evaluator.py
├── roles.json
├── requirements.txt
├── .env                           # 🔒 EXCLUDED FROM GIT
└── README.md
```

---

## 🔐 Security Notes

- 🔒 **Do not upload** `firebase_key.json` or `.env` to GitHub.
- ✅ Add them to `.gitignore`
- Use `firebase_key_sample.json` as a placeholder with dummy values for open-source demo.

---

## ✅ Setup Instructions

1. **Clone this repository**

```bash
git clone https://github.com/your-username/returnpal-returns-platform.git
cd returnpal-returns-platform
```

2. **Create `.env` file** using the provided keys

```bash
cp .env.example .env
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the app**

```bash
streamlit run returnpal_app.py
```

---

## 📈 Status

This project is actively being developed and is part of a larger returns platform prototype for both consumers and enterprise use cases.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---


