from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.analysis import analyze_customer
from app.push import send_push
from app.notification import build_push_message

app = FastAPI()


class LoginPayload(BaseModel):
    customer_id: str


@app.post("/login")
async def login(payload: LoginPayload):
    cid = payload.customer_id
    try:
        analysis = analyze_customer(cid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Decision policy: send a push if there's any actionable insight
    should_notify = bool(analysis.get("out_of_stock") or analysis.get("zero_purchases_2w") or analysis.get("portfolio_suggestions"))
    if should_notify:
        message = build_push_message(analysis)
        send_push(cid, message)

    return {"analysis": analysis, "notified": should_notify}
