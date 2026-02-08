import json
import urllib.request
import urllib.error

url = 'http://localhost:8000/api/auth/signup'
data = json.dumps({"email": "admin@example.com", "password": "admin123"}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        print(r.getcode())
        print(r.read().decode())
except urllib.error.HTTPError as e:
    print('HTTP', e.code)
    print(e.read().decode())
except Exception as e:
    print('ERR', e)
