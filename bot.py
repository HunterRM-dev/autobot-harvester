import requests
import time
import sys

# =====================================================================
# KONFIGURASI BOT (Dogecoin Mainnet)
# =====================================================================
ALCHEMY_URL = "https://dogecoin-mainnet.g.alchemy.com/v2/alch_vGDYfC7HldKkWt8hygzUU"

# Address Dogecoin untuk test (Address ini adalah address Burner/Donation)
WALLET_TO_CHECK = "DJ4k65Yb5ZaN4WBvMrYnNGvJMQugi6CPsi"

def check_network():
    print("\n--- BOT SEDANG BEKERJA ---")
    print(f"Menghubungi Dogecoin Network...")
    
    # Dogecoin guna arahan "getreceivedbyaddress" untuk check baki
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getreceivedbyaddress",
        "params": [WALLET_TO_CHECK]
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
            
            # Kalau berjaya, kira baki (Dogecoin biasanya jadi nombor biasa)
            balance_doge = float(data.get('result', 0.0))
            
            print("✅ STATUS: Sambungan Berjaya!")
            print(f"💰 Baki Wallet Test: {balance_doge} DOGE")
            return True
            
        else:
            print(f"❌ ERROR SERVER: Status Code {response.status_code}")
            print(response.text) # Print error sebenar dari server
            return False
            
    except Exception as e:
        print(f"❌ BOT CRASH/ERROR: {e}")
        return False

# =====================================================================
# ENGINE UTAMA (Loop Automatik)
# =====================================================================
if __name__ == "__main__":
    print("🤖 Autobot Harvester (Dogecoin) Telah Diaktifkan!")
    
    cycle = 1
    while True:
        try:
            print(f"\n[Cycle #{cycle}]")
            check_network()
            time.sleep(15)
            cycle += 1
        except KeyboardInterrupt:
            sys.exit(0)
