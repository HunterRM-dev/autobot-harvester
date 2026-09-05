import requests
import os
import time

# Railway akan sediakan nilai ni dari Environment Variables
ALCHEMY_URL = os.environ.get("ALCHEMY_URL")

def check_network():
    print("Bot sedang menyambung ke blockchain...")
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_blockNumber",
        "params": []
    }
    response = requests.post(ALCHEMY_URL, json=payload)
    if response.status_code == 200:
        block_hex = response.json()['result']
        block_num = int(block_hex, 16)
        print(f"✅ Berjaya sambung! Block Ethereum terkini: {block_num}")
    else:
        print("❌ Gagal sambung.")

# Supaya bot berulang (loop) setiap 10 saat
if __name__ == "__main__":
    while True:
        check_network()
        time.sleep(10) # Tidur 10 saat
