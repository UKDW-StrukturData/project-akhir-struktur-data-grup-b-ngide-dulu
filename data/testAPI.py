import requests
import time
import json

API_HOST = "mobile-phone-specs-database.p.rapidapi.com"
API_KEY = "<<< MASUKKAN API-KEYMU DI SINI >>>"

headers = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": API_KEY
}

valid_phones = []

# RANGE ID YANG MAU DITES
START = 103000
END = 104000

for cid in range(START, END):
    try:
        url = f"https://{API_HOST}/gsm/get-specifications-by-phone-custom-id/{cid}"
        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code == 200:
            try:
                data = r.json()
                # kalau ada phoneDetails berarti valid
                if "phoneDetails" in data:
                    print(f"VALID → {cid} → {data['phoneDetails'].get('modelValue')}")
                    valid_phones.append(data)
            except:
                pass
        else:
            print(f"INVALID → {cid}")

    except Exception as e:
        print(f"ERROR → {cid}: {e}")

    time.sleep(0.4)  # biar tidak diblok API rate limit

# SIMPAN KE FILE LOCAL
with open("valid_phones.json", "w") as f:
    json.dump(valid_phones, f, indent=4)

print("\nDONE! Total valid:", len(valid_phones))
