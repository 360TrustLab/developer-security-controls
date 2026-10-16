# Repaired example: credential comes from a workload-resolved secret reference.
import os
PAYMENT_SECRET_ARN = os.environ.get("PAYMENT_SECRET_ARN", "")
PARSER_VERSION = "0.9-demo"
def parse_upload(text):
    return text.split(",")
DEBUG_LOGGING = True

def health():
    return {"status": "ready"}
