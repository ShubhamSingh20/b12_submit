import os
import json
import hmac
import hashlib
import datetime
import urllib.request

URL = "https://b12.io/apply/submission"
SIGNING_SECRET = os.getenv("B12_SIGNING_SECRET").encode("utf-8")

PAYLOAD = {
    "name": "Shubham Singh",
    "email": "shubham1.singh15@gmail.com",
    "resume_link": "https://shubham-singh.dev",
    "repository_link": "https://github.com/ShubhamSingh20/b12_submit",
    "action_run_link": os.getenv("ACTION_RUN_LINK"), 
    "timestamp": (
        datetime.datetime
        .now(datetime.timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    ),
}

json_body = json.dumps(PAYLOAD, separators=(",", ":"), sort_keys=True).encode("utf-8")

print(json_body)

signature = hmac.new(
    SIGNING_SECRET,
    json_body,
    hashlib.sha256
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}",
}

request = urllib.request.Request(
    URL,
    data=json_body,
    headers=headers,
    method="POST"
)

with urllib.request.urlopen(request) as response:
    body = response.read().decode("utf-8")
    status = response.status


resp = json.loads(body)

if status == 200 and resp.get("success"):
    print("Submission successful")
    print("Receipt:", resp.get("receipt"))
else:
    print("Submission failed")
    print("Response:", body)
