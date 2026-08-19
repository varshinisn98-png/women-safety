import requests
import json

def test_locations():
    headers = {"User-Agent": "SurakshaSafetyApp/1.0 (contact: support@suraksha.ai)"}
    
    # 1. Mysuru Palace
    lat, lon = 12.3051, 76.6551
    url = f"https://nominatim.openstreetmap.org/search?amenity=police&format=json&viewbox={lon-0.08},{lat+0.08},{lon+0.08},{lat-0.08}&bounded=1&limit=4"
    r = requests.get(url, headers=headers, timeout=5)
    print("=== MYSURU PALACE AREA POLICE ===")
    for item in r.json():
        print(f" - {item.get('display_name')[:80]}... ({item.get('lat')}, {item.get('lon')})")

    # 2. Gateway of India, Mumbai
    lat, lon = 18.9220, 72.8347
    url = f"https://nominatim.openstreetmap.org/search?amenity=police&format=json&viewbox={lon-0.08},{lat+0.08},{lon+0.08},{lat-0.08}&bounded=1&limit=4"
    r = requests.get(url, headers=headers, timeout=5)
    print("=== MUMBAI GATEWAY OF INDIA AREA POLICE ===")
    for item in r.json():
        print(f" - {item.get('display_name')[:80]}... ({item.get('lat')}, {item.get('lon')})")

if __name__ == "__main__":
    test_locations()
