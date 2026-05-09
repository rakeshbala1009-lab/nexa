import requests
import time

# =========================
# CONFIG
# =========================

API_KEY = "nxa_f3ade1c6370a227d66241366d5c6d9aba583964f"
BOT_TOKEN = "8752592084:AAEMM0oZmqE-WDmsInzJwxm9XPMmENRTFJY"
CHAT_ID = "-1003867305261"

BASE_URL = "http://185.190.142.81/api/v1"

HEADERS = {
    "X-API-Key": API_KEY
}

# CHECK EVERY 0.3 SEC
CHECK_DELAY = 0.3

# SAVE SENT IDS
sent_ids = set()

# =========================
# TELEGRAM SEND
# =========================

def send_telegram(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=data, timeout=10)

    except Exception as e:
        print("Telegram Error:", e)

# =========================
# FETCH LOGS
# =========================

def fetch_logs(endpoint):

    try:

        r = requests.get(
            f"{BASE_URL}{endpoint}",
            headers=HEADERS,
            timeout=10
        )

        return r.json()

    except Exception as e:

        print("Fetch Error:", e)
        return None

# =========================
# GET RANGE
# =========================

def get_range(number):

    number = str(number)

    if len(number) >= 7:
        return number[:7] + "xxxx"

    return number

# =========================
# FORMAT MESSAGE
# =========================

def format_message(item):

    app = item.get("app_name", "Unknown")
    number = str(item.get("number", "Unknown"))
    country = item.get("country", "Unknown")

    # RANGE
    range_ = get_range(number)

    text = f"""🔥 <b>NEW LIVE RANGE</b>

━━━━━━━━━━━━━━━━

📱 <b>APP :</b> {app}
🌍 <b>COUNTRY :</b> {country}

📶 <b>RANGE</b>
<code>{range_}</code>

━━━━━━━━━━━━━━━━
"""

    return text

# =========================
# PROCESS LOGS
# =========================

def process_logs(data, prefix):

    if not data:
        return

    if not isinstance(data, dict):
        return

    if not data.get("success"):
        return

    logs = data.get("data", [])

    if not isinstance(logs, list):
        return

    for item in logs:

        # SKIP INVALID ITEMS
        if not isinstance(item, dict):
            continue

        item_id = item.get("id")

        if not item_id:
            continue

        msg_id = f"{prefix}_{item_id}"

        # SKIP DUPLICATE IDS
        if msg_id in sent_ids:
            continue

        sent_ids.add(msg_id)

        try:

            text = format_message(item)

            send_telegram(text)

            print("SENT:", msg_id)

        except Exception as e:

            print("Process Error:", e)

# =========================
# MAIN LOOP
# =========================

print("🔥 LIVE RANGE BOT STARTED...")

while True:

    try:

        # =====================
        # CONSOLE LOGS
        # =====================

        console_data = fetch_logs(
            "/console/logs?limit=50"
        )

        process_logs(
            console_data,
            "console"
        )

        # =====================
        # ENGINE2 LOGS
        # =====================

        engine2_data = fetch_logs(
            "/console/logs/engine2?limit=50"
        )

        process_logs(
            engine2_data,
            "engine2"
        )

    except Exception as e:

        print("MAIN LOOP ERROR:", e)

    # FAST CHECK
    time.sleep(CHECK_DELAY)