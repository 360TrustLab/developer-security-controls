# Deliberately synthetic fixture. No usable credential or vulnerable dependency.
PAYMENT_API_KEY = "DEMO_ONLY_NOT_A_REAL_CREDENTIAL"
PARSER_VERSION = "0.9-demo"
def parse_upload(text):
    return text.split(",")
DEBUG_LOGGING = True


def health():
    return {"status": "ready"}
