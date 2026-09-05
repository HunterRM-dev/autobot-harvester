import requests
import os
import time
import sys

# =====================================================================
# API KEY & KONFIGURASI (Hardcoded untuk senang kau test)
# =====================================================================
# Aku letak API Key kau terus kat sini macam yang kau request.
ALCHEMY_URL = "https://eth-mainnet.g.alchemy.com/v2/alch_vGDYfC7HldKkWt8hygzUU"

# Wallet Vitalik Buterin (Pencipta Ethereum) untuk kita check baki
WALLET_TO_CHECK = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

def check_balance():
    print("\n--- BOT SEDANG BEKERJA ---")
    print("Menghubungi jaringan Ethereum melalui Alchemy...")
    
    # Arahan (JSON-RPC) untuk minta baki wallet
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getBalance",
        "params": [WALLET_TO_CHECK, "latest"]
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Bot hantar request ke Alchemy
        response = requests.post(ALCHEMY_URL, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Kalau ada error dari Alchemy (contoh: API Key salah)
            if 'error' in data:
                print(f"❌ ERROR DARI ALCHEMY: {data['error']['message']}")
                return False
            
            # Blockchain bagi jawapan dalam Hexadecimal (base 16). Kena tukar ke integer.
            balance_wei_hex = data['result']
            balance_wei = int(balance_wei_hex, 16)
            
            # Tukar Wei ke ETH (1 ETH = 10^18 Wei)
            balance_eth = balance_wei / 10**18
            
            print("✅ STATUS: Sambungan Berjaya!")
            print(f"💰 Baki Wallet Vitalik: {balance_eth:.4f} ETH")
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
    print("🤖 Autobot Harvester Telah Diaktifkan!")
    print("Bot akan semak setiap 15 saat. Tekan CTRL+C untuk hentikan.")
    
    cycle = 1
    while True:
        try:
            print(f"\n[Cycle #{cycle}]")
            success = check_balance()
            
            if not success:
                print("Menunggu 30 saat sebelum cuba semula sebab ada error...")
                time.sleep(30)
            else:
                # Kalau berjaya, tunggu 15 saat sebelum buat lagi
                time.sleep(15)
                
            cycle += 1
            
        except KeyboardInterrupt:
            print("\n🛑 Bot dihentikan secara manual.")
            sys.exit(0)
