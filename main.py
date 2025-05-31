import websocket
import json
import os
import time
import threading

USER_AGENT = "Mozilla/5.0 (Linux; Android 10; Redmi 8A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
WS_URL = "wss://websocket.layeredge.io/ws/node?token={}"

# Color code for cyan + reset
CYAN = '\033[96m'
RESET = '\033[0m'

def print_banner():
    banner = """
𝐅 𝐎 𝐑 𝐄 𝐒 𝐓 𝐀 𝐑 𝐌 𝐘  - 𝐋𝐀𝐘𝐄𝐑𝐄𝐃𝐆𝐄 - 𝟑         
https://t.me/forestarmy
"""
    print(CYAN + banner + RESET)

def get_token():
    if not os.path.exists("token.txt") or os.path.getsize("token.txt") == 0:
        token = input("[🛡️] Enter your LayerEdge token: ").strip()
        with open("token.txt", "w") as f:
            f.write(token)
        print("[💾] Token saved to token.txt")
    else:
        with open("token.txt", "r") as f:
            token = f.read().strip()
    return token

def send_heartbeat(ws):
    while ws.keep_running:
        try:
            time.sleep(5)
            ws.send(json.dumps({"type": "Heartbeat"}))
        except Exception as e:
            print(f"[💥] Heartbeat error: {e}")
            break

def on_open(ws):
    print("[🔌] Connected.")
    ws.send(json.dumps({"type": "NodeStart"}))
    threading.Thread(target=send_heartbeat, args=(ws,), daemon=True).start()

def on_message(ws, message):
    try:
        data = json.loads(message)
        print(f"[📩] {json.dumps(data, indent=2)}")
        if data.get("type") == "PointsUpdate":
            points = data["data"]["total_points"]
            boost = data["data"]["total_boost_points"]
            print(f"🔥 Total Points: {points} Boost: {boost}")
    except Exception as e:
        print(f"[⚠️] Error processing message: {e}")

def on_error(ws, error):
    print(f"[❌] Error receiving message: {error}")

def on_close(ws, code, reason):
    print(f"[🔌] Connection closed. Code: {code}, Reason: {reason}")
    print("[🔁] Reconnecting in 5 seconds...")
    time.sleep(5)
    start_ws(get_token())

def start_ws(token):
    print_banner()
    ws = websocket.WebSocketApp(
        WS_URL.format(token),
        header=[f"User-Agent: {USER_AGENT}"],
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

if __name__ == "__main__":
    token = get_token()
    start_ws(token)
