import requests
import time
import threading
import os
from flask import Flask, render_template_string

app = Flask(__name__)

# =====================================================================
# PENGATURAN BOT
# =====================================================================
ALCHEMY_URL = os.environ.get("ALCHEMY_URL", "https://worldchain-mainnet.g.alchemy.com/v2/alch_vGDYfC7HldKkWt8hygzUU")
WALLET_TO_CHECK = "0x0000000000000000000000000000000000000001"

# Pangkalan Data Sementara (Untuk simpan log)
bot_logs = []
bot_cycles = 0
bot_last_block = 0

def check_network():
    global bot_cycles, bot_last_block
    print("Bot sedang menyambung ke World Chain...")
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_blockNumber",
        "params": []
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(ALCHEMY_URL, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            block_hex = data['result']
            block_num = int(block_hex, 16)
            
            current_time = time.strftime("%H:%M:%S")
            log_msg = f"[{current_time}] ✅ Sambungan berjaya! Block terkini: {block_num}"
            print(log_msg)
            
            bot_logs.append(log_msg)
            if len(bot_logs) > 15:  # Simpan 15 log terakhir
                bot_logs.pop(0)
                
            bot_cycles += 1
            bot_last_block = block_num
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Crash: {e}")
        return False

def bot_loop():
    print("🤖 Autobot Harvester (World Chain) Telah Diaktifkan di Background!")
    while True:
        check_network()
        time.sleep(15) # Check setiap 15 saat

# Mulakan bot di belakang tabir (Background Thread)
threading.Thread(target=bot_loop, daemon=True).start()

# =====================================================================
# WEBSITE DASHBOARD (Flask HTML)
# =====================================================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Autobot Dashboard | World Chain</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f1117;
            color: #e4e6eb;
            margin: 0;
            padding: 20px;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #333;
            padding-bottom: 15px;
            margin-bottom: 30px;
        }
        h1 { margin: 0; color: #00ff88; font-size: 24px;}
        .status-badge {
            background-color: #00ff88;
            color: #000;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
        }
        .stat-title { color: #8b949e; font-size: 14px; text-transform: uppercase; }
        .stat-value { font-size: 32px; font-weight: bold; margin-top: 10px; color: #fff; }
        .log-area {
            background-color: #000;
            border: 1px solid #333;
            height: 300px;
            overflow-y: auto;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 13px;
        }
        .log-time { color: #8b949e; }
        .log-success { color: #00ff88; }
        .btn {
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background-color: #30363d;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            border: 1px solid #555;
        }
        .btn:hover { background-color: #444; }
    </style>
</head>
<body>

    <header>
        <div>
            <h1>🤖 Autobot Control Panel</h1>
            <p style="margin: 5px 0 0 0; color: #8b949e;">The Autonomous World Chain Harvester</p>
        </div>
        <div>
            <span class="status-badge">● RUNNING</span>
        </div>
    </header>

    <div class="grid-container">
        <div class="card">
            <div class="stat-title">Total Bot Cycles</div>
            <div class="stat-value">{{ cycles }}</div>
        </div>
        <div class="card">
            <div class="stat-title">Latest Block Checked</div>
            <div class="stat-value">{{ last_block }}</div>
        </div>
        <div class="card">
            <div class="stat-title">Network Status</div>
            <div class="stat-value" style="color: #00ff88;">ONLINE</div>
        </div>
    </div>

    <div class="card">
        <div class="stat-title">Live Bot Logs</div>
        <div class="log-area">
            {% for log in logs %}
                <div>{{ log }}</div>
            {% endfor %}
        </div>
        <a href="/" class="btn">🔄 Refresh Logs</a>
    </div>

</body>
</html>
"""

@app.route('/')
def home():
    # Papar website dengan data dari bot
    return render_template_string(HTML_TEMPLATE, logs=bot_logs, cycles=bot_cycles, last_block=bot_last_block)

if __name__ == "__main__":
    # Railway akan cari port ni untuk hidupkan website
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
