import time
from fastapi import HTTPException

RATE_LIMIT = 5  # requests
TIME_WINDOW = 60  # seconds

user_requests = {}

def check_rate_limit(user: str):
    now = time.time()

    if user not in user_requests:
        user_requests[user] = []
    user_requests[user] = [
        t for t in user_requests[user] if now - t < TIME_WINDOW
    ]

    if len(user_requests[user]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    user_requests[user].append(now)
