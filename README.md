# Agentic AI prototype (Python + FastAPI)

Overview
- Minimal end-to-end prototype that captures a `customer_id` at login, analyzes inventory and purchase history, and sends a contextual push prompt when action is recommended.

Quick demo
- Initialize sample DB and run an example (no external deps required):

```bash
python3 run_demo.py
```

Run the API server (optional)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

- POST `/login` with JSON `{"customer_id":"cust_1"}` to trigger analysis and the push stub.

Key files
- [init_db.py](init_db.py) — creates `data.db` with sample inventory and purchases seed data.
- [app/analysis.py](app/analysis.py) — core analysis checks (out-of-stock, zero purchases in 2 weeks, portfolio mix suggestions).
- [app/notification.py](app/notification.py) — builds contextual human-readable push messages from analysis output.
- [app/push.py](app/push.py) — push stub that prints to console and appends to `pushes.log`.
- [main.py](main.py) — FastAPI endpoint `/login` that runs analysis and sends a push when appropriate.
- [run_demo.py](run_demo.py) — convenience runner that seeds the DB and demonstrates analysis + push.

Behavior
- Notifications are plain-text prompts built from analysis (for example: "You're running out of stock on prod_a (red). Please replenish your stock.").
- The push implementation is a stub; replace `app/push.py` with a provider integration (FCM/APNs) and add consent/rate-limit logic for production.

Next steps (suggested)
- Add authentication and securely capture `customer_id` from your login flow.
- Replace the push stub with a real push provider; include opt-in and backoff.
- Improve analysis: add scoring, confidence thresholds, and model-based portfolio recommendations.
- Add tests, monitoring, and audit logs for decisions and notifications.

License & notes
- Prototype code intended for demonstration. Do not use production PII handling without proper controls.
# OOS