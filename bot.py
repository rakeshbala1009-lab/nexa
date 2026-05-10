import requests
import time

# =========================
# CONFIG
# =========================

API_KEY = "nxa_f3ade1c6370a227d66241366d5c6d9aba583964f"
BOT_TOKEN = "8752592084:AAEMM0oZmqE-WDmsInzJwxm9XPMmENRTFJY"
CHAT_ID = "-1003867305261"

BASE_URL = "http://185.190.142.81"

HEADERS = {
    "X-API-Key": API_KEY
}

# ULTRA FAST CHECK
CHECK_DELAY = 0.001

# SAVE SENT RANGE + TIME
sent_keys = set()

# =========================
# TELEGRAM SEND
# =========================

def send_telegram(text):

    try:

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            },
            timeout=10
        )

        print("SENT TO GROUP")

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

    number = str(number).replace(" ", "")

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
    carrier = item.get("carrier", "Unknown")
    log_time = item.get("time", "Unknown")

    range_ = get_range(number)

    text = f"""🔥 <b>NEW LIVE RANGE</b>

━━━━━━━━━━━━━━━━
📱 <b>APP :</b> {app}

━━━━━━━━━━━━━━━━
🌍 <b>COUNTRY :</b> {country}

━━━━━━━━━━━━━━━━
📡 <b>CARRIER :</b> {carrier}

━━━━━━━━━━━━━━━━
📶 <b>RANGE :</b>

<code>{range_}</code>

━━━━━━━━━━━━━━━━
⏰ <b>TIME :</b> {log_time}

━━━━━━━━━━━━━━━━
"""

    return text

# =========================
# PROCESS LOGS
# =========================

def process_logs(data):

    global sent_keys

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

        if not isinstance(item, dict):
            continue

        try:

            number = str(item.get("number", "")).strip()
            log_time = str(item.get("time", "")).strip()

            if not number:
                continue

            # RANGE
            range_ = get_range(number)

            # UNIQUE KEY
            unique_key = f"{range_}_{log_time}"

            # SKIP SAME RANGE SAME SECOND
            if unique_key in sent_keys:
                continue

            # SAVE KEY
            sent_keys.add(unique_key)

            # CLEAN MEMORY
            if len(sent_keys) > 10000:
                sent_keys = set(list(sent_keys)[-5000:])

            # FORMAT
            text = format_message(item)

            # INSTANT SEND
            send_telegram(text)

            print("NEW:", unique_key)

        except Exception as e:

            print("Process Error:", e)

# =========================
# MAIN LOOP
# =========================

print("🔥 INSTANT LIVE RANGE BOT STARTED...")

while True:

    try:

        # CONSOLE 1
        console_data = fetch_logs(
            "/api/v1/console/logs?limit=200"
        )

        process_logs(console_data)

        # CONSOLE 2
        engine2_data = fetch_logs(
            "/api/v1/console/logs/engine2?limit=200"
        )

        process_logs(engine2_data)

    except Exception as e:

        print("MAIN LOOP ERROR:", e)

    time.sleep(CHECK_DELAY)
