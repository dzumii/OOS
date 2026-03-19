from init_db import create_db
from app.analysis import analyze_customer
from app.push import send_push
from app.notification import build_push_message


def run():
    create_db()
    cid = "cust_1"
    print(f"Running analysis for {cid}")
    res = analyze_customer(cid)
    print("Analysis result:", res)
    if res["out_of_stock"] or res["zero_purchases_2w"] or res["portfolio_suggestions"]:
        message = build_push_message(res)
        send_push(cid, message)


if __name__ == "__main__":
    run()
