import requests
import time

BASE_URL = "http://localhost:8000"

def test_resumen():
    try:
        response = requests.get(f"{BASE_URL}/facturas/resumen")
        if response.status_code == 200:
            print("✅ /facturas/resumen optimized query works!")
            print("📊 Result:", response.json())
        else:
            print(f"❌ /facturas/resumen failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Connection failed: {e}. Make sure the server is running.")

if __name__ == "__main__":
    test_resumen()
