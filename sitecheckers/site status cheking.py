import requests

URL = "https://api.github.com"

try:
    response = requests.get(URL)
except Exception as e:
    print(f"NOT OK: {str(e)}")
else:
    if response.status_code == 200:
        print("OK")
    else:
        print(f"NOT OK: HTTP response code {response.status_code}")
