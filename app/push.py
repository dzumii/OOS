import datetime


def send_push(customer_id: str, message: str):
    ts = datetime.datetime.utcnow().isoformat()
    line = f"{ts} - PUSH to {customer_id}: {message}\n"
    print(line)
    with open("pushes.log", "a") as f:
        f.write(line)
