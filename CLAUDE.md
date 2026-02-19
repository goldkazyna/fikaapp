# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FIKA is a Telegram Web App for restaurant ordering and payments. Python FastAPI backend with vanilla JS frontend, integrating with **iiko** (POS system) and **Plexy** (payment gateway).

Production URL: https://fikaapp.kz

## Running the App

```bash
pip install fastapi uvicorn requests
python server.py
```

Runs on `0.0.0.0:8000`. No requirements.txt exists — dependencies are fastapi, uvicorn, requests.

## Architecture

### Backend (FastAPI)

- **server.py** — App entry point, mounts static files and includes all routers
- **config.py** — iiko API credentials and IDs (gitignored)
- **routes/** — API endpoint handlers:
  - `pages.py` — HTML page serving (`/`, `/success`, `/fail`)
  - `orders.py` — Table order retrieval and payment (`/api/order/{table}`, `/api/pay/{table}`)
  - `takeaway.py` — Takeaway checkout (`/api/takeaway/checkout`)
  - `webhook.py` — Plexy payment webhook (`/api/webhook/plexy`)
  - `menu.py` — Menu from iiko (`/api/menu`)
  - `rating.py` — Rating submission (`/api/rating`), sends to Telegram bot
- **iiko/** — iiko POS integration:
  - `api.py` — Token management, order fetching, payment adding, order closing
  - `menu.py` — Menu retrieval
  - `tables.py` — Hardcoded table number → iiko UUID mapping (87 tables across 7 sections)
  - `delivery.py` — Pickup/takeaway order creation
- **payments/plexy.py** — Plexy payment link creation (API key hardcoded here)
- **database/models.py** — SQLite schema and CRUD for `payments` table

### Frontend (Vanilla JS SPA)

- **templates/index.html** — Single HTML file with multiple "page" divs
- **static/js/**:
  - `app.js` — Page navigation, table number detection from URL/Telegram params
  - `menu.js` — Menu loading and display
  - `order.js` — Order fetching and payment initiation
  - `takeaway.js` — Takeaway cart management and checkout
- **static/css/style.css** — Dark theme, mobile-first (designed for Telegram WebApp dimensions)

### Data Flow

**Table payment:** User → fetch order from iiko → create Plexy payment link → save to SQLite → redirect to payment → Plexy webhook → add payment to iiko → close order

**Takeaway:** User builds cart in JS → checkout → create Plexy link + save order as temp JSON in `database/` → webhook → create delivery order in iiko → delete temp JSON

### Database

SQLite at `database/fika.db` (gitignored). Single `payments` table with fields: payment_id, table_num, order_id, amount, status (pending/paid), timestamps. Ratings stored in `database/ratings.txt`.

## Credentials

API keys are hardcoded in `config.py` and `payments/plexy.py`. Telegram bot token is in `routes/rating.py`. All are sensitive — do not commit or expose them.
