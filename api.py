import requests as api
i  = api.get("https://intervue.site")
print(i.status_code)
print(i.json())