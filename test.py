import json

urlPool = []
pool = []

username = "sakis"
url = "https://youtube.com"
urlPool.append(json.dumps({"user": username, "url": url}))
urlPool.append(json.dumps({"user": username, "url": url}))


for item in urlPool:
    item=json.loads(item)
    print(item['url'])
    pool.append(item['url'])

print(str(pool))