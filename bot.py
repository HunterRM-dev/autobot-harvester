import requests
import time
import sys

# =====================================================================
# KONFIGURASI BOT (World Chain Mainnet)
# =====================================================================
ALCHEMY_URL = "https://worldchain-mainnet.g.alchemy.com/v2/alch_vGDYfC7HldKkWt8hygzUU"

# Ini adalah address 'Burner' (alamat kosong) untuk kita test sambungan
WALLET_TO_CHECK = "0x0000000000000000000000000000000000000001"

def check_network():
    print("\n--- BOT SEDANG BEKERJA ---")
    print("Menghubungi World Chain melalui Alchemy...")
    
    # Arahan (JSON-RPC) standard Ethereum untuk semak baki
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getBalance",
        "params": [WALLET_TO_CHECK, "latest"]
    }
    
    headers = {"Content-Type": "application/json"}

    try:
        # Bot hantar request ke Alchemy
        response = requests.post(ALCHEMY_URL, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Kalau ada error dari server
            if 'error' in data and data['error']:
                print(f"❌ ERROR DARI ALCHEMY: {data['error']['message']}")
                return False
            
            # Kalau berjaya, kira baki
            balance_wei = int(data['result'], 16)
            balance_eth = balance_wei / 10**18
            
            print("✅ STATUS: Sambungan World Chain Berjaya!")
            print(f"💰 Baki Wallet Test: {balance_eth:.8f} ETH")
            return True
            
        else:
            print(f"❌ ERROR SERVER: Status Code {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ BOT CRASH/ERROR: {e}")
        return False

# =====================================================================
# ENGINE UTAMA (Loop Automatik)
# =====================================================================
if __name__ == "__main__":
    print("🤖 Autobot Harvester (World Chain) Telah Diaktifkan!")
    print("Bot akan semak setiap 15 saat.")
    
    cycle = 1
    while True:
        try:
            print(f"\n[Cycle #{cycle}]")
            check_network()
            time.sleep(15)
            cycle += 1
        except KeyboardInterrupt:
            sys.exit(0)
