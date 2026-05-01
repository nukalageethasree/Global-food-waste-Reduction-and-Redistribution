# 🌍 Global Food Waste Reduction and Redistribution Platform

Full-stack application with **Streamlit** frontend, **Node.js/Express** backend, **MySQL** database, and **HuggingFace AI** agents (Mistral-7B).

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL 8.0
- HuggingFace account → https://huggingface.co/settings/tokens

---

### Step 1 — MySQL Setup

```bash
mysql -u root -p < mysql-init/init.sql
```

Or manually:
```sql
CREATE USER 'foodshare_user'@'localhost' IDENTIFIED BY 'foodshare_pass_2024';
GRANT ALL PRIVILEGES ON foodshare.* TO 'foodshare_user'@'localhost';
FLUSH PRIVILEGES;
SOURCE mysql-init/init.sql;
```

---

### Step 2 — Backend

```bash
cd backend
npm install

# Edit .env and optionally add HF_TOKEN
# HF_TOKEN is used by AI agents for food matching

npm start
# API runs at http://localhost:5000
```

---

### Step 3 — Frontend (Streamlit)

```bash
cd frontend
pip install -r requirements.txt

# Create secrets file
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml and add your HuggingFace token

streamlit run app.py
# Opens at http://localhost:8501
```

---

## 🐳 Docker Compose

```bash
export HF_TOKEN=hf_your_token_here
docker-compose up --build
```

| Service   | URL                       |
|-----------|---------------------------|
| Streamlit | http://localhost:8501     |
| Backend   | http://localhost:5000/api |
| MySQL     | localhost:3306            |

---

## 🔐 Demo Login

| Email                  | Password  | Role      |
|------------------------|-----------|-----------|
| demo@foodshare.com     | demo1234  | Donor     |
| alice@freshmart.com    | demo1234  | Donor     |
| bob@citykitchen.com    | demo1234  | Donor     |
| sarah@shelter.org      | demo1234  | Recipient |

Click **⚡ Quick Demo Login** on the login screen.

---

## 🤖 AI Agents (HuggingFace Mistral-7B)

| Agent              | Trigger                    | Function                                      |
|--------------------|----------------------------|-----------------------------------------------|
| Matching Agent     | On every food request      | Scores recipient-listing compatibility 0–100% |
| Expiry Monitor     | Every 15 min (cron)        | Flags urgent listings, sends notifications    |
| Impact Analyzer    | Impact Dashboard page      | Personalized impact summary + badge           |
| Chat Assistant     | AI Chat page               | Conversational food waste expert              |
| Recommender        | Dashboard load             | Personalised next-action suggestions          |
| Match Insight      | Browse Listings (frontend) | Direct HuggingFace call from Streamlit        |
| Waste Analyzer     | Browse Listings (frontend) | Pattern analysis on available food            |

> **Note:** AI agents work without a HuggingFace token (fallback defaults apply), but for best results add `HF_TOKEN` to your `.env` and `secrets.toml`.

---

## 📁 Project Structure

```
foodshare/
├── backend/
│   ├── agents/aiAgents.js    # 5 HuggingFace AI agents
│   ├── config/db.js          # MySQL pool
│   ├── middleware/auth.js    # JWT auth
│   ├── routes/               # auth, listings, requests, dashboard
│   ├── server.js             # Express + cron
│   └── .env
├── frontend/
│   ├── app.py                # Main Streamlit entry point + sidebar nav
│   ├── pages/
│   │   ├── login.py          # Login & Register
│   │   ├── dashboard.py      # Stats + charts + AI recommendations
│   │   ├── browse_listings.py
│   │   ├── create_listing.py
│   │   ├── manage_requests.py
│   │   ├── pickup_tracking.py
│   │   ├── impact_dashboard.py
│   │   ├── ai_chat.py        # Chat with Mistral-7B
│   │   ├── notifications.py
│   │   └── profile.py
│   ├── utils/
│   │   ├── api.py            # HTTP client for backend
│   │   └── hf_ai.py         # Direct HuggingFace calls from frontend
│   ├── .streamlit/
│   │   ├── config.toml       # Theme (green)
│   │   └── secrets.toml.example
│   └── requirements.txt
├── mysql-init/init.sql
├── docker-compose.yml
└── README.md
```

---

## 📡 API Endpoints

| Method | Endpoint                            | Description                  |
|--------|-------------------------------------|------------------------------|
| POST   | /api/auth/register                  | Register                     |
| POST   | /api/auth/login                     | Login                        |
| GET    | /api/auth/me                        | Current user                 |
| PUT    | /api/auth/profile                   | Update profile               |
| GET    | /api/listings                       | Browse listings              |
| POST   | /api/listings                       | Create listing               |
| GET    | /api/listings/my/all                | My listings                  |
| PUT    | /api/listings/:id                   | Update listing               |
| DELETE | /api/listings/:id                   | Cancel listing               |
| POST   | /api/requests                       | Submit request (AI match)    |
| GET    | /api/requests                       | My requests                  |
| PUT    | /api/requests/:id/status            | Approve/reject/complete      |
| GET    | /api/dashboard/stats                | Dashboard KPIs               |
| GET    | /api/dashboard/notifications        | Notifications                |
| PUT    | /api/dashboard/notifications/read-all | Mark all read              |
| GET    | /api/dashboard/impact               | AI impact analysis           |
| GET    | /api/dashboard/recommendations      | AI recommendations           |
| POST   | /api/dashboard/chat                 | AI chat (HuggingFace)        |
| GET    | /api/dashboard/pickup-tracking      | Pickup tracking              |

---

## 🛠️ Tech Stack

| Layer      | Technology                           |
|------------|--------------------------------------|
| Frontend   | Streamlit 1.32, Plotly, Pandas       |
| Backend    | Node.js, Express.js                  |
| Database   | MySQL 8.0 + mysql2                   |
| AI         | HuggingFace Inference API (Mistral-7B-Instruct) |
| Auth       | JWT + bcryptjs                       |
| Scheduler  | node-cron (expiry monitor)           |
| DevOps     | Docker + Docker Compose              |

---

## 🌐 UN SDGs Supported
- **SDG 2** — Zero Hunger
- **SDG 12** — Responsible Consumption & Production
- **SDG 13** — Climate Action
- **SDG 17** — Partnerships for the Goals
